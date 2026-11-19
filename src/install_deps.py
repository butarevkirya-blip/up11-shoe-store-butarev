import subprocess
import sys

print("Устанавливаю зависимости...")
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
print("[OK] Готово")