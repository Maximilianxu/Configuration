DROP TABLE IF EXISTS c_order;
CREATE TABLE c_order(
    id INT AUTO_INCREMENT,
    user_email VARCHAR(64),
    product_id INT,
    assignments TEXT,
    order_date DATE,
    price FLOAT,
    order_state VARCHAR(4),
    PRIMARY KEY(id)
);