import os
import sqlite3


def find_project_root():
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, 'src')):
        return cwd
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(current, 'src')):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = find_project_root()
DB_PATH = os.path.join(BASE_DIR, 'db', 'shoe_store.sqlite')

ok_count = 0
fail_count = 0
fail_messages = []


def check(label, condition, details=""):
    global ok_count, fail_count
    if condition:
        ok_count += 1
        suffix = f" {details}" if details else ""
        print(f"[OK]   {label}{suffix}")
    else:
        fail_count += 1
        suffix = f" {details}" if details else ""
        msg = f"{label}{suffix}"
        fail_messages.append(msg)
        print(f"[FAIL] {label}{suffix}")


print("=" * 70)
print("ПРОВЕРКА ПРОЕКТА УП.11 — «Чудо Обувь»")
print("=" * 70)
print("Корень проекта:", BASE_DIR)
print("Файл БД:      ", DB_PATH)
print("=" * 70)

# ========== БЛОК 1: ПАПКИ И КОРНЕВЫЕ ФАЙЛЫ ==========
print("\n[БЛОК 1] Папки и корневые файлы")
print("-" * 70)
check("Папка db/", os.path.isdir(os.path.join(BASE_DIR, 'db')))
check("Папка db/backups/", os.path.isdir(os.path.join(BASE_DIR, 'db', 'backups')))
check("Папка docs/", os.path.isdir(os.path.join(BASE_DIR, 'docs')))
check("Папка queries/", os.path.isdir(os.path.join(BASE_DIR, 'queries')))
check("Папка src/", os.path.isdir(os.path.join(BASE_DIR, 'src')))
check("Файл .gitignore", os.path.exists(os.path.join(BASE_DIR, '.gitignore')))
check("Файл README.md", os.path.exists(os.path.join(BASE_DIR, 'README.md')))
check("Файл requirements.txt", os.path.exists(os.path.join(BASE_DIR, 'requirements.txt')))
check("Файл БД shoe_store.sqlite", os.path.exists(DB_PATH))

# ========== БЛОК 2: SQL-ФАЙЛЫ ==========
print("\n[БЛОК 2] SQL-файлы (queries/ и db/)")
print("-" * 70)
for f in ['queries_day6.sql', 'queries_day7.sql', 'queries_day8.sql']:
    check(f"queries/{f}", os.path.exists(os.path.join(BASE_DIR, 'queries', f)))
for f in ['views_indexes.sql', 'triggers.sql']:
    path = os.path.join(BASE_DIR, 'db', f)
    if os.path.exists(path):
        check(f"db/{f}", True)
    else:
        print(f"[INFO] db/{f} отсутствует (не критично, SQL уже в run_queries.py)")

# ========== БЛОК 3: PYTHON-СКРИПТЫ ==========
print("\n[БЛОК 3] Python-скрипты (src/)")
print("-" * 70)
for f in ['setup_all.py', 'run_queries.py', 'shell.py', 'backup.py',
          'db_analyze.py', 'db_validate.py', 'db_naming_check.py',
          'procedures_functions.py', 'auth.py']:
    check(f"src/{f}", os.path.exists(os.path.join(BASE_DIR, 'src', f)))

# ========== БЛОК 4: ДОКУМЕНТАЦИЯ ==========
print("\n[БЛОК 4] Ключевые файлы docs/")
print("-" * 70)
for f in ['ERD_module_1.pdf', 'ERD_module_1.drawio',
          '00_domain_description.md', '01_normalization.md',
          '13_security_policy.md', '15_practice_report.md']:
    check(f"docs/{f}", os.path.exists(os.path.join(BASE_DIR, 'docs', f)))

# Если БД нет — дальше проверять нечего
if not os.path.exists(DB_PATH):
    print("\n" + "=" * 70)
    print(f"ИТОГО: OK={ok_count}, FAIL={fail_count}")
    print("БД отсутствует. Запусти src/setup_all.py и повтори.")
    print("=" * 70)
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")

# ========== БЛОК 5: ТАБЛИЦЫ ==========
print("\n[БЛОК 5] Таблицы в БД")
print("-" * 70)
tables = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
)]
print("  Найдено:", tables)
required_tables = ['roles', 'users', 'products', 'sizes',
                   'stock_items', 'orders', 'order_items', 'audit_log']
for t in required_tables:
    check(f"Таблица {t}", t in tables)
check("Всего таблиц >= 8", len(tables) >= 8, f"(найдено {len(tables)})")

# ========== БЛОК 6: ДАННЫЕ ==========
print("\n[БЛОК 6] Данные в таблицах")
print("-" * 70)
minimums = {
    'roles': 4, 'users': 6, 'products': 6, 'sizes': 11,
    'stock_items': 60, 'orders': 15, 'order_items': 15,
}
for table, minimum in minimums.items():
    try:
        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        check(f"{table}: {n} записей", n >= minimum, f"(минимум {minimum})")
    except sqlite3.Error as e:
        check(f"{table}: чтение", False, f"({e})")

# ========== БЛОК 7: ПРЕДСТАВЛЕНИЯ ==========
print("\n[БЛОК 7] Представления (VIEW)")
print("-" * 70)
views = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name"
)]
for v in ['view_orders_with_client', 'view_products_with_stock', 'view_top_clients']:
    check(f"VIEW {v}", v in views)
for v in views:
    try:
        n = conn.execute(f"SELECT COUNT(*) FROM {v}").fetchone()[0]
        print(f"       {v}: {n} строк")
    except sqlite3.Error as e:
        check(f"{v}: чтение", False, f"({e})")

