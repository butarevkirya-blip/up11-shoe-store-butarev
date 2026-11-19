import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Папка проекта (BASE_DIR):")
print(BASE_DIR)
print("=" * 60)

print("\nСодержимое корня проекта:")
for name in sorted(os.listdir(BASE_DIR)):
    full = os.path.join(BASE_DIR, name)
    kind = "DIR " if os.path.isdir(full) else "FILE"
    print(f"  [{kind}] {name}")

print("\nСодержимое папки queries:")
queries_dir = os.path.join(BASE_DIR, 'queries')
if os.path.isdir(queries_dir):
    files = os.listdir(queries_dir)
    if not files:
        print("  ПАПКА ПУСТАЯ!")
    for name in sorted(files):
        print(f"  {repr(name)}")
else:
    print("  ПАПКИ queries НЕТ!")

print("\nВсе .sql файлы во всём проекте:")
for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root:
        continue
    for f in files:
        if f.endswith('.sql') or 'queries' in f.lower() or f.endswith('.sql.txt'):
            print("  ", os.path.join(root, f))

print("\nСодержимое папки src:")
src_dir = os.path.join(BASE_DIR, 'src')
for name in sorted(os.listdir(src_dir)):
    print("  ", name)

print("\nСодержимое папки db:")
db_dir = os.path.join(BASE_DIR, 'db')
if os.path.isdir(db_dir):
    for name in sorted(os.listdir(db_dir)):
        print("  ", name)
else:
    print("  ПАПКИ db НЕТ!")
print("=" * 60)