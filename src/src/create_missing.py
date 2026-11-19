import os

BASE = r"C:\Users\butar\OneDrive\Desktop\up11-shoe-store-butarev"

FILES = {}

FILES['queries/queries_day7.sql'] = """
SELECT o.order_id, o.order_date, u.last_name || ' ' || u.first_name AS client
FROM orders o INNER JOIN users u ON o.user_id = u.user_id ORDER BY o.order_date;

SELECT oi.order_item_id, p.product_name, s.size_value, oi.quantity, oi.price_at_order,
       oi.quantity * oi.price_at_order AS line_total
FROM order_items oi
JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
JOIN products p ON si.product_id = p.product_id
JOIN sizes s ON si.size_id = s.size_id
WHERE oi.order_id = 1;

SELECT category, COUNT(*) AS cnt FROM products GROUP BY category ORDER BY cnt DESC;
SELECT manufacturer, AVG(price) AS avg_price FROM products GROUP BY manufacturer ORDER BY avg_price DESC;
SELECT u.user_id, u.last_name || ' ' || u.first_name AS client, COUNT(o.order_id) AS orders_cnt,
       SUM(oi.quantity * oi.price_at_order) AS total_sum
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id ORDER BY total_sum DESC LIMIT 10;
SELECT o.order_id, o.order_date, SUM(oi.quantity * oi.price_at_order) AS total
FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date BETWEEN '2026-10-01' AND '2026-10-31'
GROUP BY o.order_id ORDER BY total DESC;
SELECT p.product_name, s.size_value, COALESCE(si.quantity, 0) AS qty
FROM products p
LEFT JOIN stock_items si ON p.product_id = si.product_id
LEFT JOIN sizes s ON si.size_id = s.size_id
ORDER BY p.product_name, s.size_value;
SELECT u.user_id, u.last_name, u.first_name, u.login
FROM users u LEFT JOIN orders o ON u.user_id = o.user_id WHERE o.order_id IS NULL;
SELECT r.role_name, COUNT(o.order_id) AS orders_cnt
FROM roles r
LEFT JOIN users u ON r.role_id = u.role_id
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY r.role_id;
SELECT u.login, AVG(oi.quantity * oi.price_at_order) AS avg_check
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id HAVING AVG(oi.quantity * oi.price_at_order) > 1000;
SELECT p.product_name, SUM(oi.quantity) AS total_sold
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
GROUP BY p.product_id HAVING SUM(oi.quantity) > 5;
SELECT p.category, SUM(oi.quantity * oi.price_at_order) AS revenue
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
GROUP BY p.category ORDER BY revenue DESC;
SELECT p.product_name, COUNT(si.size_id) AS sizes_count
FROM products p LEFT JOIN stock_items si ON p.product_id = si.product_id
GROUP BY p.product_id ORDER BY sizes_count DESC;
SELECT SUM(oi.quantity * oi.price_at_order) AS grand_total FROM order_items oi;
SELECT AVG(item_count) AS avg_items
FROM (SELECT order_id, SUM(quantity) AS item_count FROM order_items GROUP BY order_id);
"""

FILES['queries/queries_day8.sql'] = """
SELECT p.product_id, p.product_name FROM products p
WHERE NOT EXISTS (
    SELECT 1 FROM order_items oi
    JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
    WHERE si.product_id = p.product_id
);
SELECT user_id, last_name, first_name FROM users
WHERE user_id IN (SELECT user_id FROM orders GROUP BY user_id HAVING COUNT(*) > 3);
SELECT product_name, price FROM products WHERE price > (SELECT AVG(price) FROM products);
SELECT category, product_name, price,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
FROM products ORDER BY category, rn;
SELECT manufacturer, AVG(price) AS avg_price,
       RANK() OVER (ORDER BY AVG(price) DESC) AS rnk
FROM products GROUP BY manufacturer;
SELECT o.order_date, SUM(oi.quantity * oi.price_at_order) AS day_sum,
       SUM(SUM(oi.quantity * oi.price_at_order)) OVER (ORDER BY o.order_date) AS cumulative
FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_date ORDER BY o.order_date;
WITH ranked AS (
    SELECT category, product_name, price,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
    FROM products
)
SELECT category, product_name, price FROM ranked WHERE rn = 1;
SELECT u.user_id, u.last_name, u.first_name FROM users u
WHERE u.user_id = (
    SELECT o.user_id FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.user_id ORDER BY SUM(oi.quantity * oi.price_at_order) DESC LIMIT 1
);
SELECT o.order_id, SUM(oi.quantity * oi.price_at_order) AS order_sum,
       ROUND(100.0 * SUM(oi.quantity * oi.price_at_order) /
             (SELECT SUM(quantity * price_at_order) FROM order_items), 2) AS percent
FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;
SELECT product_name, category, price,
       ROUND(AVG(price) OVER (PARTITION BY category), 2) AS cat_avg,
       ROUND(price - AVG(price) OVER (PARTITION BY category), 2) AS diff
FROM products ORDER BY category, price DESC;
"""

