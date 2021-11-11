--Retail Therapy
--Jonathan Browning (Products Guru), Piper Hampsch (Users Guru), Lucas Lynn (Social Guru), Connor Murphy (Sellers Guru), Leah Okamura (Carts Guru)
--CS 316
--Code is arranged by what it pertains to
--There are 5 categories: (Users, Products, Carts, Sellers, Social)


--USERS--+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

--Users(uid, email, firstname, lastname, address, password)
CREATE TABLE Users (
    id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    -- address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

--Account(uid, balance)
CREATE TABLE Account (
    uid INT NOT NULL PRIMARY KEY REFERENCES Users(id),
    balance FLOAT NOT NULL DEFAULT 0.0 CHECK (balance >= 0.0)
);

--Purchases(uid, oid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page)
CREATE TABLE Purchases (
    oid INT NOT NULL PRIMARY KEY,
    uid INT NOT NULL REFERENCES Users(id),
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

--Products(id, name, price, available, img)
CREATE TABLE Products (
    pid INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    img BYTEA NOT NULL --apparently psql prefers BYTEA to IMAGE
);

--CARTS--++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

--Cart(cid)
CREATE TABLE Cart(
    cid INT NOT NULL PRIMARY KEY
);

--InCart(cid, p_quantity, unit_price, total_price, pid, uid)
CREATE TABLE InCart (
    cid INT UNIQUE NOT NULL REFERENCES Cart(cid),
    p_quantity INT NOT NULL CHECK(p_quantity >=1),
    unit_price FLOAT NOT NULL,  --REFERENCES Products(price), --removed this b/c of constraints on use of REFERENCES
    total_price FLOAT NOT NULL,
    pid INT UNIQUE NOT NULL REFERENCES Products(pid),
    uid INT UNIQUE REFERENCES Users(id),
    PRIMARY KEY(cid)
);

--SaveForLater(cid, p_quantity, unit_price, total_price, pid)
CREATE TABLE SaveForLater (
    cid INT UNIQUE NOT NULL REFERENCES Cart(cid),
    p_quantity INT NOT NULL CHECK(p_quantity >=1),
    unit_price FLOAT NOT NULL, --REFERENCES Products(price), --see above
    total_price FLOAT NOT NULL,
    pid INT UNIQUE NOT NULL REFERENCES Products(pid),
    uid INT UNIQUE REFERENCES Users(id),
    PRIMARY KEY(cid)
);

--Orders(cid, oid, order_totalPrice, fulfilled)
CREATE TABLE Orders (
    cid INT NOT NULL REFERENCES Cart(cid),
    oid INT NOT NULL,
    order_totalPrice FLOAT NOT NULL,
    fulfilled BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(oid)
);

--SELLERS--++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

--Sellers(id)
CREATE TABLE Sellers (
    id INT UNIQUE NOT NULL REFERENCES Users(id),
    PRIMARY KEY (id)
    --seller_name: how to deal with this if sellers are also users
);

--Inventory(seller_id, pid, in_stock)
CREATE TABLE Inventory (
    seller_id INT NOT NULL REFERENCES Sellers(id),
    pid INT NOT NULL REFERENCES Products(pid),
    in_stock INT NOT NULL
);

--SellerOrders(seller_id, order_id, uid)
CREATE TABLE SellerOrders (
	seller_id INT NOT NULL REFERENCES Sellers(id),
	order_id INT NOT NULL REFERENCES Orders(oid) PRIMARY KEY,
	uid INT NOT NULL REFERENCES Users(id)
);

--UpdateSubmission(buyer_balance, seller_balance, fulfilled_time, oid, cid, seller_id, bid, total_price)
--moved here to be below Sellers
CREATE TABLE Update_Submission(
    buyer_balance FLOAT NOT NULL,
    seller_balance FLOAT NOT NULL,
    fulfilled_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    oid INT UNIQUE NOT NULL REFERENCES Orders(oid),
    cid INT UNIQUE NOT NULL REFERENCES Cart(cid),
    seller_id INT UNIQUE NOT NULL REFERENCES Sellers(id),
    --bid INT NOT NULL REFERENCES Buyers(id), --commenting this out bc we have no buyers table
    total_price FLOAT UNIQUE NOT NULL,  --REFERENCES InCart(total_price), --see above note about REFERENCES
    PRIMARY KEY(oid, seller_id, cid), --bid
    CHECK(buyer_balance >= total_price)
);

--SOCIAL--+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

--Product_Reviews(uid, pid, time_reviewed, rating, comments, votes)
CREATE TABLE Product_Reviews (
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(pid),
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating FLOAT NOT NULL DEFAULT 0.0 CHECK(rating >= 0.0 AND rating <= 5.0),
    comments VARCHAR(2048),
    votes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (uid, pid)
);

--Seller_Reviews(uid, seller_id, time_reviewed, rating, comments, votes)
CREATE TABLE Seller_Reviews (
    uid INT NOT NULL REFERENCES Users(id),
    seller_id INT NOT NULL REFERENCES Sellers(id),
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating FLOAT NOT NULL DEFAULT 0.0 CHECK(rating >= 0.0 AND rating <= 5.0),
    comments VARCHAR(2048),
    votes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (uid, seller_id)
);

--Images_Reviews(uid, pid, img)
CREATE TABLE Images_Reviews (
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(pid), 
    img BYTEA NOT NULL
);

--PublicView(uid, firstname, seller, email, address, reviews)
CREATE VIEW PublicView(uid, firstname, email, address, reviews) AS
    SELECT Users.uid, firstname, email, address, rating --before 'rating' was 'reviews' - not sure if we want rating or comments?
    FROM Users, Seller_Reviews
    WHERE Users.uid = Seller_Reviews.seller_id
;
-- moved this one down here b/c sql got mad that Seller_Reviews hadn't been declared yet
