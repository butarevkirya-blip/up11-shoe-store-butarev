# Описание ER-диаграммы

7 основных сущностей: roles, users, products, sizes, stock_items, orders, order_items, плюс audit_log.

## Связи

- roles 1:N users
- users 1:N orders
- orders 1:N order_items (CASCADE)
- products 1:N stock_items (RESTRICT)
- sizes 1:N stock_items (RESTRICT)
- stock_items 1:N order_items (RESTRICT)

Кардинальность показана на диаграмме ERD_module_1.pdf.
