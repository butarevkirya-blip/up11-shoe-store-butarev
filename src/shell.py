import sqlite3
import os
import sys

DB_PATH = os.path.join('db', 'shoe_store.sqlite')

PERMISSIONS = {
    'читатель':      {'view_catalog'},
    'пользователь':  {'view_catalog', 'filter_catalog', 'create_order'},
    'менеджер':      {'view_catalog', 'filter_catalog', 'create_order', 'view_orders', 'delete_order'},
    'администратор': {'view_catalog', 'filter_catalog', 'create_order', 'view_orders', 'delete_order', 'edit_order'},
}


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def login(conn):
    login_input = input("Введите логин: ").strip()
    row = conn.execute("""
        SELECT u.user_id, u.last_name, u.first_name, r.role_name
        FROM users u JOIN roles r ON u.role_id = r.role_id
        WHERE u.login = ?
    """, (login_input,)).fetchone()
    if not row:
        print("[ERROR] Пользователь не найден")
        return None
    user = {'user_id': row[0], 'fio': f"{row[1]} {row[2]}", 'role': row[3]}
    conn.execute("INSERT INTO audit_log (table_name, operation, user_login) VALUES (?, ?, ?)",
                 ('users', 'LOGIN', login_input))
    conn.commit()
    print(f"[OK] Добро пожаловать, {user['fio']} (роль: {user['role']})")
    return user


def has_perm(user, perm):
    return perm in PERMISSIONS.get(user['role'], set())


def view_catalog(conn):
    print("\n--- Каталог ---")
    for r in conn.execute("""
        SELECT p.product_id, p.product_name, p.manufacturer, p.price, s.size_value, si.quantity
        FROM products p
        JOIN stock_items si ON p.product_id = si.product_id
        JOIN sizes s ON si.size_id = s.size_id
        WHERE si.quantity > 0
        ORDER BY p.product_name, s.size_value
    """):
        print(f"ID={r[0]} | {r[1]} | {r[2]} | {r[3]} руб. | размер {r[4]} | в наличии {r[5]}")


def filter_catalog(conn):
    keyword = input("Поиск: ").strip()
    for r in conn.execute("""
        SELECT product_id, product_name, manufacturer, price
        FROM products
        WHERE product_name LIKE ? OR manufacturer LIKE ?
        ORDER BY price DESC
    """, (f"%{keyword}%", f"%{keyword}%")):
        print(f"ID={r[0]} | {r[1]} | {r[2]} | {r[3]} руб.")


def view_orders(conn):
    print("\n--- Заказы ---")
    for r in conn.execute("""
        SELECT o.order_id, o.order_date,
               u.last_name || ' ' || u.first_name AS client,
               COALESCE(SUM(oi.quantity * oi.price_at_order), 0) AS total
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY o.order_id
        ORDER BY o.order_date DESC
    """):
        print(f"№{r[0]} | {r[1]} | {r[2]} | сумма: {r[3]} руб.")


def delete_order(conn):
    oid = input("ID заказа: ").strip()
    try:
        conn.execute("DELETE FROM orders WHERE order_id = ?", (int(oid),))
        conn.commit()
        print(f"[OK] Заказ {oid} удалён")
    except (ValueError, sqlite3.Error) as e:
        print("[ERROR]", e)


def main():
    if not os.path.exists(DB_PATH):
        print("[ERROR] Сначала запустите src/db_init.py")
        sys.exit(1)
    conn = connect()
    user = login(conn)
    if not user:
        conn.close()
        return
    while True:
        print("\n=== Меню ===")
        print("1. Просмотр каталога")
        if has_perm(user, 'filter_catalog'):
            print("2. Поиск по каталогу")
        if has_perm(user, 'view_orders'):
            print("3. Просмотр заказов")
        if has_perm(user, 'delete_order'):
            print("4. Удалить заказ")
        print("0. Выход")
        choice = input("Выбор: ").strip()
        if choice == '1':
            view_catalog(conn)
        elif choice == '2' and has_perm(user, 'filter_catalog'):
            filter_catalog(conn)
        elif choice == '3' and has_perm(user, 'view_orders'):
            view_orders(conn)
        elif choice == '4' and has_perm(user, 'delete_order'):
            delete_order(conn)
        elif choice == '0':
            print("До свидания!")
            break
        else:
            print("[ERROR] Неверный выбор или нет прав")
    conn.close()


if __name__ == '__main__':
    main()