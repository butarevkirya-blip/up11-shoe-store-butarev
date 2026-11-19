# Анализ плана выполнения

EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 1; возвращает SEARCH orders USING INDEX idx_orders_user_id. Индексы на внешние ключи используются. Планы запросов эффективны.
