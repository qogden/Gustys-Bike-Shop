/*Database*/
DROP DATABASE IF EXISTS bikes;
CREATE DATABASE bikes;

DROP ROLE IF EXISTS biker;
CREATE ROLE biker WITH password 'bike123' LOGIN;
\c bike

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email text NOT NULL,
    password text NOT NULL,
    usertype text NOT NULL
    
    PRIMARY KEY(email)
);

GRANT ALL ON users TO biker;
GRANT ALL ON users_email_seq TO biker;

DROP TABLE IF EXISTS customer;
CREATE TABLE customer (
    id serial NOT NULL,
    firstname text NOT NULL,
    lastname text NOT NULL,
    email text NOT NULL reference users(email),
    
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
    
    PRIMARY KEY(id)
);

GRANT ALL ON customer TO biker;
GRANT ALL ON customer_id_seq TO biker;

DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
    id serial NOT NULL,
    email text NOT NULL reference users(email),

    /*address*/
    street1 text NOT NULL,
    street2 text NOT NULL,
    city text NOT NULL,
    state text NOT NULL,
    zip text NOT NULL
    
    PRIMARY KEY(id)
);

GRANT ALL ON employee TO biker;
GRANT ALL ON employee_id_seq TO biker;

DROP TABLE IF EXISTS timesheet;
CREATE TABLE timesheet (
    id serial NOT NULL,
    employeeid text NOT NULL reference employee(id),
    clock timestamp NOT NULL,
    hours int NOT NULL
    
    PRIMARY KEY(id)
);

GRANT ALL ON timesheet TO biker;
GRANT ALL ON timesheet_employeeid_seq TO biker;

DROP TABLE IF EXISTS product;
CREATE TABLE users (
    id serial NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    price decimal NOT NULL,
    stock int NOT NULL
    
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS cart;
CREATE TABLE cart (
    id serial NOT NULL,
    customerid text NOT NULL reference customer(id),
    clock timestamp NOT NULL,
    productid text NOT NULL,
    quantity int NOT NULL
    
    PRIMARY KEY(id)
);

GRANT ALL ON cart TO biker;
GRANT ALL ON cart_id_seq TO biker;

DROP TABLE IF EXISTS review;
CREATE TABLE review (
    id serial NOT NULL,
    customerid text NOT NULL reference customer(id),
    productid text NOT NULL reference product(id),
    day date NOT NULL,
    rating int NOT NULL,
    comment text NOT NUll
    
    PRIMARY KEY(id)
);

GRANT ALL ON users TO biker;
GRANT ALL ON users_id_seq TO biker;

/*CREATING TEST USERS*/
INSERT INTO users(username, password) VALUES('master', crypt('master123', gen_salt('bf')), 'master administrator');
INSERT INTO users(username, password) VALUES('manager', crypt('manager123', gen_salt('bf')), 'manager asministrator');
INSERT INTO users(username, password) VALUES('sales', crypt('sales123', gen_salt('bf')), 'sales administrator');
INSERT INTO users(username, password) VALUES('employee', crypt('employee123', gen_salt('bf')), 'employee');
INSERT INTO users(username, password) VALUES('customer', crypt('customer123', gen_salt('bf')), 'customer');

