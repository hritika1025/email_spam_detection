CREATE DATABASE spam_test;
USE spam_test;
CREATE TABLE email(
    id INT(11) NOT NULL AUTO_INCREMENT,
    mail TEXT(20000) NOT NULL,
    PRIMARY KEY(id)
);