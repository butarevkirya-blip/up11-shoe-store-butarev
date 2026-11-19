import sqlite3
import os

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
DB_PATH = os.path.join(BASE_DIR, 'db', 'shoe_store.sqlite')
DB_PATH = os.path.join(BASE_DIR, 'db', 'shoe_store.sqlite')

QUERIES_DAY6 = """
SELECT * FROM products;
SELECT product_name, price FROM products;
SELECT product_name, price FROM products WHERE price > 10000;
SELECT product_name, manufacturer, price FROM products WHERE category = 'кроссовки';
SELECT product_name, price FROM products WHERE manufacturer = 'Nike';
SELECT product_name, price FROM products ORDER BY price DESC;
SELECT manufacturer, product_name, price FROM products ORDER BY manufacturer ASC, price ASC;
SELECT product_name, price FROM products ORDER BY price DESC LIMIT 5;
SELECT product_name, price FROM products ORDER BY product_id LIMIT 5 OFFSET 5;
SELECT DISTINCT category FROM products;
SELECT DISTINCT manufacturer FROM products ORDER BY manufacturer;
SELECT DISTINCT category, subcategory FROM products ORDER BY category, subcategory;
SELECT user_id, last_name, first_name, login FROM users WHERE login = 'admin';
SELECT order_id, order_date, user_id FROM orders WHERE order_date BETWEEN '2026-10-01' AND '2026-10-31' ORDER BY order_date;
SELECT product_name, price FROM products WHERE price BETWEEN 5000 AND 12000 ORDER BY price;
"""

QUERIES_DAY7 = """
SELECT o.order_id, o.order_date, u.last_name || ' ' || u.first_name AS client
FROM orders o INNER JOIN users u ON o.user_id = u.user_id ORDER BY o.order_date;

SELECT oi.order_item_id, p.product_name, s.size_value, oi.quantity, oi.price_at_order,
       oi.quantity * oi.price_at_order AS line_total
FROM order_items oi
JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
JOIN products p ON si.product_id = p.product_id
JOIN sizes s ON si.size_id = s.size_id
WHERE oi.order_id = 1;

SELECT category, COUNT(*) AS cnt FROM products GROUP BY category ORDER BY cnt DESC;
SELECT manufacturer, AVG(price) AS avg_price FROM products GROUP BY manufacturer ORDER BY avg_price DESC;

SELECT u.user_id, u.last_name || ' ' || u.first_name AS client,
       COUNT(o.order_id) AS orders_cnt,
       SUM(oi.quantity * oi.price_at_order) AS total_sum
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id ORDER BY total_sum DESC LIMIT 10;

SELECT o.order_id, o.order_date, SUM(oi.quantity * oi.price_at_order) AS total
FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date BETWEEN '2026-10-01' AND '2026-10-31'
GROUP BY o.order_id ORDER BY total DESC;

SELECT p.product_name, s.size_value, COALESCE(si.quantity, 0) AS qty
FROM products p
LEFT JOIN stock_items si ON p.product_id = si.product_id
LEFT JOIN sizes s ON si.size_id = s.size_id
ORDER BY p.product_name, s.size_value;

SELECT u.user_id, u.last_name, u.first_name, u.login
FROM users u LEFT JOIN orders o ON u.user_id = o.user_id WHERE o.order_id IS NULL;

SELECT r.role_name, COUNT(o.order_id) AS orders_cnt
FROM roles r
LEFT JOIN users u ON r.role_id = u.role_id
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY r.role_id;

SELECT u.login, AVG(oi.quantity * oi.price_at_order) AS avg_check
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id HAVING AVG(oi.quantity * oi.price_at_order) > 1000;

SELECT p.product_name, SUM(oi.quantity) AS total_sold
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
GROUP BY p.product_id HAVING SUM(oi.quantity) > 5;

SELECT p.category, SUM(oi.quantity * oi.price_at_order) AS revenue
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
GROUP BY p.category ORDER BY revenue DESC;

SELECT p.product_name, COUNT(si.size_id) AS sizes_count
FROM products p LEFT JOIN stock_items si ON p.product_id = si.product_id
GROUP BY p.product_id ORDER BY sizes_count DESC;

SELECT SUM(oi.quantity * oi.price_at_order) AS grand_total FROM order_items oi;

SELECT AVG(item_count) AS avg_items
FROM (SELECT order_id, SUM(quantity) AS item_count FROM order_items GROUP BY order_id);
"""

