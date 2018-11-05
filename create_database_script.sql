CREATE TABLE author
(
    author_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL
);
CREATE UNIQUE INDEX author_author_id_uindex ON author (author_id);
INSERT INTO author (author_id, first_name, last_name) VALUES (1, 'J.K.', 'Rowling');
INSERT INTO author (author_id, first_name, last_name) VALUES (2, 'Ramez', 'Elmasri');
INSERT INTO author (author_id, first_name, last_name) VALUES (3, 'Shamkant', 'Navathe');
CREATE TABLE author_book
(
    author_id int(11),
    book_id int(11),
    CONSTRAINT fk_author_book_author FOREIGN KEY (author_id) REFERENCES author (author_id),
    CONSTRAINT fk_author_book_book FOREIGN KEY (book_id) REFERENCES book (book_id)
);
CREATE INDEX fk_author_book_author ON author_book (author_id);
CREATE INDEX fk_author_book_book ON author_book (book_id);
INSERT INTO author_book (author_id, book_id) VALUES (1, 1);
INSERT INTO author_book (author_id, book_id) VALUES (2, 2);
INSERT INTO author_book (author_id, book_id) VALUES (3, 2);
INSERT INTO author_book (author_id, book_id) VALUES (1, 3);
INSERT INTO author_book (author_id, book_id) VALUES (2, 3);
CREATE TABLE book
(
    book_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    title varchar(50) NOT NULL,
    publisher_id int(11),
    num_in_stock int(11) NOT NULL,
    pages int(11) NOT NULL,
    release_year int(4),
    CONSTRAINT fk_book_publisher FOREIGN KEY (publisher_id) REFERENCES publisher (publisher_id)
);
CREATE UNIQUE INDEX book_book_id_uindex ON book (book_id);
CREATE INDEX fk_book_publisher ON book (publisher_id);
INSERT INTO book (book_id, title, publisher_id, num_in_stock, pages, release_year) VALUES (1, 'Harry Potter', 1, 5, 200, 2010);
INSERT INTO book (book_id, title, publisher_id, num_in_stock, pages, release_year) VALUES (2, 'Fundamentals of Database Systems', 2, 2, 300, 2016);
INSERT INTO book (book_id, title, publisher_id, num_in_stock, pages, release_year) VALUES (3, 'Databases at Hogwarts', 1, 99, 100, 1999);
CREATE TABLE cart
(
    book_id int(11) NOT NULL,
    customer_id int(11) NOT NULL,
    CONSTRAINT `PRIMARY` PRIMARY KEY (book_id, customer_id),
    CONSTRAINT fk_cart_book FOREIGN KEY (book_id) REFERENCES book (book_id),
    CONSTRAINT fk_cart_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);
CREATE INDEX fk_cart_customer ON cart (customer_id);
CREATE TABLE customer
(
    customer_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    first_name varchar(50),
    last_name varchar(50) NOT NULL,
    address varchar(100)
);
CREATE UNIQUE INDEX customer_customer_id_uindex ON customer (customer_id);
INSERT INTO customer (customer_id, first_name, last_name, address) VALUES (1, 'Tyler', 'Carberry', '201 Mullica Hill Road');
CREATE TABLE customer_book
(
    customer_id int(11) NOT NULL,
    book_id int(11) NOT NULL,
    CONSTRAINT `PRIMARY` PRIMARY KEY (customer_id, book_id),
    CONSTRAINT customer_book_ibfk_1 FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    CONSTRAINT customer_book_ibfk_3 FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    CONSTRAINT customer_book_ibfk_2 FOREIGN KEY (book_id) REFERENCES book (book_id),
    CONSTRAINT customer_book_ibfk_4 FOREIGN KEY (book_id) REFERENCES book (book_id)
);
CREATE INDEX book_id ON customer_book (book_id);
CREATE TABLE publisher
(
    publisher_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name varchar(50) NOT NULL
);
CREATE UNIQUE INDEX publisher_publisher_id_uindex ON publisher (publisher_id);
INSERT INTO publisher (publisher_id, name) VALUES (1, 'Bloomsbury Publishing');
INSERT INTO publisher (publisher_id, name) VALUES (2, 'Pearson');
CREATE TABLE rating
(
    product_rating int(11),
    product_id int(11) NOT NULL,
    customer_id int(11) NOT NULL,
    CONSTRAINT `PRIMARY` PRIMARY KEY (product_id, customer_id),
    CONSTRAINT FK_rating_book FOREIGN KEY (product_id) REFERENCES book (book_id)
);
CREATE TABLE restock
(
    restock_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    book_id int(11) NOT NULL,
    amount int(11) NOT NULL,
    CONSTRAINT fk_restock_book FOREIGN KEY (book_id) REFERENCES book (book_id)
);
CREATE UNIQUE INDEX restock_restock_id_uindex ON restock (restock_id);
CREATE UNIQUE INDEX restock_book_id_uindex ON restock (book_id);
CREATE TABLE transaction
(
    transaction_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    transaction_time datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
    customer_id int(11) NOT NULL,
    CONSTRAINT fk_transaction_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);
CREATE UNIQUE INDEX transaction_transaction_id_uindex ON transaction (transaction_id);
CREATE INDEX fk_transaction_customer ON transaction (customer_id);
CREATE TABLE transaction_book
(
    transaction_id int(11) NOT NULL,
    book_id int(11) NOT NULL,
    CONSTRAINT `PRIMARY` PRIMARY KEY (transaction_id, book_id),
    CONSTRAINT fk_transaction_book_transaction FOREIGN KEY (transaction_id) REFERENCES transaction (transaction_id),
    CONSTRAINT fk_transaction_book_book FOREIGN KEY (book_id) REFERENCES book (book_id)
);
CREATE INDEX fk_transaction_book_book ON transaction_book (book_id);
CREATE TABLE wish_list
(
    customer_id int(11) NOT NULL,
    book_id int(11) NOT NULL,
    CONSTRAINT `PRIMARY` PRIMARY KEY (customer_id, book_id),
    CONSTRAINT fk_wish_list_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    CONSTRAINT fk_wish_list_book FOREIGN KEY (book_id) REFERENCES book (book_id)
);
CREATE INDEX fk_wish_list_book ON wish_list (book_id);