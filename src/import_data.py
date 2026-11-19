import sqlite3
import os
from openpyxl import load_workbook

DB_PATH = os.path.join('db', 'shoe_store.sqlite')
DATA_DIR = 'data'


def import_roles(conn):
    roles = ['администратор', 'менеджер', 'пользователь', 'читатель']
    for r in roles:
        conn.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", (r,))
    conn.commit()
    print("[OK] Роли:", len(roles))


def import_sizes(conn):
    path = os.path.join(DATA_DIR, 'Sizes_import.xlsx')
    if not os.path.exists(path):
        print("[SKIP]", path)
        return
    wb = load_workbook(path, read_only=True)
    ws = wb.active
    cnt = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        conn.execute("INSERT OR IGNORE INTO sizes (size_value) VALUES (?)", (row[0],))
        cnt += 1
    conn.commit()
    wb.close()
    print("[OK] Размеры:", cnt)


def import_products(conn):
    path = os.path.join(DATA_DIR, 'Products_import.xlsx')
    if not os.path.exists(path):
        print("[SKIP]", path)
        return
    wb = load_workbook(path, read_only=True)
    ws = wb.active
    cnt = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        conn.execute("""
            INSERT INTO products
                (category, subcategory, manufacturer, product_name,
                 image_path, composition, description, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, row)
        cnt += 1
    conn.commit()
    wb.close()
    print("[OK] Товары:", cnt)


def import_users(conn):
    path = os.path.join(DATA_DIR, 'Users_import.xlsx')
    if not os.path.exists(path):
        print("[SKIP]", path)
        return
    wb = load_workbook(path, read_only=True)
    ws = wb.active
    cnt = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        last_name, first_name, middle_name, login, role_name = row
        r = conn.execute("SELECT role_id FROM roles WHERE role_name = ?", (role_name,)).fetchone()
        if not r:
            continue
        conn.execute("""
            INSERT OR IGNORE INTO users
                (last_name, first_name, middle_name, login, role_id)
            VALUES (?, ?, ?, ?, ?)
        """, (last_name, first_name, middle_name, login, r[0]))
        cnt += 1
    conn.commit()
    wb.close()
    print("[OK] Пользователи:", cnt)


def import_stock_items(conn):
    path = os.path.join(DATA_DIR, 'Stock_Items_import.xlsx')
    if not os.path.exists(path):
        print("[SKIP]", path)
        return
    wb = load_workbook(path, read_only=True)
    ws = wb.active
    cnt = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        conn.execute("""
            INSERT OR IGNORE INTO stock_items (product_id, size_id, quantity)
            VALUES (?, ?, ?)
        """, row)
        cnt += 1
    conn.commit()
    wb.close()
    print("[OK] Позиции:", cnt)


def import_orders(conn):
    path = os.path.join(DATA_DIR, 'Orders_import.xlsx')
    if not os.path.exists(path):
        print("[SKIP]", path)
        return
    wb = load_workbook(path, read_only=True)
    ws = wb.active
    cnt = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        order_date, user_login = row
        r = conn.execute("SELECT user_id FROM users WHERE login = ?", (user_login,)).fetchone()
        if not r:
            continue
        conn.execute("INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
                     (order_date, r[0]))
        cnt += 1
    conn.commit()
    wb.close()
    print("[OK] Заказы:", cnt)


def check_integrity(conn):
    for table in ['roles', 'users', 'products', 'sizes', 'stock_items', 'orders']:
        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {n}")
    violations = conn.execute("PRAGMA foreign_key_check;").fetchall()
    if violations:
        print("[FAIL] Нарушения:", violations)
    else:
        print("[OK] Целостность в порядке")


def main():
    if not os.path.exists(DB_PATH):
        print("[ERROR] Сначала запустите src/db_init.py")
        return
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        import_roles(conn)
        import_sizes(conn)
        import_products(conn)
        import_users(conn)
        import_stock_items(conn)
        import_orders(conn)
        print("--- Проверка ---")
        check_integrity(conn)
    finally:
        conn.close()


if __name__ == '__main__':
    main()