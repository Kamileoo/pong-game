DROP DATABASE IF EXISTS pong;
CREATE DATABASE pong;
USE pong;
-- show DATABASES;
CREATE TABLE achivements (
    name VARCHAR(30) PRIMARY KEY,
    -- url to picture
    badge VARCHAR(120));
CREATE TABLE users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(320) NOT NULL,
    nick VARCHAR(20) NOT NULL,
    password CHAR(72) NOT NULL,
    -- 0 if not admin 1 if admin
    admin BOOL NOT NULL DEFAULT FALSE,
    no_games BIGINT,
    no_wins BIGINT,
    no_loses BIGINT,
    no_ties BIGINT);
CREATE TABLE got_achivements (
    achivement_name VARCHAR(30) REFERENCES achivements(name) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    date DATETIME NOT NULL,
    PRIMARY KEY (achivement_name, user_id)
);

show TABLES;