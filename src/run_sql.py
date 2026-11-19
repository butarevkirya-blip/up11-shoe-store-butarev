import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'shoe_store.sqlite')


def run_file(path):
    if not os.path.exists(path):
        print("Файл не найден:", path)
        return
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    with open(path, 'r', encoding='utf-8') as f:
        sql = f.read()
    try:
        conn.executescript(sql)
        conn.commit()
        print("[OK] Выполнен:", path)
    except sqlite3.Error as e:
        print("[ERROR]", e)
    finally:
        conn.close()


def main():
    print("1 - queries_day6.sql")
    print("2 - queries_day7.sql")
    print("3 - queries_day8.sql")
    print("4 - views_indexes.sql")
    print("5 - triggers.sql")
    choice = input("Номер: ").strip()
    mapping = {
        '1': os.path.join(BASE_DIR, 'queries', 'queries_day6.sql'),
        '2': os.path.join(BASE_DIR, 'queries', 'queries_day7.sql'),
        '3': os.path.join(BASE_DIR, 'queries', 'queries_day8.sql'),
        '4': os.path.join(BASE_DIR, 'db', 'views_indexes.sql'),
        '5': os.path.join(BASE_DIR, 'db', 'triggers.sql'),
    }
    if choice in mapping:
        run_file(mapping[choice])
    else:
        print("Неверный выбор")


if __name__ == '__main__':
    main()