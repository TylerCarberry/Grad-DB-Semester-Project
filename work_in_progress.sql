# Tyler Carberry

create table author
(
  author_id  int auto_increment,
  first_name varchar(50) not null,
  last_name  varchar(50) not null,
  constraint author_author_id_uindex
  unique (author_id)
);

alter table author
  add primary key (author_id);

create table customer
(
  customer_id int auto_increment,
  first_name  varchar(50)  null,
  last_name   varchar(50)  not null,
  address     varchar(100) null,
  constraint customer_customer_id_uindex
  unique (customer_id)
);

alter table customer
  add primary key (customer_id);

create table publisher
(
  publisher_id int auto_increment,
  name         varchar(50) not null,
  constraint publisher_publisher_id_uindex
  unique (publisher_id)
);

alter table publisher
  add primary key (publisher_id);

create table book
(
  book_id      int auto_increment,
  title        varchar(50) not null,
  publisher_id int         null,
  num_in_stock int         not null,
  pages        int         not null,
  release_year int(4)      null,
  constraint book_book_id_uindex
  unique (book_id),
  constraint fk_book_publisher
  foreign key (publisher_id) references publisher (publisher_id)
);

alter table book
  add primary key (book_id);

create table author_book
(
  author_id int null,
  book_id   int null,
  constraint fk_author_book_author
  foreign key (author_id) references author (author_id),
  constraint fk_author_book_book
  foreign key (book_id) references book (book_id)
);

create table cart
(
  book_id     int not null,
  customer_id int not null,
  primary key (book_id, customer_id),
  constraint fk_cart_book
  foreign key (book_id) references book (book_id),
  constraint fk_cart_customer
  foreign key (customer_id) references customer (customer_id)
);

create table restock
(
  restock_id int auto_increment,
  book_id    int not null,
  amount     int not null,
  constraint restock_book_id_uindex
  unique (book_id),
  constraint restock_restock_id_uindex
  unique (restock_id),
  constraint fk_restock_book
  foreign key (book_id) references book (book_id)
);

alter table restock
  add primary key (restock_id);

create table transaction
(
  transaction_id   int auto_increment,
  transaction_time datetime default CURRENT_TIMESTAMP not null,
  customer_id      int                                not null,
  constraint transaction_transaction_id_uindex
  unique (transaction_id),
  constraint fk_transaction_customer
  foreign key (customer_id) references customer (customer_id)
);

alter table transaction
  add primary key (transaction_id);

create table transaction_book
(
  transaction_id int not null,
  book_id        int not null,
  primary key (transaction_id, book_id),
  constraint fk_transaction_book_book
  foreign key (book_id) references book (book_id),
  constraint fk_transaction_book_transaction
  foreign key (transaction_id) references transaction (transaction_id)
);

create table wish_list
(
  customer_id int not null,
  book_id     int not null,
  primary key (customer_id, book_id),
  constraint fk_wish_list_book
  foreign key (book_id) references book (book_id),
  constraint fk_wish_list_customer
  foreign key (customer_id) references customer (customer_id)
);


# List of adventure works customers with first name, last name, email, and address
CREATE OR REPLACE VIEW adventure_customers(first_name, last_name, email, address) AS
SELECT cont.FirstName, cont.LastName, cont.EmailAddress, address.address FROM adventureworks.customer c
  JOIN adventureworks.individual i on c.CustomerID = i.CustomerID
  JOIN adventureworks.contact cont on i.ContactID = cont.ContactID
  JOIN adventureworks.customeraddress ca on ca.CustomerID = c.CustomerID
  JOIN adventure_customers_address address on address.address_id = ca.AddressID;


# List of adventure works full addresses concatenated as a string
CREATE OR REPLACE VIEW adventure_customers_address(address_id, address) AS
SELECT a.AddressID, concat(a.AddressLine1, ifnull(concat(' ', a.AddressLine2), ''), ' ', a.City, ' ', trim(s.StateProvinceCode), ' ', a.PostalCode, ' ', s.CountryRegionCode) FROM adventureworks.customeraddress ca
  JOIN adventureworks.address a ON ca.AddressID = a.AddressID
  JOIN adventureworks.stateprovince s ON s.StateProvinceID = a.StateProvinceID;




# List of sakila customers with first name, last name, email, and address
CREATE OR REPLACE VIEW sakila_customers(first_name, last_name, email, address) AS
SELECT c.first_name, c.last_name, c.email, concat(a.address, ifnull(a.address2, ''), ' ', city.city, ' ', a.district, ' ', a.postal_code, ' ', country.country)
FROM sakila.customer c
JOIN sakila.address a on a.address_id = c.address_id
JOIN sakila.city city on a.city_id = city.city_id
JOIN sakila.country country on city.country_id = country.country_id;


# List of sakila customers with first name, last name, email, and address
CREATE OR REPLACE VIEW northwind_customers(first_name, last_name, email, address) AS
SELECT c.first_name, c.last_name, ifnull(c.email_address, 'unknown email'), concat(c.address, ' ', c.city, ' ', c.state_province, ' ', c.zip_postal_code, ' ', c.country_region) from northwind.customers c
;