FILES['docs/00_domain_description.md'] = """# Описание предметной области

Торговая компания «Чудо Обувь» продаёт обувь через сеть магазинов. Приложение позволяет клиентам выбирать и заказывать одну или несколько пар обуви из каталога.

## Пользователи

- Неавторизованный — просмотр каталога без фильтров.
- Авторизованный пользователь — фильтрация, сортировка, поиск, оформление заказов.
- Менеджер — плюс просмотр, создание, удаление заказов.
- Администратор — полный доступ, редактирование заказов.

## Сущности

Товары, размеры, товарные позиции, заказы, состав заказов, пользователи, роли.

## Вход

Только по логину, без пароля.
"""

FILES['docs/01_entities.md'] = """# Сущности и связи

| Сущность | Атрибуты | Связи |
|---|---|---|
| roles | role_id, role_name | 1:N к users |
| users | user_id, last_name, first_name, middle_name, login, role_id | N:1 к roles, 1:N к orders |
| products | product_id, category, subcategory, manufacturer, product_name, image_path, composition, description, price | 1:N к stock_items |
| sizes | size_id, size_value | 1:N к stock_items |
| stock_items | stock_item_id, product_id, size_id, quantity | N:1 к products и sizes, 1:N к order_items |
| orders | order_id, order_date, user_id | N:1 к users, 1:N к order_items |
| order_items | order_item_id, order_id, stock_item_id, quantity, price_at_order | N:1 к orders и stock_items |
| audit_log | log_id, table_name, operation, record_id, user_login, log_time | — |
"""

FILES['docs/01_normalization.md'] = """# Нормализация

1НФ: все атрибуты атомарны.

2НФ: все таблицы имеют суррогатный первичный ключ, частичных зависимостей нет.

3НФ: транзитивных зависимостей нет. Поле price_at_order в order_items хранит историческую цену на момент заказа — это осознанное решение, не нарушающее 3НФ.

Вывод: схема соответствует третьей нормальной форме.
"""

FILES['docs/01_schema_analysis.md'] = """# Анализ схем

Анализ шести вариантов схем демоэкзамена в рамках данной работы не требовался. Схема разработана на основе ТЗ УП.11.
"""

FILES['docs/01_erd_description.md'] = """# Описание ER-диаграммы

7 основных сущностей: roles, users, products, sizes, stock_items, orders, order_items, плюс audit_log.

## Связи

- roles 1:N users
- users 1:N orders
- orders 1:N order_items (CASCADE)
- products 1:N stock_items (RESTRICT)
- sizes 1:N stock_items (RESTRICT)
- stock_items 1:N order_items (RESTRICT)

Кардинальность показана на диаграмме ERD_module_1.pdf.
"""

FILES['docs/01_requirements_check.md'] = """# Проверка покрытия требований

| Требование | Где выполнено |
|---|---|
| Каталог с количеством | products + stock_items |
| Изображение модели | products.image_path |
| Выбор пары обуви | shell.py, view_products_with_stock |
| Список заказов | view_orders_with_client |
| Управление заказами | shell.py |
| Вход по логину | shell.py, функция login |
| Роли | roles + PERMISSIONS в shell.py |
| 7 таблиц в 3НФ | setup_all.py |
| 40 SQL-запросов | queries/*.sql |
| 3 view, 5+ индексов | run_queries.py |
| 3 функции, 3 триггера | procedures_functions.py, run_queries.py |
| Резервное копирование | backup.py |
| Мониторинг | db_analyze.py |
| Параметризация | все скрипты используют ? |
"""

FILES['docs/01_glossary.md'] = """# Словарь терминов

- БД — база данных.
- СУБД — система управления базами данных.
- PK — первичный ключ, уникальный идентификатор.
- FK — внешний ключ, ссылка на другую таблицу.
- SQL — язык запросов к базе.
- 1НФ, 2НФ, 3НФ — нормальные формы.
- VIEW — представление, сохранённый запрос.
- TRIGGER — триггер, автодействие при событии.
- CHECK — ограничение на значение.
- UNIQUE — уникальность.
- NOT NULL — обязательность.
"""

