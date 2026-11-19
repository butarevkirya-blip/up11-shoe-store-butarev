import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join('db', 'shoe_store.sqlite')


def seed():
    if not os.path.exists(DB_PATH):
        print("[ERROR] Сначала запустите src/db_init.py")
        return
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    for r in ['администратор', 'менеджер', 'пользователь', 'читатель']:
        conn.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", (r,))
    roles = {n: i for i, n in conn.execute("SELECT role_id, role_name FROM roles")}

    for s in range(35, 46):
        conn.execute("INSERT OR IGNORE INTO sizes (size_value) VALUES (?)", (s,))
    sizes_ids = [r[0] for r in conn.execute("SELECT size_id FROM sizes ORDER BY size_value")]

    products = [
        ('кроссовки', 'спортивные', 'Nike', 'Air Max 90',
         'images/nike_am90.jpg', 'текстиль', 'Классические кроссовки', 8990.00),
        ('ботинки', 'зимние', 'Timberland', 'Winter Boots',
         'images/timber.jpg', 'кожа', 'Тёплые ботинки', 12990.00),
        ('туфли', 'классические', 'ECCO', 'Oxford',
         'images/ecco.jpg', 'кожа', 'Элегантные туфли', 10990.00),
        ('кроссовки', 'беговые', 'Adidas', 'Ultraboost 22',
         'images/adidas.jpg', 'текстиль', 'Беговые', 13990.00),
        ('сандалии', 'летние', 'Crocs', 'Classic Clog',
         'images/crocs.jpg', 'EVA', 'Лёгкие', 3490.00),
        ('ботинки', 'демисезон', 'Dr. Martens', '1460',
         'images/dm.jpg', 'кожа', 'Культовые', 15990.00),
    ]
    for p in products:
        conn.execute("""
            INSERT INTO products
                (category, subcategory, manufacturer, product_name,
                 image_path, composition, description, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, p)
    product_ids = [r[0] for r in conn.execute("SELECT product_id FROM products ORDER BY product_id")]

    users = [
        ('Иванов', 'Иван', 'Иванович', 'admin', 'администратор'),
        ('Петров', 'Пётр', 'Петрович', 'manager', 'менеджер'),
        ('Сидоров', 'Сидор', 'Сидорович', 'user1', 'пользователь'),
        ('Кузнецова', 'Анна', 'Сергеевна', 'user2', 'пользователь'),
        ('Смирнов', 'Алексей', 'Владимирович', 'user3', 'пользователь'),
        ('Читатель', 'Читатель', 'Читателевич', 'reader', 'читатель'),
    ]
    for u in users:
        conn.execute("""
            INSERT OR IGNORE INTO users
                (last_name, first_name, middle_name, login, role_id)
            VALUES (?, ?, ?, ?, ?)
        """, (u[0], u[1], u[2], u[3], roles[u[4]]))
    user_ids = [r[0] for r in conn.execute("SELECT user_id FROM users ORDER BY user_id")]

    for pid in product_ids:
        for sid in sizes_ids:
            qty = random.randint(0, 20)
            conn.execute("""
                INSERT OR IGNORE INTO stock_items (product_id, size_id, quantity)
                VALUES (?, ?, ?)
            """, (pid, sid, qty))

    available = [r[0] for r in conn.execute("SELECT stock_item_id FROM stock_items WHERE quantity > 0")]
    if not available:
        available = [r[0] for r in conn.execute("SELECT stock_item_id FROM stock_items")]

    for _ in range(15):
        order_date = (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
        user_id = random.choice(user_ids)
        cur = conn.execute("INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
                           (order_date, user_id))
        order_id = cur.lastrowid
        for _ in range(random.randint(1, 3)):
            si = random.choice(available)
            qty = random.randint(1, 3)
            r = conn.execute("""
                SELECT p.price FROM products p
                JOIN stock_items si ON p.product_id = si.product_id
                WHERE si.stock_item_id = ?
            """, (si,)).fetchone()
            if not r:
                continue
            conn.execute("""
                INSERT INTO order_items
                    (order_id, stock_item_id, quantity, price_at_order)
                VALUES (?, ?, ?, ?)
            """, (order_id, si, qty, r[0]))

    conn.commit()
    conn.close()
    print("[OK] Тестовые данные добавлены")


if __name__ == '__main__':
    seed()