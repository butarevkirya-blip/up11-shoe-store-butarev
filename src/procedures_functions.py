import sqlite3
import os

DB_PATH = os.path.join('db', 'shoe_store.sqlite')


def register_functions(conn):
    def order_total(order_id):
        r = conn.execute(
            "SELECT COALESCE(SUM(quantity * price_at_order), 0) FROM order_items WHERE order_id = ?",
            (order_id,)
        ).fetchone()
        return r[0]

    def product_stock(product_id):
        r = conn.execute(
            "SELECT COALESCE(SUM(quantity), 0) FROM stock_items WHERE product_id = ?",
            (product_id,)
        ).fetchone()
        return r[0]

    def apply_discount(total):
        try:
            t = float(total)
        except (TypeError, ValueError):
            return 0.0
        return round(t * 0.9, 2) if t > 50000 else t

    def fio(last, first, middle):
        return ' '.join(p for p in [last, first, middle] if p)

    conn.create_function("order_total", 1, order_total)
    conn.create_function("product_stock", 1, product_stock)
    conn.create_function("apply_discount", 1, apply_discount)
    conn.create_function("fio", 3, fio)


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        register_functions(conn)
        r = conn.execute("SELECT order_total(1), apply_discount(60000), fio('Иванов','Иван','Иванович')").fetchone()
        print("[OK] Функции зарегистрированы. Тест:", r)
    finally:
        conn.close()


if __name__ == '__main__':
    main()