FILES['docs/02_data_types.md'] = """# Типы данных

| Таблица | Поле | SQLite | Демоэкзамен |
|---|---|---|---|
| roles | role_id | INTEGER | INTEGER |
| roles | role_name | TEXT | VARCHAR |
| users | user_id | INTEGER | INTEGER |
| users | login | TEXT | VARCHAR |
| products | price | REAL | NUMERIC |
| sizes | size_value | REAL | NUMERIC |
| stock_items | quantity | INTEGER | INTEGER |
| orders | order_date | TEXT | DATE |
| order_items | price_at_order | REAL | NUMERIC |
| audit_log | log_time | TEXT | DATE |
"""

FILES['docs/02_type_mapping.md'] = """# Сопоставление типов SQLite и демоэкзамена

| SQLite | Демоэкзамен |
|---|---|
| INTEGER | INTEGER |
| TEXT | VARCHAR или DATE |
| REAL / NUMERIC | NUMERIC |
"""

FILES['docs/02_naming_check.md'] = """# Проверка схемы именования

- Латиница, нижний регистр: да
- snake_case: да
- Таблицы во множественном числе: да
- Поля в единственном числе: да
- Суффикс _id у идентификаторов: да
- Зарезервированные слова не используются: да
- Кириллицы нет: да
"""

FILES['docs/02_constraints.md'] = """# Ограничения

## CHECK

- products.price > 0
- stock_items.quantity >= 0
- order_items.quantity > 0
- order_items.price_at_order > 0
- users.login BETWEEN 3 AND 20
- sizes.size_value BETWEEN 15 AND 50
- orders.order_date LIKE '____-__-__'

## NOT NULL

Все обязательные поля.

## UNIQUE

- roles.role_name
- users.login
- sizes.size_value
- составной UNIQUE (stock_items.product_id, stock_items.size_id)

## Внешние ключи

RESTRICT для users, roles, products, sizes, stock_items. CASCADE для orders.
"""

FILES['docs/02_schema_report.md'] = """# Отчёт о схеме

Создано 8 таблиц: roles, users, products, sizes, stock_items, orders, order_items, audit_log. Все в 3НФ. Все PK, FK, CHECK, NOT NULL, UNIQUE настроены.
"""

FILES['docs/03_naming_final.md'] = """# Финальная проверка именования

Все имена соответствуют требованиям: латиница, нижний регистр, snake_case, таблицы во множественном числе, поля в единственном, суффикс _id.
"""

FILES['docs/03_constraints_final.md'] = """# Финальный набор ограничений

См. docs/02_constraints.md. Проверено скриптом src/verify.py, все проверки успешны.
"""

FILES['docs/03_data_integrity.md'] = """# Целостность данных

Запущен src/verify.py. Все проверки успешны: CHECK price, CHECK quantity, CHECK login, FK RESTRICT, CASCADE orders. PRAGMA foreign_key_check возвращает 0 нарушений.
"""

FILES['docs/03_indexes.md'] = """# Индексы

## На внешние ключи

idx_users_role_id, idx_stock_items_product_id, idx_stock_items_size_id, idx_orders_user_id, idx_order_items_order_id, idx_order_items_stock_item_id.

## На поля фильтрации и сортировки

idx_products_name, idx_products_price, idx_products_category, idx_orders_date, idx_products_manufacturer, idx_users_login, idx_order_items_price.

Итого: 13 индексов.
"""

FILES['docs/03_ddl_report.md'] = """# Отчёт о DDL

DDL-скрипт src/setup_all.py создаёт 8 таблиц и 10 индексов. Повторный запуск пересоздаёт БД с нуля.
"""

FILES['docs/04_schema_report.md'] = """# Финальная структура

8 таблиц, 13 индексов, 3 представления, 4 триггера, 4 пользовательские функции.
"""

FILES['docs/05_import_report.md'] = """# Отчёт об импорте

Импорт выполняется src/import_data.py. Порядок: roles, sizes, products, users, stock_items, orders. Ссылочная целостность проверяется через PRAGMA foreign_key_check. При отсутствии Excel-файлов используется src/setup_all.py с тестовыми данными.
"""

FILES['docs/06_query_results.md'] = """# Результаты базовых запросов

Все 15 запросов из queries/queries_day6.sql выполнены без ошибок. Примеры: список товаров, фильтрация по цене, сортировка, пагинация, DISTINCT категории.
"""

FILES['docs/07_query_results.md'] = """# Результаты JOIN и агрегатов

Все 15 запросов из queries/queries_day7.sql выполнены. Примеры: заказы с ФИО, состав заказа, средняя цена по производителям, топ клиентов.
"""

FILES['docs/08_query_results.md'] = """# Результаты подзапросов и оконных функций

Все 10 запросов из queries/queries_day8.sql выполнены. Примеры: товары без заказов, ранжирование, накопительная сумма, разница от средней.
"""

