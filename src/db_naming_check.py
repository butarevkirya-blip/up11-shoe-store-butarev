import sqlite3
import os
import re

DB_PATH = os.path.join('db', 'shoe_store.sqlite')
RESERVED = {'order', 'select', 'from', 'where', 'index', 'table', 'column'}


def check():
    conn = sqlite3.connect(DB_PATH)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )]
    for t in tables:
        ok = bool(re.fullmatch(r'[a-z][a-z0-9_]*', t)) and t not in RESERVED
        print(f"[{'OK' if ok else 'FAIL'}] table: {t}")
    for t in tables:
        for col in conn.execute(f"PRAGMA table_info({t})").fetchall():
            name = col[1]
            ok = bool(re.fullmatch(r'[a-z][a-z0-9_]*', name)) and name not in RESERVED
            print(f"[{'OK' if ok else 'FAIL'}] {t}.{name}")
    conn.close()


if __name__ == '__main__':
    check()