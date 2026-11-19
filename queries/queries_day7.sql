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
