import os

BASE = r"C:\Users\butar\OneDrive\Desktop\up11-shoe-store-butarev"

if not os.path.isdir(BASE):
    BASE = os.getcwd()

print("=" * 70)
print("КОРЕНЬ:", BASE)
print("=" * 70)

print("\nВСЕ ФАЙЛЫ В ПРОЕКТЕ (кроме .git, без папок):")
print("-" * 70)
total = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d != '.git']
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, BASE)
        try:
            size = os.path.getsize(full)
        except OSError:
            size = -1
        print(f"  {rel:65s} {size:>8} б")
        total += 1
print(f"\nВсего файлов: {total}")

print("\n" + "=" * 70)
print("СОДЕРЖИМОЕ ПАПКИ src:")
print("=" * 70)
src = os.path.join(BASE, 'src')
if os.path.isdir(src):
    items = sorted(os.listdir(src))
    if not items:
        print("  ПУСТО")
    for name in items:
        full = os.path.join(src, name)
        kind = "DIR " if os.path.isdir(full) else "FILE"
        print(f"  [{kind}] {name}")
else:
    print("  ПАПКИ src НЕТ!")

print("\n" + "=" * 70)
print("СОДЕРЖИМОЕ ПАПКИ queries:")
print("=" * 70)
q = os.path.join(BASE, 'queries')
if os.path.isdir(q):
    items = sorted(os.listdir(q))
    if not items:
        print("  ПУСТО")
    for name in items:
        print("  ", name)
else:
    print("  ПАПКИ queries НЕТ!")

print("\n" + "=" * 70)
print("СОДЕРЖИМОЕ ПАПКИ docs:")
print("=" * 70)
d = os.path.join(BASE, 'docs')
if os.path.isdir(d):
    items = sorted(os.listdir(d))
    if not items:
        print("  ПУСТО")
    for name in items:
        print("  ", name)
else:
    print("  ПАПКИ docs НЕТ!")

print("\n" + "=" * 70)
print("ЧТО ИЩЕТ ПРОВЕРКА (полные пути):")
print("=" * 70)
expected = [
    'src/setup_all.py', 'src/run_queries.py', 'src/shell.py',
    'src/backup.py', 'src/auth.py',
    'queries/queries_day6.sql', 'queries/queries_day7.sql',
    'docs/00_domain_description.md', 'docs/ERD_module_1.pdf',
]
for rel in expected:
    full = os.path.join(BASE, rel.replace('/', os.sep))
    print(f"  {'[ЕСТЬ]' if os.path.exists(full) else '[НЕТ] '} {full}")