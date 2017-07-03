CREATE Database powerbi;
USE powerbi;


CREATE TABLE users(
    username VARCHAR (20) NOT NULL,
    password VARCHAR(32) NOT NULL,
    brand_name VARCHAR (20),
    parent_company VARCHAR (20),
    status VARCHAR (20),
    PRIMARY KEY (username)
);

INSERT INTO users VALUES ('admin', MD5('admin'), NULL, NULL, 'admin');

CREATE TABLE dashboards(
    username VARCHAR (20),
    url VARCHAR (500) NOT NULL,
    msg_dashboard VARCHAR (100) NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username)
);