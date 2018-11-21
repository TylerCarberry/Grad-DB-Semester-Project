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


# All customers from sakila, northwind, adventure works
# TODO: Add ours also
CREATE OR REPLACE VIEW all_customers (first_name, last_name, email, address, store) AS
  SELECT first_name, last_name, email, address, 'northwind' FROM northwind_customers
  UNION
  SELECT first_name, last_name, email, address, 'sakila' FROM sakila_customers
  UNION
  SELECT first_name, last_name, email, address, 'adventureworks' FROM adventure_customers
;


SELECT * FROM all_customers