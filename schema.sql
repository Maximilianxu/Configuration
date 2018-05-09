DROP TABLE IF EXISTS c_user;
CREATE TABLE c_user(
    email VARCHAR(64),
    name VARCHAR(16) UNIQUE,
    password VARCHAR(32),
    role TINYINT,
    company VARCHAR(64),
    profession VARCHAR(64),
    PRIMARY KEY(email)
);

DROP TABLE IF EXISTS c_order;
CREATE TABLE c_order(
    id INT AUTO_INCREMENT,
    user_email VARCHAR(64),
    product_id INT,
    assignments TEXT,
    order_date DATE,
    price FLOAT,
    order_state VARCHAR(4),
    PRIMARY KEY(id),
    FOREIGN KEY (user_email) REFERENCES c_user(email)
);

DROP TABLE IF EXISTS product;
CREATE TABLE product(
    id INT AUTO_INCREMENT,
    user_email VARCHAR(64),
    name VARCHAR(64),
    introduction TEXT,
    is_release TINYINT,
    deadline DATETIME,
    root_component_id INT,
    PRIMARY KEY(id),
    FOREIGN KEY(user_email) REFERENCES c_user(email)
);

DROP TABLE IF EXISTS component;
CREATE TABLE component(
    id INT AUTO_INCREMENT,
    product_id INT,
    father_component_id INT,
    name VARCHAR(64),
    introduction TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(product_id) REFERENCES product(id)
);

DROP TABLE IF EXISTS property;
CREATE TABLE property(
    id INT AUTO_INCREMENT,
    component_id INT,
    name VARCHAR(64),
    introduction TEXT,
    datatype VARCHAR(32),
    dataunit VARCHAR(32),
    domin TEXT,
    domin_display TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(component_id) REFERENCES component(id)
);

DROP TABLE IF EXISTS c_constraint;
CREATE TABLE c_constraint(
    id INT AUTO_INCREMENT,
    product_id INT,
    expression VARCHAR(128),
    PRIMARY KEY(id),
    FOREIGN KEY(product_id) REFERENCES product(id)
);

DROP TABLE IF EXISTS con_include_p;
CREATE TABLE con_include_p(
    constraint_id INT,
    property_id INT
);