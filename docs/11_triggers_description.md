# Триггеры

1. trg_orders_insert — логирует INSERT в orders.
2. trg_orders_delete — логирует DELETE из orders.
3. trg_order_items_insert — уменьшает quantity в stock_items при добавлении позиции.
4. trg_users_delete_guard — запрещает удаление пользователя с заказами.
