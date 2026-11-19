import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join('db', 'shoe_store.sqlite')
BACKUP_DIR = os.path.join('db', 'backups')


def backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = os.path.join(BACKUP_DIR, f'shoe_store_{ts}.sqlite')
    src = sqlite3.connect(DB_PATH)
    dst = sqlite3.connect(path)
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    print("[OK] Резервная копия:", path)
    return path


def main():
    backup()


if __name__ == '__main__':
    main()