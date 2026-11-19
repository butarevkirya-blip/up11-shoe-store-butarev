import sqlite3
import os

DB_PATH = os.path.join('db', 'shoe_store.sqlite')


def validate():
    conn = sqlite3.connect(DB_PATH)
    checks = [
        ("Цена <= 0", "SELECT COUNT(*) FROM products WHERE price <= 0"),
        ("Отриц. количество", "SELECT COUNT(*) FROM stock_items WHERE quantity < 0"),
        ("Заказы без клиента", "SELECT COUNT(*) FROM orders WHERE user_id IS NULL"),
        ("Позиции qty <= 0", "SELECT COUNT(*) FROM order_items WHERE quantity <= 0"),
        ("Пользователи без роли", "SELECT COUNT(*) FROM users WHERE role_id IS NULL"),
    ]
    for label, sql in checks:
        n = conn.execute(sql).fetchone()[0]
        print(f"[{'OK' if n == 0 else 'FAIL'}] {label}: {n}")
    conn.close()


if __name__ == '__main__':
    validate()