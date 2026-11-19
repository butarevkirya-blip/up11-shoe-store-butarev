SELECT * FROM products;

SELECT product_name, price FROM products;

SELECT product_name, price FROM products WHERE price > 10000;

SELECT product_name, manufacturer, price FROM products WHERE category = 'кроссовки';

SELECT product_name, price FROM products WHERE manufacturer = 'Nike';

SELECT product_name, price FROM products ORDER BY price DESC;

SELECT manufacturer, product_name, price FROM products ORDER BY manufacturer ASC, price ASC;

SELECT product_name, price FROM products ORDER BY price DESC LIMIT 5;

SELECT product_name, price FROM products ORDER BY product_id LIMIT 5 OFFSET 5;

SELECT DISTINCT category FROM products;

SELECT DISTINCT manufacturer FROM products ORDER BY manufacturer;

SELECT DISTINCT category, subcategory FROM products ORDER BY category, subcategory;

SELECT user_id, last_name, first_name, login FROM users WHERE login = 'admin';

SELECT order_id, order_date, user_id FROM orders WHERE order_date BETWEEN '2026-10-01' AND '2026-10-31' ORDER BY order_date;

SELECT product_name, price FROM products WHERE price BETWEEN 5000 AND 12000 ORDER BY price;