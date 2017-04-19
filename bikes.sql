/*Content database in PostgreSQL*/
DROP DATABASE IF EXISTS bikes;
CREATE DATABASE bikes;

DROP ROLE IF EXISTS biker;
CREATE ROLE biker WITH password 'bike123' LOGIN;
\c bikes

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS users CASCADE;
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
    t_date timestamp NOT NULL,
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
    comment text NOT NULL
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
     id serial NOT NULL PRIMARY KEY,
     customerid int NOT NULL references customers(id),
     orderdate timestamp NOT NULL,
     status text NOT NULL,
     
     firstname text NOT NULL,
     lastname text NOT NULL,
     email text NOT NULL references users(email),
     
     /*billing information*/
     bstreet text NOT NULL,
     bstreet2 text NOT NULL,
     bcity text NOT NULL,
     bstate text NOT NULL,
     bzip text NOT NULL,
    
     /*shipping information*/
     sstreet text NOT NULL,
     sstreet2 text NOT NULL,
     scity text NOT NULL,
     sstate text NOT NULL,
     szip text NOT NULL,
    
     /*payment information*/
     cardno text NOT NULL,
     csc text NOT NULL,
     exp text NOT NULL
     
);

DROP TABLE IF EXISTS orderitems;
CREATE TABLE orderitems(
    orderid int NOT NULL references orders(id),
    productid int NOT NULL references products(id),
    price decimal NOT NULL,
    quantity int NOT NULL

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
GRANT ALL ON orderitems TO biker;
GRANT ALL ON orders TO biker;
GRANT ALL ON orders_id_seq TO biker;


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
INSERT INTO customers(firstname, lastname, email, bstreet1, bstreet2, bcity, bstate, bzip, sstreet1, sstreet2, scity, sstate, szip, cardno, csc, exp) VALUES('testfirstname', 'testlastname', (SELECT email FROM users WHERE email = 'user2@email.com'), 
                        'testbstreet1', 'testbstreet2', 'testbcity', 'AZ', 'testbzip', 'testsstreet1', 'testsstreet2', 'testscity', 'VA', 'testszip', '1234567890', '123','2017-09');
INSERT INTO customers(firstname, lastname, email) VALUES('testfirstname2', 'testlastname1', (SELECT email FROM users WHERE email = 'customers1@email.com'));
INSERT INTO customers(firstname, lastname, email) VALUES('userfirst1', 'userlast1', (SELECT email FROM users WHERE email = 'user1@email.com'));
INSERT INTO customers(firstname, lastname, email) VALUES('userfirst2', 'userlast2', (SELECT email FROM users WHERE email = 'customers@email.com'));

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
INSERT INTO producttype(producttype) VALUES ('parts');
INSERT INTO producttype(producttype) VALUES ('tools');


/*ADDING BIKE PRODUCTS*/
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Merax BW2KS', '/static/images/bike1.jpg','Never stop riding.', 749.99, 31, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bayside Kent3600', '/static/images/bike2.jpeg','Made for the perfect ride along the water.', 644.99, 49, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Mongoose XCT28', '/static/images/bike3.jpeg','Able to withstand great impact.', 389.99, 15, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Genesis Off Road 2061', '/static/images/bike4.jpeg','Made to last a lifetime.', 700.00, 37, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Frameo 360', '/static/images/bike5.jpg','Perfect for the long haul.', 624.99, 55, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Mongoose 28', '/static/images/bike6.jpeg','Durable bike withstand inclement weather with a breeze.', 374.99, 70, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Roadmaster Adventure', '/static/images/bike7.jpeg','An adorable blue finish is pperfect for your future cyclists.', 100.50, 75, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Serv 6000', '/static/images/bike8.jpg','A great bike for mountain climbing', 149.99, 40, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Durbon C5', '/static/images/bike9.jpg','A perfect fit for tall riders.', 255.00, 20, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Diamondback XC', '/static/images/bike10.jpg','It is perfect for hiking steep inclines or for casual strolls.', 449.99, 60, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Orange 324', '/static/images/bike11.jpg','Beautiful red color makes it visible in dark settings.', 300.00, 30, 1);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Northwoods Pamona', '/static/images/bike12.jpg','Aethetically pleasing, this bike has a beautiful silver and seafoam grean finish.', 249.99, 50, 1);

