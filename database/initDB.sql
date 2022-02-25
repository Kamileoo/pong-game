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
CREATE TABLE operating_systems(
    name VARCHAR(40),
    version VARCHAR(10),
    PRIMARY KEY (name, version)
);
CREATE TABLE ip_addresses(
    ip_address VARCHAR(15) PRIMARY KEY
);
CREATE TABLE logins_history(
    operating_system VARCHAR(40) REFERENCES operating_systems(name),
    system_version VARCHAR(10) REFERENCES operating_systems(version),
    ip_address VARCHAR(15) REFERENCES ip_addresses(ip_address),
    user_id BIGINT REFERENCES users(user_id),
    login_time DATETIME NOT NULL,
    logout_time DATETIME NOT NULL,
    PRIMARY KEY(operating_system, system_version, ip_address, user_id)
);
CREATE TABLE guilds(
    name varchar(30) PRIMARY KEY
);
CREATE TABLE games(
    game_id BIGINT PRIMARY KEY,
    start_time datetime NOT NULL,
    end_time datetime not null
);
CREATE TABLE participants(
    game_id BIGINT REFERENCES games(game_id),
    user_id BIGINT REFERENCES users(user_id),
    status CHAR(1) NOT NULL,
    score SMALLINT NOT NULL,
    PRIMARY KEY (game_id, user_id)
);
-- fill databes with examples
insert into users(email, nick, password)
values('domek@nic.pl', 'nick1', PASSWORD('123'));
insert into users(email, nick, password)
values('domek@nic1.pl', 'nick2', PASSWORD('123'));
show TABLES;