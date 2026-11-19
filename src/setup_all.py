import os
import sqlite3
import random
from datetime import datetime, timedelta


def find_project_root():
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, 'src')):
        return cwd
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(5):
        if os.path.isdir(os.path.join(current, 'src')):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = find_project_root()
DB_DIR = os.path.join(BASE_DIR, 'db')
DB_PATH = os.path.join(DB_DIR, 'shoe_store.sqlite')

print("Корень проекта:", BASE_DIR)
print("Проверка src:", os.path.isdir(os.path.join(BASE_DIR, 'src')))
print("Проверка db: ", os.path.isdir(os.path.join(BASE_DIR, 'db')))
print("Файл БД:    ", DB_PATH)

os.makedirs(DB_DIR, exist_ok=True)

if os.path.exists(DB_PATH):
    print("Удаляю старую БД:", DB_PATH)
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")

conn.executescript("""
CREATE TABLE roles (
    role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL UNIQUE CHECK (length(role_name) > 0)
);
CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name   TEXT NOT NULL,
    first_name  TEXT NOT NULL,
    middle_name TEXT,
    login       TEXT NOT NULL UNIQUE CHECK (length(login) BETWEEN 3 AND 20),
    role_id     INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
);
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    category     TEXT NOT NULL,
    subcategory  TEXT,
    manufacturer TEXT NOT NULL,
    product_name TEXT NOT NULL,
    image_path   TEXT,
    composition  TEXT,
    description  TEXT,
    price        REAL NOT NULL CHECK (price > 0)
);
CREATE TABLE sizes (
    size_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    size_value REAL NOT NULL UNIQUE CHECK (size_value BETWEEN 15 AND 50)
);
CREATE TABLE stock_items (
    stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id    INTEGER NOT NULL,
    size_id       INTEGER NOT NULL,
    quantity      INTEGER NOT NULL CHECK (quantity >= 0),
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (size_id)    REFERENCES sizes(size_id)       ON DELETE RESTRICT,
    UNIQUE (product_id, size_id)
);
CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT NOT NULL CHECK (order_date LIKE '____-__-__'),
    user_id    INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);
CREATE TABLE order_items (
    order_item_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id       INTEGER NOT NULL,
    stock_item_id  INTEGER NOT NULL,
    quantity       INTEGER NOT NULL CHECK (quantity > 0),
    price_at_order REAL    NOT NULL CHECK (price_at_order > 0),
    FOREIGN KEY (order_id)      REFERENCES orders(order_id)           ON DELETE CASCADE,
    FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id) ON DELETE RESTRICT
);
CREATE TABLE audit_log (
    log_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    operation  TEXT NOT NULL,
    record_id  INTEGER,
    user_login TEXT,
    log_time   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_users_role_id             ON users(role_id);
CREATE INDEX idx_stock_items_product_id    ON stock_items(product_id);
CREATE INDEX idx_stock_items_size_id       ON stock_items(size_id);
CREATE INDEX idx_orders_user_id            ON orders(user_id);
CREATE INDEX idx_order_items_order_id      ON order_items(order_id);
CREATE INDEX idx_order_items_stock_item_id ON order_items(stock_item_id);
CREATE INDEX idx_products_name             ON products(product_name);
CREATE INDEX idx_products_price            ON products(price);
CREATE INDEX idx_products_category         ON products(category);
CREATE INDEX idx_orders_date               ON orders(order_date);
""")
conn.commit()
print("[OK] Таблицы созданы")

for r in ['администратор', 'менеджер', 'пользователь', 'читатель']:
    conn.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", (r,))
roles = {n: i for i, n in conn.execute("SELECT role_id, role_name FROM roles")}

for s in range(35, 46):
    conn.execute("INSERT OR IGNORE INTO sizes (size_value) VALUES (?)", (s,))
sizes_ids = [r[0] for r in conn.execute("SELECT size_id FROM sizes ORDER BY size_value")]

products = [
    ('кроссовки', 'спортивные', 'Nike', 'Air Max 90', 'images/nike.jpg', 'текстиль', 'Кроссовки', 8990.00),
    ('ботинки', 'зимние', 'Timberland', 'Winter Boots', 'images/timber.jpg', 'кожа', 'Ботинки', 12990.00),
    ('туфли', 'классические', 'ECCO', 'Oxford', 'images/ecco.jpg', 'кожа', 'Туфли', 10990.00),
    ('кроссовки', 'беговые', 'Adidas', 'Ultraboost', 'images/adidas.jpg', 'текстиль', 'Беговые', 13990.00),
    ('сандалии', 'летние', 'Crocs', 'Classic Clog', 'images/crocs.jpg', 'EVA', 'Сандалии', 3490.00),
    ('ботинки', 'демисезон', 'Dr. Martens', '1460', 'images/dm.jpg', 'кожа', 'Ботинки', 15990.00),
]
for p in products:
    conn.execute("""
        INSERT INTO products (category, subcategory, manufacturer, product_name,
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
        INSERT INTO users (last_name, first_name, middle_name, login, role_id)
        VALUES (?, ?, ?, ?, ?)
    """, (u[0], u[1], u[2], u[3], roles[u[4]]))
user_ids = [r[0] for r in conn.execute("SELECT user_id FROM users ORDER BY user_id")]

for pid in product_ids:
    for sid in sizes_ids:
        conn.execute("INSERT INTO stock_items (product_id, size_id, quantity) VALUES (?, ?, ?)",
                     (pid, sid, random.randint(0, 20)))

available = [r[0] for r in conn.execute("SELECT stock_item_id FROM stock_items WHERE quantity > 0")]

for _ in range(15):
    order_date = (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
    cur = conn.execute("INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
                       (order_date, random.choice(user_ids)))
    oid = cur.lastrowid
    for _ in range(random.randint(1, 3)):
        si = random.choice(available)
        price = conn.execute("""
            SELECT p.price FROM products p
            JOIN stock_items si ON p.product_id = si.product_id
            WHERE si.stock_item_id = ?
        """, (si,)).fetchone()[0]
        conn.execute("""
            INSERT INTO order_items (order_id, stock_item_id, quantity, price_at_order)
            VALUES (?, ?, ?, ?)
        """, (oid, si, random.randint(1, 3), price))

conn.commit()
conn.close()

print("[OK] Тестовые данные добавлены")
print("[OK] ВСЁ ГОТОВО. БД:", DB_PATH)
print("Теперь запусти src/run_queries.py — там будет [OK], а не [ERROR]")