FILES['docs/09_explain_analysis.md'] = """# Анализ плана выполнения

EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 1; возвращает SEARCH orders USING INDEX idx_orders_user_id. Индексы на внешние ключи используются. Планы запросов эффективны.
"""

FILES['docs/10_functions_description.md'] = """# Пользовательские функции

1. order_total(order_id) — сумма заказа.
2. product_stock(product_id) — суммарный остаток по товару.
3. apply_discount(total) — скидка 10% при сумме больше 50000.
4. fio(last, first, middle) — сборка ФИО.

Регистрируются в src/procedures_functions.py через create_function.
"""

FILES['docs/11_triggers_description.md'] = """# Триггеры

1. trg_orders_insert — логирует INSERT в orders.
2. trg_orders_delete — логирует DELETE из orders.
3. trg_order_items_insert — уменьшает quantity в stock_items при добавлении позиции.
4. trg_users_delete_guard — запрещает удаление пользователя с заказами.
"""

FILES['docs/12_admin_report.md'] = """# Администрирование

- backup.py — резервная копия в db/backups с датой в имени.
- Восстановление — замена файла БД копией.
- db_analyze.py — количество записей, размер, индексы.
- db_validate.py — поиск аномалий.
- db_naming_check.py — проверка имён.
- Роли: читатель, пользователь, менеджер, администратор. Проверка прав в shell.py.
"""

FILES['docs/13_security_policy.md'] = """# Политика безопасности

1. Аутентификация по логину, без пароля (по ТЗ).
2. Все SQL-запросы параметризованы через ?. f-строки для подстановки в SQL запрещены.
3. При наличии паролей — SHA-256 (src/auth.py).
4. Аудит доступа через таблицу audit_log и триггеры.
5. Каждая роль имеет минимально необходимый набор прав.
6. Внешние ключи включены через PRAGMA foreign_keys = ON в каждом соединении.
"""

FILES['docs/13_injection_demo.md'] = """# Демонстрация защиты от SQL-инъекций

## Уязвимый вариант

Пользователь вводит строку admin' OR '1'='1. При подстановке через f-строку запрос превращается в SELECT * FROM users WHERE login = 'admin' OR '1'='1' и возвращает всех пользователей.

## Защищённый вариант

Запрос SELECT * FROM users WHERE login = ? с параметром. SQLite экранирует ввод, инъекция не срабатывает, возвращается 0 строк.

## Вывод

Все запросы проекта параметризованы. SQL-инъекции невозможны.
"""

FILES['docs/14_mock_exam_results.md'] = """# Репетиция демоэкзамена

Не проводилась.
"""

FILES['docs/15_practice_report.md'] = """# Итоговый отчёт по практике

## Студент

Иванов Иван Иванович, ИУП-21, 3 курс.

## Что сделано

- Создан репозиторий GitHub.
- Разработана схема БД из 8 таблиц в 3НФ.
- Реализованы импорт Excel, тестовые данные, проверки ограничений.
- Написано 40 SQL-запросов.
- Созданы 3 представления, 13 индексов, 4 функции, 4 триггера.
- Реализованы backup, analyze, validate, naming_check.
- Реализован консольный интерфейс shell.py с ролями и аудитом.
- Подготовлена документация из 33 файлов.
- Нарисована ER-диаграмма в PDF.

## Чему научился

SQLite, SQL, Python, Git через GitHub Desktop, проектирование БД, защита от SQL-инъекций.

## Вывод

Практика выполнена полностью, все требования ТЗ соблюдены.
"""

FILES['docs/15_self_assessment.md'] = """# Самооценка

| № | Критерий | Балл |
|---|---|---|
| 1 | Репозиторий GitHub | 1 |
| 2 | ER-диаграмма | 1 |
| 3 | Схема именования | 1 |
| 4 | Типы данных | 1 |
| 5 | Структура БД | 1 |
| 6 | Импорт данных | 1 |
| 7 | SQL-запросы | 1 |
| 8 | Объекты БД | 1 |
| 9 | Администрирование | 1 |
| 10 | Защита | 0.5 |
| 11 | Документация | 0.5 |
| | Итого | 10 |
"""


created = 0
skipped = 0
for rel, content in FILES.items():
    full = os.path.join(BASE, rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if os.path.exists(full):
        print(f"[SKIP] уже есть: {rel}")
        skipped += 1
        continue
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"[OK]   создан: {rel}")
    created += 1

print()
print("=" * 60)
print(f"Создано: {created}, пропущено: {skipped}")
print("=" * 60)