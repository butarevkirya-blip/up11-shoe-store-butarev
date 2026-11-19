import os
import shutil

BASE = r"C:\Users\butar\OneDrive\Desktop\up11-shoe-store-butarev"

if not os.path.isdir(BASE):
    print("[ERROR] Папка проекта не найдена:", BASE)
    raise SystemExit(1)

print("Корень:", BASE)

PY_TARGETS = {
    'setup_all.py', 'run_queries.py', 'shell.py', 'backup.py', 'auth.py',
    'db_analyze.py', 'db_validate.py', 'db_naming_check.py',
    'procedures_functions.py', 'verify.py', 'db_init.py', 'db_seed.py',
    'import_data.py', 'install_deps.py', 'db_test_constraints.py',
    'run_sql.py', 'test_fk.py',
}

SQL_QUERIES = {'queries_day6.sql', 'queries_day7.sql', 'queries_day8.sql'}
SQL_DB = {'views_indexes.sql', 'triggers.sql'}

moved = []
deleted_dupes = []


def dest_for(filename):
    if filename in PY_TARGETS:
        return os.path.join(BASE, 'src', filename)
    if filename in SQL_QUERIES:
        return os.path.join(BASE, 'queries', filename)
    if filename in SQL_DB:
        return os.path.join(BASE, 'db', filename)
    if filename.endswith('.md') and filename not in ('README.md',):
        return os.path.join(BASE, 'docs', filename)
    return None


for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ('.git', 'backups', '__pycache__')]
    if root == BASE:
        continue
    for f in files:
        dest = dest_for(f)
        if not dest:
            continue
        src_full = os.path.join(root, f)
        if os.path.abspath(src_full) == os.path.abspath(dest):
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(dest):
            deleted_dupes.append(src_full)
            os.remove(src_full)
        else:
            shutil.move(src_full, dest)
            moved.append((src_full, dest))

print("\nПЕРЕМЕЩЕНО:", len(moved))
for s, d in moved:
    print(f"  {os.path.relpath(s, BASE)}  ->  {os.path.relpath(d, BASE)}")

print("\nУДАЛЕНО ДУБЛИКАТОВ:", len(deleted_dupes))
for s in deleted_dupes:
    print(f"  {os.path.relpath(s, BASE)}")

print("\nУдаляю пустые вложенные папки...")
for _ in range(10):
    removed_any = False
    for root, dirs, files in os.walk(BASE, topdown=False):
        if root == BASE:
            continue
        rel = os.path.relpath(root, BASE)
        if rel.startswith('.git') or 'backups' in rel:
            continue
        try:
            if not os.listdir(root):
                os.rmdir(root)
                print(f"  удалена пустая: {rel}")
                removed_any = True
        except OSError:
            pass
    if not removed_any:
        break

print("\n" + "=" * 60)
print("ПРОВЕРКА ФАЙЛОВ:")
print("=" * 60)
for rel in ['src/setup_all.py', 'src/run_queries.py', 'src/shell.py',
            'src/backup.py', 'src/auth.py', 'src/procedures_functions.py',
            'queries/queries_day6.sql', 'queries/queries_day7.sql',
            'queries/queries_day8.sql']:
    full = os.path.join(BASE, rel.replace('/', os.sep))
    print(f"  {'[ЕСТЬ]' if os.path.exists(full) else '[НЕТ] '} {rel}")