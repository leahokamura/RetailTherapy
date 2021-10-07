-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

--Users(uid, email, firstname, lastname, address, password)
CREATE TABLE Users (
    uid INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

--Account(uid, balance)
CREATE TABLE Account (
    uid INT NOT NULL PRIMARY KEY REFERENCES Users(uid),
    balance FLOAT NOT NULL DEFAULT 0.0;
);

--Purchases(uid, oid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page)
CREATE TABLE Purchases (
    oid INT NOT NULL PRIMARY KEY,
    uid NOT NULL REFERENCES Users(uid),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    total_amount FLOAT NOT NULL,
    item_quantity INT NOT NULL,
    fulfillment_status VARCHAR(20) NOT NULL CHECK (fulfillment_status IN ('Ordered', 'In Transit', 'Delivered')),
    order_page VARCHAR(2048)
);

--Public_View(uid, firstname, seller, email, address, reviews)
CREATE TABLE Public_View (
    uid INT NOT NULL PRIMARY KEY REFERENCES Users(uid),
    firstname VARCHAR(255) NOT NULL REFERENCES Users(firstname)
    --seller BOOLEAN DEFAULT FALSE,
    --address VARCHAR(255) NOT NULL REFERENCES Users(address)
    --reviews TYPE REFERENCES Seller_Reviews()
);

CREATE VIEW PublicView(uid, firstname, email, address, reviews) AS
    SELECT uid, firstname, email, address, reviews
    FROM Users, Seller_Reviews
    WHERE Users.uid = Seller_Reviews.id
;

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE
);


CREATE TABLE Product_Reviews (
    uid REFERENCES Users(uid),
    pid REFERENCES Products(id),
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating INT NOT NULL,
    comments VARCHAR(2048),
    votes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (uid, pid)
)

CREATE TABLE Seller_Reviews (
    uid REFERENCES Users(uid),
    seller_id REFERENCES Sellers(id),
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating INT NOT NULL,
    comments VARCHAR(2048),
    votes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (uid, seller_id)
)

CREATE TABLE Images_Reviews (
    uid REFERENCES Users(uid),
    pid REFERENCES Products(id), 
    img INT NOT NULL
)
