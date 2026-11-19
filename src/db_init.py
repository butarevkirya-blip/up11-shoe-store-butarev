import sqlite3
import os

DB_PATH = os.path.join('db', 'shoe_store.sqlite')


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT    NOT NULL UNIQUE CHECK (length(role_name) > 0)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name   TEXT    NOT NULL,
        first_name  TEXT    NOT NULL,
        middle_name TEXT,
        login       TEXT    NOT NULL UNIQUE CHECK (length(login) BETWEEN 3 AND 20),
        role_id     INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        category     TEXT    NOT NULL,
        subcategory  TEXT,
        manufacturer TEXT    NOT NULL,
        product_name TEXT    NOT NULL,
        image_path   TEXT,
        composition  TEXT,
        description  TEXT,
        price        REAL    NOT NULL CHECK (price > 0)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sizes (
        size_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        size_value REAL    NOT NULL UNIQUE CHECK (size_value BETWEEN 15 AND 50)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_items (
        stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id    INTEGER NOT NULL,
        size_id       INTEGER NOT NULL,
        quantity      INTEGER NOT NULL CHECK (quantity >= 0),
        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
        FOREIGN KEY (size_id)    REFERENCES sizes(size_id)       ON DELETE RESTRICT,
        UNIQUE (product_id, size_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT    NOT NULL CHECK (order_date LIKE '____-__-__'),
        user_id    INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id       INTEGER NOT NULL,
        stock_item_id  INTEGER NOT NULL,
        quantity       INTEGER NOT NULL CHECK (quantity > 0),
        price_at_order REAL    NOT NULL CHECK (price_at_order > 0),
        FOREIGN KEY (order_id)      REFERENCES orders(order_id)           ON DELETE CASCADE,
        FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id) ON DELETE RESTRICT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        log_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT    NOT NULL,
        operation  TEXT    NOT NULL,
        record_id  INTEGER,
        user_login TEXT,
        log_time   TEXT    NOT NULL DEFAULT (datetime('now'))
    );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role_id            ON users(role_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_items_product_id   ON stock_items(product_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_items_size_id      ON stock_items(size_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id           ON orders(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id     ON order_items(order_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_stock_item_id ON order_items(stock_item_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_name            ON products(product_name);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_price           ON products(price);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category        ON products(category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_date              ON orders(order_date);")

    conn.commit()


def main():
    os.makedirs('db', exist_ok=True)
    if os.path.exists(DB_PATH):
        print("База данных уже существует:", DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn)
        print("[OK] База данных создана:", DB_PATH)
    finally:
        conn.close()


if __name__ == '__main__':
    main()