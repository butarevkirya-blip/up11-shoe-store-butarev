# Сущности и связи

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
