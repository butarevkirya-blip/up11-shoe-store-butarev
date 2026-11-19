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
