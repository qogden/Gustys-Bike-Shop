/*Content database in PostgreSQL*/
DROP DATABASE IF EXISTS bikes;
CREATE DATABASE bikes;

DROP ROLE IF EXISTS biker;
CREATE ROLE biker WITH password 'bike123' LOGIN;
\c bikes

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email text NOT NULL PRIMARY KEY,
    password text NOT NULL
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

DROP TABLE IF EXISTS employeetype;
CREATE TABLE employeetype (
    id serial NOT NULL PRIMARY KEY,
    employeetype text NOT NULL
);

DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    id serial NOT NULL PRIMARY KEY,
    firstname text NOT NULL,
    lastname text NOT NULL,
    email text NOT NULL references users(email),
    employeetype int NOT NULL references employeetype(id),
    
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

DROP TABLE IF EXISTS producttype;
CREATE TABLE producttype (
    id serial NOT NULL PRIMARY KEY,
    producttype text NOT NULL
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id serial NOT NULL PRIMARY KEY,
    name text NOT NULL,
    image text,
    description text,
    price decimal NOT NULL,
    stock int,
    producttype int references producttype(id)
);

DROP TABLE IF EXISTS cart;
CREATE TABLE cart (
    id serial NOT NULL PRIMARY KEY,
    customerid int NOT NULL references customers(id),
    day date NOT NULL,
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

/*PERMISSIONS*/
GRANT ALL ON users TO biker;
GRANT ALL ON customers TO biker;
GRANT ALL ON customers_id_seq TO biker;
GRANT ALL ON employeetype TO biker;
GRANT ALL ON employeetype_id_seq TO biker;
GRANT ALL ON employees TO biker;
GRANT ALL ON employees_id_seq TO biker;
GRANT ALL ON timesheet TO biker;
GRANT ALL ON timesheet_id_seq TO biker;
GRANT ALL ON producttype TO biker;
GRANT ALL ON producttype_id_seq TO biker;
GRANT ALL ON products TO biker;
GRANT ALL ON products_id_seq TO biker;
GRANT ALL ON cart TO biker;
GRANT ALL ON cart_id_seq TO biker;
GRANT ALL ON reviews TO biker;
GRANT ALL ON reviews_id_seq TO biker;


/*ADDING TYPES OF USERS*/
INSERT INTO employeetype(employeetype) VALUES ('master');
INSERT INTO employeetype(employeetype) VALUES ('manager');
INSERT INTO employeetype(employeetype) VALUES ('sales');
INSERT INTO employeetype(employeetype) VALUES ('employee');

/*ADDING USERS*/
INSERT INTO users(email, password) VALUES('customers@email.com', crypt('customer123', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('customers1@email.com', crypt('customer123', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('masters@gustybikeshop.com', crypt('master123', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('managers@gustybikeshop.com', crypt('manager123', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('sales@gustybikeshop.com', crypt('sales123', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('employees@gustybikeshop.com', crypt('employee123', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('employees1@gustybikeshop.com', crypt('employee123', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('employee@gustybikeshop.com', crypt('Simon', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('user1@email.com', crypt('Simon1', gen_salt('bf')));
INSERT INTO users(email, password) VALUES('user2@email.com', crypt('Simon2', gen_salt('bf')));

/*ADDING CUSTOMERS*/
INSERT INTO customers(firstname, lastname, email, bstreet1, bstreet2, bcity, bstate, bzip, sstreet1, sstreet2, scity, sstate, szip, cardno, csc, exp) VALUES('testfirstname', 'testlastname', (SELECT email FROM users WHERE email = 'customers@email.com'), 
                        'testbstreet1', 'testbstreet2', 'testbcity', 'testbstate', 'testbzip', 'testsstreet1', 'testsstreet2', 'testscity', 'testsstate', 'testszip', crypt('testcardno', gen_salt('bf')),  crypt('testcsc', gen_salt('bf')),  crypt('testexp', gen_salt('bf')));
INSERT INTO customers(firstname, lastname, email) VALUES('testfirstname2', 'testlastname1', (SELECT email FROM users WHERE email = 'customers1@email.com'));
INSERT INTO customers(firstname, lastname, email) VALUES('userfirst1', 'userlast1', (SELECT email FROM users WHERE email = 'user1@email.com'));
INSERT INTO customers(firstname, lastname, email) VALUES('userfirst2', 'userlast2', (SELECT email FROM users WHERE email = 'user2@email.com'));

/*ADDING EMPLOYEES*/
INSERT INTO employees(firstname, lastname, employeetype, email, street1, street2, city, state, zip) VALUES('masterfirst', 'masterlast', 1, (SELECT email FROM users WHERE email = 'masters@gustybikeshop.com'), 
                     'teststreet1', 'teststreet2', 'testcity', 'teststate', 'testzip');
INSERT INTO employees(firstname, lastname, employeetype, email, street1, street2, city, state, zip) VALUES('managerfirst', 'managerlast', 2, (SELECT email FROM users WHERE email = 'managers@gustybikeshop.com'), 
                     'teststreet1', 'teststreet2', 'testcity', 'teststate', 'testzip');
INSERT INTO employees(firstname, lastname, employeetype, email, street1, street2, city, state, zip) VALUES('salesfirst', 'saleslast', 3, (SELECT email FROM users WHERE email = 'sales@gustybikeshop.com'), 
                     'teststreet1', 'teststreet2', 'testcity', 'teststate', 'testzip');
INSERT INTO employees(firstname, lastname, employeetype, email, street1, street2, city, state, zip) VALUES('employeefirst', 'employeelast', 4, (SELECT email FROM users WHERE email = 'employees@gustybikeshop.com'), 
                     'teststreet1', 'teststreet2', 'testcity', 'teststate', 'testzip');
INSERT INTO employees(firstname, lastname, employeetype, email, street1, street2, city, state, zip) VALUES('employeefirst1', 'employeelast1', 4, (SELECT email FROM users WHERE email = 'employees1@gustybikeshop.com'), 
                     'teststreet1', 'teststreet2', 'testcity', 'teststate', 'testzip');
INSERT INTO employees(firstname, lastname, employeetype, email, street1, street2, city, state, zip) VALUES('testfirstname', 'testlastname', 4, (SELECT email FROM users WHERE email = 'employee@gustybikeshop.com'), 
                     'teststreet1', 'teststreet2', 'testcity', 'teststate', 'testzip');

/*ADDING PRODUCT TYPES*/
INSERT INTO producttype(producttype) VALUES ('bicycles');
INSERT INTO producttype(producttype) VALUES ('apparel');
INSERT INTO producttype(producttype) VALUES ('parts');
INSERT INTO producttype(producttype) VALUES ('tools');


/*ADDING PRODUCTS*/
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Test Bike', '','testing bikes', 250.99, 30, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Test Apparel', '','testing apparel', 30.00, 100, 2);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Test Parts', '','testing parts', 75.50, 50, 3);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Test Tools', '','testing tools', 20.00, 75, 4);
INSERT INTO products(name, description, price, stock) VALUES('Bicycle', 'Test Bike.', 300, 200);

/*ADDING TO CART*/
INSERT INTO cart(customerid, day, productid, quantity) VALUES((SELECT id FROM customers WHERE email = 'user2@email.com'), (SELECT CURRENT_DATE), 2, 1);
INSERT INTO cart(customerid, day, productid, quantity) VALUES((SELECT id FROM customers WHERE email = 'user1@email.com'), (SELECT CURRENT_DATE), 1, 2);
INSERT INTO cart(customerid, day, productid, quantity) VALUES((SELECT id FROM customers WHERE email = 'user1@email.com'), (SELECT CURRENT_DATE), 2, 1);
INSERT INTO cart(customerid, day, productid, quantity) VALUES((SELECT id FROM customers WHERE email = 'user2@email.com'), (SELECT CURRENT_DATE), 4, 2);

/*ADDING REVIEWS*/
INSERT INTO reviews(customerid, productid, day, rating, comment) VALUES((SELECT id FROM customers WHERE email = 'user1@email.com'), 1, (SELECT CURRENT_DATE), 5, 'This is a great product!');











