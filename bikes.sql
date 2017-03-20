/*Database*/
DROP DATABASE IF EXISTS bikes;
CREATE DATABASE bikes;

DROP ROLE IF EXISTS biker;
CREATE ROLE biker WITH password 'bike123' LOGIN;
\c bike

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id serial NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    usertype text NOT NULL
    
    PRIMARY KEY(id)
);

GRANT ALL ON users TO biker;
GRANT ALL ON users_id_seq TO biker;

DROP TABLE IF EXISTS customer;
CREATE TABLE customer (
    userid serial NOT NULL,
    firstname text NOT NULL,
    lastname text NOT NULL,
    
    /*billing information*/
    bstreet1 text NOT NULL,
    bstreet2 text NOT NULL,
    bcity text NOT NULL,
    bstate text NOT NULL,
    bzip text NOT NULL,
    
    /*shipping information*/
    sstreet1 text NOT NULL,
    sstreet2 text NOT NULL,
    scity text NOT NULL,
    sstate text NOT NULL,
    szip text NOT NULL,
    
    /*payment information*/
    cardno text NOT NULL,
    csc text NOT NULL,
    exp text NOT NULL
);

DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
    userid serial NOT NULL,
    
    /*address*/
    street1 text NOT NULL,
    street2 text NOT NULL,
    city text NOT NULL,
    state text NOT NULL,
    zip text NOT NULL
);

DROP TABLE IF EXISTS timesheet;
CREATE TABLE timesheet (
    userid serial NOT NULL,
    clock timestamp NOT NULL,
    hours int NOT NULL
);

DROP TABLE IF EXISTS product;
CREATE TABLE users (
    id serial NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    price decimal NOT NULL,
    stock int NOT NULL
);

DROP TABLE IF EXISTS cart;
CREATE TABLE cart (
    userid text NOT NULL,
    clock timestamp NOT NULL,
    productid text NOT NULL,
    quantity int NOT NULL
);

DROP TABLE IF EXISTS review;
CREATE TABLE review (
    id serial NOT NULL,
    day date NOT NULL,
    rating int NOT NULL,
    userid text NOT NULL,
    productid text NOT NULL,
    comment text NOT NUll
    
    PRIMARY KEY(id)
);

/*CREATING TEST USERS*/
INSERT INTO users(username, password) VALUES('master', crypt('master123', gen_salt('bf')), 'master administrator');
INSERT INTO users(username, password) VALUES('manager', crypt('manager123', gen_salt('bf')), 'manager asministrator');
INSERT INTO users(username, password) VALUES('sales', crypt('sales123', gen_salt('bf')), 'sales administrator');
INSERT INTO users(username, password) VALUES('employee', crypt('employee123', gen_salt('bf')), 'employee');
INSERT INTO users(username, password) VALUES('customer', crypt('customer123', gen_salt('bf')), 'customer');

