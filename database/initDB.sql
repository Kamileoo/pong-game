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
    nick VARCHAR(20) NOT NULL UNIQUE,
    password CHAR(72) NOT NULL,
    -- 0 if not admin 1 if admin
    admin BOOL NOT NULL DEFAULT FALSE,
    no_games BIGINT DEFAULT 0,
    no_wins BIGINT DEFAULT 0,
    no_loses BIGINT DEFAULT 0,
    no_ties BIGINT DEFAULT 0);
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
    game_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    start_time datetime NOT NULL,
    end_time datetime not null
);
CREATE TABLE participants(
    game_id BIGINT REFERENCES games(game_id),
    user_id BIGINT REFERENCES users(user_id),
    status ENUM('W', 'L', 'T'),
    score SMALLINT NOT NULL,
    PRIMARY KEY (game_id, user_id)
);
-- functions and procedures
DELIMITER $$
drop procedure if exists add_game$$
create procedure add_game(
    IN start_time datetime,
    IN end_time datetime,
    IN winner_id BIGINT,
    IN loser_id BIGINT
    )BEGIN
    DECLARE game_id bigint;
    INSERT INTO games (start_time, end_time) values(start_time, end_time);
    select LAST_INSERT_ID() into game_id ;
    insert into participants values(
            game_id, winner_id, 'W', 1);
    insert into participants values(
            game_id, loser_id, 'L', 0);
    END$$
drop trigger if exists update_player_stats$$
create trigger update_plater_stats AFTER INSERT 
ON participants FOR EACH ROW
BEGIN
    IF NEW.status = 'W' THEN
        UPDATE users 
        SET no_wins = no_wins + 1
        WHERE user_id=NEW.user_id;
    ELSEIF NEW.status = 'L' THEN
        UPDATE users 
        SET no_loses = no_loses + 1
        WHERE user_id=NEW.user_id;
    ELSE 
        UPDATE users
        SET no_ties = no_ties +1
        WHERE user_id = NEW.user_id;
    END IF;
    UPDATE users 
    SET no_games=no_games+1
    where user_id=NEW.user_id; 
END$$

drop procedure if exists add_login_event$$
create procedure add_login_event(
    IN system_name VARCHAR(40),
    IN system_version VARCHAR(10),
    IN ip_address VARCHAR(15),
    IN user_id BIGINT
)BEGIN
INSERT INTO logins_history
VALUES(
    system_name,
    system_version,
    ip_address,
    user_id,
    NOW()
);
END$$

drop trigger if exists new_ip$$
create trigger new_ip BEFORE UPDATE
ON logins_history FOR EACH ROW
BEGIN
    DECLARE ip_exists BOOL;
    SELECT IF(COUNT(*)>0,1,0) FROM ip_addresses 
    WHERE ip_address=NEW.ip_address into ip_exists;
    IF ip_exists=0 THEN 
    INSERT INTO ip_addresses values(NEW.ip_address);
    END IF;
END$$

drop trigger if exists new_os$$
create trigger new_os BEFORE UPDATE
ON logins_history FOR EACH ROW
BEGIN
    DECLARE os_exists BOOL;
    SELECT IF(COUNT(*)>0,1,0) FROM operating_systems 
    WHERE name=NEW.operating_system and 
    version=NEW.system_version into os_exists;
    IF os_exists=0 THEN 
    INSERT INTO operating_ststems 
    values(NEW.operating_system,NEW.system_version);
    END IF;
END$$


drop trigger if exists two_games_achivement$$
create trigger two_games_achivement AFTER UPDATE
ON users FOR EACH ROW
BEGIN
    IF NEW.no_games = 2 AND OLD.no_games<>2 THEN
        INSERT INTO got_achivements 
        VALUES(
            'TWO_GAMES',
            NEW.user_id,
            NOW()
        );
    END IF;
END$$
DELIMITER ;
-- fill databes with examples
insert into users(email, nick, password)
values('domek@nic.pl', 'nick1', '123'),
('domek@nic1.pl', 'nick2', '123'),
('domek@bajonajo.com', 'nick3', '1234');
insert into achivements(name) values ('TWO_GAMES');
CALL add_game('2013-01-23 01:14:04','2013-01-23 01:14:04',1,2);
CALL add_game('2013-01-23 01:14:04','2013-01-23 01:14:04',2,1);
CALL add_game('2013-01-23 01:14:04','2013-01-23 01:14:04',3,1);

COMMIT;
DELIMITER ;
show TABLES;