/*ADDING PART PRODUCTS*/
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Black Handle Bar', '/static/images/parts1.jpeg','This stainless steel handle bar is very study and with stands weather damages.', 16.85, 50, 2);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bike Bicycle FreeWheel', '/static/images/parts2.jpeg','Universal gear replacement', 29.99, 45, 2);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bicycle Front Wheel', '/static/images/parts3.jpeg','24 x 1.75 ALLOY BOLT-ON', 28.99, 14, 2);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Weinmann Hybrid Wheel', '/static/images/parts4.jpeg','700 x 35 Quick Release Silver Alloy Front Wheel.', 29.99, 30, 2);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Black Bell Sports Tire', '/static/images/parts5.jpeg','Mountain bike tire with mountain bike tire with Kevlar', 75.50, 63, 2);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bell Inner Tube', '/static/images/parts6.jpeg','26" Universal inner tube replacement, durable and reliable.', 5.00, 20, 2);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Red Bar Handle', '/static/images/parts7.jpeg','This stainless steel handle bar is very study and with stands weather damages.', 16.85, 52, 2);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bell Front Wheel', '/static/images/parts8.jpg','Wheel comes with inner tube and tire traction.', 75.50, 65, 2);

/*ADDING TOOL PRODUCTS*/
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bell Tire Patching Glue', '/static/images/tools1.jpeg','Reliable glue to patch inconvenience quickly.', 10.50, 50, 3);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bikehand Crankset Crank Arm Puller Removal Tool', '/static/images/tools2.jpeg','A tool to help you get there.', 12.00, 20, 3);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bikehand Chain Wear Indicator', '/static/images/tools3.jpeg','Do not wait until the chain breaks to replace it. Let us help you check for wear in the chain', 75.50, 30, 3);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Image 16 in 1 Multi-Funtional Repair Tool', '/static/images/tools4.jpeg','With a combination of different tools, this tool set can help you with any repair.', 9.99, 33, 3);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bike Wheel Truing Stand', '/static/images/tools5.jpeg', 'Spin those wheels for days on this truing stand.', 45.00, 29, 3);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('Bikehand Chain Quick Link Open Close Tool', '/static/images/tools6.jpeg','Quickly open and close chain links with this tool.', 15.00, 43, 3);
INSERT INTO products(name, image, description, price, stock, producttype) VALUES ('29 piece Bike Repair Tool Set', '/static/images/tools7.jpeg','Perfect emergency repair tool kit to fix your bike on the go.', 75.50, 60, 3);

/*ADDING TO CART*/
INSERT INTO cart(customerid, day, productid, quantity) VALUES((SELECT id FROM customers WHERE email = 'user2@email.com'), (SELECT CURRENT_DATE), 2, 1);
INSERT INTO cart(customerid, day, productid, quantity) VALUES((SELECT id FROM customers WHERE email = 'user1@email.com'), (SELECT CURRENT_DATE), 1, 2);
INSERT INTO cart(customerid, day, productid, quantity) VALUES((SELECT id FROM customers WHERE email = 'user1@email.com'), (SELECT CURRENT_DATE), 2, 1);
INSERT INTO cart(customerid, day, productid, quantity) VALUES((SELECT id FROM customers WHERE email = 'user2@email.com'), (SELECT CURRENT_DATE), 4, 2);

/*ADDING TO TIMESHEET*/
INSERT INTO timesheet(employeeid, t_date, hours) VALUES((SELECT id FROM employees WHERE email = 'sales@gustybikeshop.com'), (SELECT CURRENT_DATE-1), 4);
INSERT INTO timesheet(employeeid, t_date, hours) VALUES((SELECT id FROM employees WHERE email = 'employee@gustybikeshop.com'), (SELECT CURRENT_DATE-2), 2);
INSERT INTO timesheet(employeeid, t_date, hours) VALUES((SELECT id FROM employees WHERE email = 'employee@gustybikeshop.com'), (SELECT CURRENT_DATE-1), 8);

/*ADDING REVIEWS*/
INSERT INTO reviews(customerid, productid, day, rating, comment) VALUES((SELECT id FROM customers WHERE email = 'user1@email.com'), 1, (SELECT CURRENT_DATE), 5, 'This is a great product!');
INSERT INTO reviews(customerid, productid, day, rating, comment) VALUES((SELECT id FROM customers WHERE email = 'user2@email.com'), 1, (SELECT CURRENT_DATE), 3, 'This is make to last. Love it!');











