import sqlite3
import os

DB_PATH = os.path.join('db', 'shoe_store.sqlite')


def _conn():
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA foreign_keys = ON;")
    return c


def test_price():
    c = _conn()
    try:
        c.execute("INSERT INTO products (category, manufacturer, product_name, price) VALUES ('a','b','c',-1)")
        print("[FAIL] price")
    except sqlite3.IntegrityError:
        print("[OK] CHECK price > 0")
    finally:
        c.rollback()
        c.close()


def test_quantity():
    c = _conn()
    try:
        c.execute("INSERT INTO stock_items (product_id, size_id, quantity) VALUES (1,1,-1)")
        print("[FAIL] quantity")
    except sqlite3.IntegrityError:
        print("[OK] CHECK quantity >= 0")
    finally:
        c.rollback()
        c.close()


def test_login():
    c = _conn()
    try:
        c.execute("INSERT INTO users (last_name, first_name, login, role_id) VALUES ('a','b','xx',1)")
        print("[FAIL] login")
    except sqlite3.IntegrityError:
        print("[OK] CHECK login length")
    finally:
        c.rollback()
        c.close()


def test_unique_login():
    c = _conn()
    try:
        r = c.execute("SELECT login FROM users LIMIT 1").fetchone()
        if not r:
            print("[SKIP] unique login")
            return
        c.execute("INSERT INTO users (last_name, first_name, login, role_id) VALUES ('a','b',?,1)", (r[0],))
        print("[FAIL] unique login")
    except sqlite3.IntegrityError:
        print("[OK] UNIQUE login")
    finally:
        c.rollback()
        c.close()


def test_restrict_user():
    c = _conn()
    try:
        r = c.execute("SELECT user_id FROM orders LIMIT 1").fetchone()
        if not r:
            print("[SKIP] restrict user")
            return
        c.execute("DELETE FROM users WHERE user_id = ?", (r[0],))
        print("[FAIL] restrict user")
    except sqlite3.IntegrityError:
        print("[OK] ON DELETE RESTRICT users")
    finally:
        c.rollback()
        c.close()


def test_cascade():
    c = _conn()
    try:
        r = c.execute("SELECT order_id FROM order_items LIMIT 1").fetchone()
        if not r:
            print("[SKIP] cascade")
            return
        oid = r[0]
        before = c.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (oid,)).fetchone()[0]
        c.execute("DELETE FROM orders WHERE order_id = ?", (oid,))
        after = c.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (oid,)).fetchone()[0]
        print("[OK] CASCADE" if before > 0 and after == 0 else "[FAIL] cascade")
    finally:
        c.rollback()
        c.close()


def main():
    print("=== Проверка ограничений ===")
    test_price()
    test_quantity()
    test_login()
    test_unique_login()
    test_restrict_user()
    test_cascade()


if __name__ == '__main__':
    main()