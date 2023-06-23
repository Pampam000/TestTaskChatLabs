CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0 CHECK (balance >= 0)
);

CREATE TABLE IF NOT EXISTS Business (
    name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Platform (
    name varchar(255) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Orders (
    id serial PRIMARY KEY,
    business_name VARCHAR(255) REFERENCES Business(name) NOT NULL,
    platform_name VARCHAR(255) REFERENCES Platform(name) NOT NULL,
    user_id INTEGER REFERENCES Users (id) NOT NULL,
    min_price INTEGER NOT NULL CHECK (min_price > 0),
    max_price INTEGER NOT NULL CHECK (max_price >= min_price),
    phone VARCHAR(20) NOT NULL
);