# ========== БЛОК 8: ИНДЕКСЫ ==========
print("\n[БЛОК 8] Индексы")
print("-" * 70)
indexes = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
)]
check(f"Индексов >= 10", len(indexes) >= 10, f"(найдено {len(indexes)})")
print("  Примеры:", sorted(indexes)[:5], "...")

# ========== БЛОК 9: ТРИГГЕРЫ + РЕАЛЬНЫЙ ТЕСТ ==========
print("\n[БЛОК 9] Триггеры")
print("-" * 70)
triggers = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='trigger'"
)]
for t in ['trg_orders_insert', 'trg_orders_delete',
          'trg_order_items_insert', 'trg_users_delete_guard']:
    check(f"TRIGGER {t}", t in triggers)

print("\n  Проверка: триггер логирования audit_log")
before = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
cur = conn.execute("INSERT INTO orders (order_date, user_id) VALUES ('2099-01-01', 1)")
test_order_id = cur.lastrowid
conn.commit()
after = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
check("Триггер audit_log срабатывает", after > before, f"(было {before}, стало {after})")
conn.execute("DELETE FROM orders WHERE order_id = ?", (test_order_id,))
conn.commit()
print(f"       (тестовый заказ #{test_order_id} удалён)")

# ========== БЛОК 10: FK RESTRICT (правильный тест) ==========
print("\n[БЛОК 10] FK RESTRICT (нельзя удалить пользователя с заказами)")
print("-" * 70)
row = conn.execute("""
    SELECT u.user_id, u.login, COUNT(o.order_id) AS cnt
    FROM users u
    JOIN orders o ON u.user_id = o.user_id
    GROUP BY u.user_id
    ORDER BY cnt DESC
    LIMIT 1
""").fetchone()

if row:
    uid, login, cnt = row
    print(f"  Тестирую: user_id={uid}, login='{login}', заказов={cnt}")
    try:
        conn.execute("DELETE FROM users WHERE user_id = ?", (uid,))
        check("FK RESTRICT users", False,
              f"(удалось удалить '{login}' с {cnt} заказами!)")
        conn.rollback()
    except sqlite3.IntegrityError:
        check("FK RESTRICT users", True,
              f"(SQLite запретил удаление '{login}' с {cnt} заказами)")
        conn.rollback()
else:
    print("[SKIP] Нет пользователей с заказами — тест невозможен")

# ========== БЛОК 11: FK CASCADE ==========
print("\n[БЛОК 11] FK CASCADE (при удалении заказа удаляются его позиции)")
print("-" * 70)
row = conn.execute("SELECT order_id FROM order_items LIMIT 1").fetchone()
if row:
    oid = row[0]
    before = conn.execute(
        "SELECT COUNT(*) FROM order_items WHERE order_id = ?", (oid,)
    ).fetchone()[0]
    conn.execute("DELETE FROM orders WHERE order_id = ?", (oid,))
    after = conn.execute(
        "SELECT COUNT(*) FROM order_items WHERE order_id = ?", (oid,)
    ).fetchone()[0]
    check("CASCADE order_items", after == 0, f"(было {before}, стало {after})")
    conn.rollback()
else:
    print("[SKIP] Нет order_items — тест невозможен")

# ========== БЛОК 12: CHECK + ЦЕЛОСТНОСТЬ + .GITIGNORE ==========
print("\n[БЛОК 12] CHECK-ограничения, целостность, .gitignore")
print("-" * 70)

print("  CHECK price > 0:")
try:
    conn.execute("""
        INSERT INTO products (category, manufacturer, product_name, price)
        VALUES ('a', 'b', 'c', -1)
    """)
    check("CHECK price > 0", False, "(отрицательная цена прошла!)")
    conn.rollback()
except sqlite3.IntegrityError:
    check("CHECK price > 0", True)

print("  CHECK quantity >= 0:")
try:
    conn.execute("""
        INSERT INTO stock_items (product_id, size_id, quantity)
        VALUES (1, 1, -1)
    """)
    check("CHECK quantity >= 0", False, "(отрицательное количество прошло!)")
    conn.rollback()
except sqlite3.IntegrityError:
    check("CHECK quantity >= 0", True)

print("  CHECK login 3–20:")
try:
    conn.execute("""
        INSERT INTO users (last_name, first_name, login, role_id)
        VALUES ('a', 'b', 'xx', 1)
    """)
    check("CHECK login 3–20", False, "(короткий логин прошёл!)")
    conn.rollback()
except sqlite3.IntegrityError:
    check("CHECK login 3–20", True)

print("\n  PRAGMA foreign_key_check:")
violations = conn.execute("PRAGMA foreign_key_check").fetchall()
check("Целостность FK", len(violations) == 0,
      f"({len(violations)} нарушений)")

print("\n  .gitignore содержит db/shoe_store.sqlite:")
gi_path = os.path.join(BASE_DIR, '.gitignore')
if os.path.exists(gi_path):
    with open(gi_path, encoding='utf-8') as f:
        gi = f.read()
    check(".gitignore исключает БД",
          'db/shoe_store.sqlite' in gi or 'shoe_store.sqlite' in gi)
else:
    check(".gitignore существует", False)

conn.close()

# ========== ИТОГ ==========
print("\n" + "=" * 70)
if fail_count == 0:
    print(f"РЕЗУЛЬТАТ: ВСЁ РАБОТАЕТ  (OK={ok_count}, FAIL=0)")
    print("Проект готов к сдаче.")
else:
    print(f"РЕЗУЛЬТАТ: ЕСТЬ ПРОБЛЕМЫ  (OK={ok_count}, FAIL={fail_count})")
    print("\nСписок проблем:")
    for m in fail_messages:
        print(f"  - {m}")
print("=" * 70)