SELECT * FROM sakila_customers;

# List of Rowan Books customers with first name, last name, email, and address
CREATE OR REPLACE VIEW rowan_customers(first_name, last_name, email, address) AS
SELECT c.first_name, c.last_name, ifnull(c.email, 'unknown email'), c.address
       FROM carberryt9.customer c
;

SELECT * FROM rowan_customers;


# All customers from sakila, northwind, adventure works
# TODO: Add ours also
CREATE OR REPLACE VIEW all_customers (first_name, last_name, email, address, store) AS
  SELECT first_name, last_name, email, address, 'northwind' FROM northwind_customers
  UNION
  SELECT first_name, last_name, email, address, 'sakila' FROM sakila_customers
  UNION
  SELECT first_name, last_name, email, address, 'adventureworks' FROM adventure_customers
  UNION
  SELECT first_name, last_name, email, address, 'rowan_books' FROM rowan_customers
;

SELECT * FROM all_customers LIMIT 100;






# Products
# The view for northwind products

CREATE OR REPLACE VIEW northwind_products(name, description, category, cost) AS
SELECT p.product_name, ifnull(p.description, ''), p.category, p.standard_cost
FROM northwind.products p;


# Adventure works products
CREATE OR REPLACE VIEW adventure_products(name, description, category, cost) AS
SELECT p.Name, pd.Description, pc.Name, p.ListPrice
FROM adventureworks.product p
JOIN adventureworks.productsubcategory sub ON p.ProductSubcategoryID = sub.ProductSubcategoryID
JOIN adventureworks.productcategory pc on sub.ProductCategoryID = pc.ProductCategoryID
JOIN adventureworks.productmodel pm on pm.ProductModelID = p.ProductModelID
JOIN adventureworks.productmodelproductdescriptionculture longname on longname.ProductModelID = pm.ProductModelID
JOIN adventureworks.productdescription pd on pd.ProductDescriptionID = longname.ProductDescriptionID
  WHERE longname.CultureID = 'en'
;


SELECT * FROM adventure_products;


CREATE OR REPLACE VIEW sakila_products(name, description, category, cost) AS
SELECT f.title, concat(f.rating, ' (', f.length, ' minutes) ', f.description), group_concat(c.name separator '-'), f.replacement_cost
FROM sakila.film f
JOIN sakila.film_category fc on fc.film_id = f.film_id
JOIN sakila.category c on fc.category_id = c.category_id
GROUP BY f.film_id
;

SELECT * FROM sakila_products;


CREATE OR REPLACE VIEW rowan_products(name, description, category, cost) AS
SELECT b.title, b.description, group_concat(g.name separator '-'), b.price
FROM carberryt9.book b
JOIN carberryt9.book_genre bg on b.book_id = bg.book_id
JOIN carberryt9.genre g on g.genre_id = bg.genre_id
GROUP BY b.book_id
;

SELECT * FROM rowan_products;


# All products from sakila, northwind, adventure works
# TODO: Add ours also
CREATE OR REPLACE VIEW all_products (name, description, category, cost, store) AS
  SELECT name, description, category, cost, 'northwind' FROM northwind_products
  UNION
  SELECT name, description, category, cost, 'sakila' FROM sakila_products
  UNION
  SELECT name, description, category, cost, 'adventureworks' FROM adventure_products
  UNION
  SELECT name, description, category, cost, 'rowan' FROM rowan_products
;

SELECT * FROM all_products;






# 7. Ability to generate a restocking order (should be saved in a ”restocking” table) if the supply of any of your products falls below the minimum stock level

DROP TRIGGER IF EXISTS restock_trigger;
CREATE TRIGGER restock_trigger BEFORE UPDATE ON carberryt9.book
  FOR EACH ROW
  BEGIN
    IF new.num_in_stock < (SELECT value_constant from carberryt9.constants c where c.key_constant = 'restock_min') THEN
      SET new.num_in_stock = old.num_in_stock + (SELECT value_constant from carberryt9.constants c where c.key_constant = 'restock_level');
      INSERT INTO restock(book_id, amount) VALUES(new.book_id, (SELECT value_constant from carberryt9.constants c where c.key_constant = 'restock_level'));
    END IF ;
  END;


# add rating and runtime to the description from saquila

# 10. List of all your products whose inventory has fallen below the minimum stock level
SELECT * FROM carberryt9.book WHERE num_in_stock < (SELECT value_constant from carberryt9.constants c where c.key_constant = 'restock_min');

# 11. List of customers who have not been “too active”(you define this) and for whom special offers should be made.
# A not active customer is a customer who has previously placed an order before, but has not placed an order in the past month
SELECT * from carberryt9.customer c1
WHERE
    (SELECT max(t2.transaction_time) most_recent_order
     FROM transaction t2 JOIN customer c2 ON t2.customer_id = c2.customer_id
     WHERE c2.customer_id = c1.customer_id
     GROUP BY c2.customer_id) < now() - 30* 24* 60* 60