QUERIES_DAY8 = """
SELECT p.product_id, p.product_name FROM products p
WHERE NOT EXISTS (
    SELECT 1 FROM order_items oi
    JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
    WHERE si.product_id = p.product_id
);

SELECT user_id, last_name, first_name FROM users
WHERE user_id IN (SELECT user_id FROM orders GROUP BY user_id HAVING COUNT(*) > 3);

SELECT product_name, price FROM products WHERE price > (SELECT AVG(price) FROM products);

SELECT category, product_name, price,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
FROM products ORDER BY category, rn;

SELECT manufacturer, AVG(price) AS avg_price,
       RANK() OVER (ORDER BY AVG(price) DESC) AS rnk
FROM products GROUP BY manufacturer;

SELECT o.order_date,
       SUM(oi.quantity * oi.price_at_order) AS day_sum,
       SUM(SUM(oi.quantity * oi.price_at_order)) OVER (ORDER BY o.order_date) AS cumulative
FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_date ORDER BY o.order_date;

WITH ranked AS (
    SELECT category, product_name, price,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
    FROM products
)
SELECT category, product_name, price FROM ranked WHERE rn = 1;

SELECT u.user_id, u.last_name, u.first_name FROM users u
WHERE u.user_id = (
    SELECT o.user_id FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.user_id ORDER BY SUM(oi.quantity * oi.price_at_order) DESC LIMIT 1
);

SELECT o.order_id,
       SUM(oi.quantity * oi.price_at_order) AS order_sum,
       ROUND(100.0 * SUM(oi.quantity * oi.price_at_order) /
             (SELECT SUM(quantity * price_at_order) FROM order_items), 2) AS percent
FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;

SELECT product_name, category, price,
       ROUND(AVG(price) OVER (PARTITION BY category), 2) AS cat_avg,
       ROUND(price - AVG(price) OVER (PARTITION BY category), 2) AS diff
FROM products ORDER BY category, price DESC;
"""

VIEWS_INDEXES = """
CREATE VIEW IF NOT EXISTS view_orders_with_client AS
SELECT o.order_id, o.order_date,
       u.last_name || ' ' || u.first_name || COALESCE(' ' || u.middle_name, '') AS client_fio,
       u.login
FROM orders o JOIN users u ON o.user_id = u.user_id;

CREATE VIEW IF NOT EXISTS view_products_with_stock AS
SELECT p.product_id, p.product_name, p.category, p.price, s.size_value, si.quantity
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN sizes s ON si.size_id = s.size_id;

CREATE VIEW IF NOT EXISTS view_top_clients AS
SELECT u.user_id,
       u.last_name || ' ' || u.first_name AS client_name,
       COUNT(o.order_id) AS orders_count,
       SUM(oi.quantity * oi.price_at_order) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id ORDER BY total_spent DESC;

CREATE INDEX IF NOT EXISTS idx_products_manufacturer ON products(manufacturer);
CREATE INDEX IF NOT EXISTS idx_users_login ON users(login);
CREATE INDEX IF NOT EXISTS idx_order_items_price ON order_items(price_at_order);
"""

TRIGGERS = """
CREATE TRIGGER IF NOT EXISTS trg_orders_insert
AFTER INSERT ON orders
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, user_login, log_time)
    VALUES ('orders', 'INSERT', NEW.order_id, 'system', datetime('now'));
END;

CREATE TRIGGER IF NOT EXISTS trg_orders_delete
AFTER DELETE ON orders
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, user_login, log_time)
    VALUES ('orders', 'DELETE', OLD.order_id, 'system', datetime('now'));
END;

CREATE TRIGGER IF NOT EXISTS trg_order_items_insert
AFTER INSERT ON order_items
BEGIN
    UPDATE stock_items SET quantity = quantity - NEW.quantity
    WHERE stock_item_id = NEW.stock_item_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_users_delete_guard
BEFORE DELETE ON users
WHEN EXISTS (SELECT 1 FROM orders WHERE user_id = OLD.user_id)
BEGIN
    SELECT RAISE(ABORT, 'Нельзя удалить пользователя с заказами');
END;
"""


def execute(conn, label, sql):
    print("=" * 60)
    print(label)
    print("=" * 60)
    try:
        conn.executescript(sql)
        conn.commit()
        print("[OK]", label)
    except sqlite3.Error as e:
        print("[ERROR]", e)


def main():
    print("Файл БД:", DB_PATH)
    if not os.path.exists(DB_PATH):
        print("[ERROR] БД не найдена. Сначала запусти src/db_init.py и src/db_seed.py")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        execute(conn, "Базовые запросы (day6, 15 шт.)", QUERIES_DAY6)
        execute(conn, "JOIN и агрегаты (day7, 15 шт.)", QUERIES_DAY7)
        execute(conn, "Подзапросы и оконные функции (day8, 10 шт.)", QUERIES_DAY8)
        execute(conn, "Представления и индексы", VIEWS_INDEXES)
        execute(conn, "Триггеры", TRIGGERS)
    finally:
        conn.close()
    print("=" * 60)
    print("ВСЁ ГОТОВО. Все запросы, представления и триггеры применены.")
    print("Проверь в SQLite Viewer (правой кнопкой по db/shoe_store.sqlite).")


if __name__ == '__main__':
    main()