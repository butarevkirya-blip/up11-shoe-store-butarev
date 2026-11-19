# Проверка покрытия требований

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
