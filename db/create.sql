--Retail Therapy
--Jonathan Browning (Products Guru), Piper Hampsch (Users Guru), Lucas Lynn (Social Guru), Connor Murphy (Sellers Guru), Leah Okamura (Carts Guru)
--CS 316
--Code is arranged by what it pertains to
--There are 5 categories: (Users, Products, Carts, Sellers, Social)


--USERS--+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

--Users(uid, email, firstname, lastname, address, password)
CREATE TABLE Users (
    uid INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    password VARCHAR(255) NOT NULL
);

--Affirm(uid, affirmation)
CREATE TABLE Affirm (
    affirmation VARCHAR(255) NOT NULL PRIMARY KEY
);

--Account(uid, balance)
CREATE TABLE Account (
    uid INT NOT NULL PRIMARY KEY REFERENCES Users(uid),
    balance FLOAT NOT NULL DEFAULT 0.00 CHECK (balance >= 0.00)
);

--Purchases(oid, uid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page)
CREATE TABLE Purchases (
    oid INT NOT NULL PRIMARY KEY,
    uid INT NOT NULL REFERENCES Users(uid),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    total_amount FLOAT NOT NULL,
    item_quantity INT NOT NULL,
    fulfillment_status VARCHAR(20) NOT NULL CHECK (fulfillment_status IN ('Ordered', 'In Transit', 'Delivered')),
    order_page VARCHAR(2048)
);

--PRODUCTS

--Product_Categories(category)
CREATE TABLE Product_Categories (
    category VARCHAR(255) NOT NULL PRIMARY KEY
);

--Products(pid, name, price, available, image)
CREATE TABLE Products (
    pid INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    image VARCHAR(4096) NOT NULL, --apparently psql prefers BYTEA to IMAGE
    description VARCHAR(2048) NOT NULL,
    category VARCHAR(255) NOT NULL REFERENCES Product_Categories(category)
);

--SELLERS--++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

--Sellers(uid)
CREATE TABLE Sellers (
    uid INT UNIQUE NOT NULL REFERENCES Users(uid),
    PRIMARY KEY (uid)
    --seller_name: how to deal with this if sellers are also users
);

--Inventory(seller_id, pid, in_stock)
CREATE TABLE Inventory (
    seller_id INT NOT NULL REFERENCES Sellers(uid),
    pid INT NOT NULL REFERENCES Products(pid),
    in_stock INT NOT NULL
);

--SellerOrders(seller_id, order_id, uid)
CREATE TABLE SellerOrders (
	seller_id INT NOT NULL REFERENCES Sellers(uid),
	order_id INT NOT NULL REFERENCES Orders(oid) PRIMARY KEY,
	uid INT NOT NULL REFERENCES Users(uid)
);

--CARTS--++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

--InCart(uid, pid, name, p_quantity, unit_price, seller_id)
CREATE TABLE InCart(
    uid INT NOT NULL REFERENCES Users(uid),
    pid INT NOT NULL REFERENCES Products(pid),
    name VARCHAR(255) REFERENCES Products(name),
    p_quantity INT NOT NULL CHECK(p_quantity >= 1),
    unit_price DECIMAL(10, 2) NOT NULL CHECK(unit_price > 0),
    seller_id INT NOT NULL REFERENCES Sellers(uid),
    PRIMARY KEY(uid, pid, seller_id)
);

--SaveForLater(cid, p_quantity, unit_price, total_price, pid)
-- CREATE TABLE SaveForLater (
--     cid INT UNIQUE NOT NULL REFERENCES Cart(cid),
--     p_quantity INT NOT NULL CHECK(p_quantity >=1),
--     unit_price FLOAT NOT NULL, --REFERENCES Products(price), --see above
--     total_price FLOAT NOT NULL,
--     pid INT UNIQUE NOT NULL REFERENCES Products(pid),
--     uid INT UNIQUE REFERENCES Users(uid),
--     PRIMARY KEY(cid)
-- );

--Orders(oid, uid, total_price, fulfilled, time_purchased)
CREATE TABLE Orders (
    oid INT NOT NULL UNIQUE,
    uid INT NOT NULL REFERENCES Users(uid),
    total_price FLOAT NOT NULL,
    fulfilled BOOLEAN DEFAULT FALSE,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY(oid, uid)
);

--OrderedItems(uid, oid, pid, unit_price, p_quantity, fulfilled, fulfillment_time)
CREATE TABLE OrderedItems (
    uid INT NOT NULL REFERENCES Users(uid),
    oid INT NOT NULL REFERENCES Orders(oid),
    pid INT NOT NULL REFERENCES Products(pid),
    unit_price FLOAT NOT NULL,
    p_quantity INT NOT NULL,
    fulfilled BOOLEAN DEFAULT FALSE,
    fulfillment_time timestamp without time zone DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY (uid, oid, pid)
    
);


--SOCIAL--+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

--Product_Reviews(uid, pid, time_reviewed, rating, comments, votes)
CREATE TABLE Product_Reviews (
    uid INT NOT NULL REFERENCES Users(uid),
    pid INT NOT NULL REFERENCES Products(pid),
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating FLOAT NOT NULL DEFAULT 0.0 CHECK(rating >= 0.0 AND rating <= 5.0),
    comments VARCHAR(2048),
    votes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (uid, pid)
);

CREATE TABLE PR_Comments (
    rid INT NOT NULL REFERENCES Users(uid),
    uid INT NOT NULL REFERENCES Users(uid),
    pid INT NOT NULL REFERENCES Products(pid),
    time_commented timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    comment VARCHAR(2048),
    votes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (uid, pid, time_commented)
);

--Seller_Reviews(uid, seller_id, time_reviewed, rating, comments, votes)
CREATE TABLE Seller_Reviews (
    uid INT NOT NULL REFERENCES Users(uid),
    seller_id INT NOT NULL REFERENCES Sellers(uid),
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating FLOAT NOT NULL DEFAULT 0.0 CHECK(rating >= 0.0 AND rating <= 5.0),
    comments VARCHAR(2048),
    votes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (uid, seller_id)
);

CREATE TABLE SR_Comments (
    rid INT NOT NULL REFERENCES Users(uid),
    uid INT NOT NULL REFERENCES Users(uid),
    seller_id INT NOT NULL REFERENCES Sellers(uid),
    time_commented timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    comment VARCHAR(2048),
    votes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (uid, seller_id, time_commented)
);

--Images_Reviews(uid, pid, img)
CREATE TABLE Images_Reviews (
    uid INT NOT NULL REFERENCES Users(uid),
    pid INT NOT NULL REFERENCES Products(pid), 
    img VARCHAR(255) NOT NULL

);

--PublicView(uid, firstname, seller, email, address, reviews)
CREATE VIEW PublicView(uid, firstname, email, address, reviews) AS
    SELECT Users.uid, firstname, email, address, rating --before 'rating' was 'reviews' - not sure if we want rating or comments?
    FROM Users, Seller_Reviews
    WHERE Users.uid = Seller_Reviews.seller_id
;
-- moved this one down here b/c sql got mad that Seller_Reviews hadn't been declared yet
