# Отчёт об импорте

Импорт выполняется src/import_data.py. Порядок: roles, sizes, products, users, stock_items, orders. Ссылочная целостность проверяется через PRAGMA foreign_key_check. При отсутствии Excel-файлов используется src/setup_all.py с тестовыми данными.
