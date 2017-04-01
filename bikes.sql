/*Content database in PostgreSQL*/
DROP DATABASE IF EXISTS bikes;
CREATE DATABASE bikes;

DROP ROLE IF EXISTS biker;
CREATE ROLE biker WITH password 'bike123' LOGIN;
\c bikes

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS usertype;
CREATE TABLE usertype (
    id serial NOT NULL PRIMARY KEY,
    usertype text NOT NULL
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email text NOT NULL PRIMARY KEY,
    password text NOT NULL,
    usertype int NOT NULL references usertype(id)
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    id serial NOT NULL PRIMARY KEY,
    firstname text NOT NULL,
    lastname text NOT NULL,
    email text NOT NULL references users(email),
    
    /*billing information*/
    bstreet1 text,
    bstreet2 text,
    bcity text,
    bstate text,
    bzip text,
    
    /*shipping information*/
    sstreet1 text,
    sstreet2 text,
    scity text,
    sstate text,
    szip text,
    
    /*payment information*/
    cardno text,
    csc text,
    exp text 

);

DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    id serial NOT NULL PRIMARY KEY,
    email text NOT NULL references users(email),

    /*address*/
    street1 text NOT NULL,
    street2 text NOT NULL,
    city text NOT NULL,
    state text NOT NULL,
    zip text NOT NULL
);

DROP TABLE IF EXISTS timesheet;
CREATE TABLE timesheet (
    id serial NOT NULL PRIMARY KEY,
    employeeid int NOT NULL references employees(id),
    clock timestamp NOT NULL,
    hours int NOT NULL
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id serial NOT NULL PRIMARY KEY,
    name text NOT NULL,
    image text,
    description text,
    price decimal NOT NULL,
    stock int
);

DROP TABLE IF EXISTS cart;
CREATE TABLE cart (
    id serial NOT NULL PRIMARY KEY,
    customerid int NOT NULL references customers(id),
    clock date NOT NULL,
    productid text NOT NULL,
    quantity int NOT NULL
);

DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews (
    id serial NOT NULL PRIMARY KEY,
    customerid int NOT NULL references customers(id),
    productid int NOT NULL references products(id),
    day date NOT NULL,
    rating int NOT NULL,
    comment text
);

GRANT ALL ON users TO biker;
GRANT ALL ON customers TO biker;
GRANT ALL ON customers_id_seq TO biker;
GRANT ALL ON employees TO biker;
GRANT ALL ON employees_id_seq TO biker;
GRANT ALL ON timesheet TO biker;
GRANT ALL ON timesheet_id_seq TO biker;
GRANT ALL ON products TO biker;
GRANT ALL ON products_id_seq TO biker;
GRANT ALL ON cart TO biker;
GRANT ALL ON cart_id_seq TO biker;
GRANT ALL ON reviews TO biker;
GRANT ALL ON reviews_id_seq TO biker;

/*TYPES OF USERS*/
INSERT INTO usertype(usertype) VALUES ('master');
INSERT INTO usertype(usertype) VALUES ('manager');
INSERT INTO usertype(usertype) VALUES ('sales');
INSERT INTO usertype(usertype) VALUES ('employee');
INSERT INTO usertype(usertype) VALUES ('customer');

/*CREATING USERS*/
INSERT INTO users(email, password, usertype) VALUES('master', crypt('master123', gen_salt('bf')), 1);
INSERT INTO users(email, password, usertype) VALUES('manager', crypt('manager123', gen_salt('bf')), 2);
INSERT INTO users(email, password, usertype) VALUES('sales', crypt('sales123', gen_salt('bf')), 3);
INSERT INTO users(email, password, usertype) VALUES('employee', crypt('employee123', gen_salt('bf')), 4);
INSERT INTO users(email, password, usertype) VALUES('customer', crypt('customer123', gen_salt('bf')), 5);

/*DATA FOR TEST CASES*/