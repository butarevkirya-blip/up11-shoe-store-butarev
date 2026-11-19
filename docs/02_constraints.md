# Ограничения

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
