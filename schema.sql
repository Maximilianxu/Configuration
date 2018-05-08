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

DROP TABLE IF EXISTS expert;
CREATE TABLE expert(
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    company VARCHAR(20),
    profession VARCHAR(20),
    PRIMARY KEY(id)
);