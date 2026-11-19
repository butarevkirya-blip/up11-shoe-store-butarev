import sqlite3
import os

DB_PATH = os.path.join('db', 'shoe_store.sqlite')


def analyze():
    conn = sqlite3.connect(DB_PATH)
    tables = ['roles', 'users', 'products', 'sizes', 'stock_items',
              'orders', 'order_items', 'audit_log']
    print("=== Статистика ===")
    for t in tables:
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {n}")
    print("Размер файла:", os.path.getsize(DB_PATH), "байт")
    print("=== Индексы ===")
    for name, tbl in conn.execute("""
        SELECT name, tbl_name FROM sqlite_master
        WHERE type='index' AND name NOT LIKE 'sqlite_%'
        ORDER BY tbl_name, name
    """):
        print(f"  {tbl}.{name}")
    conn.close()


if __name__ == '__main__':
    analyze()