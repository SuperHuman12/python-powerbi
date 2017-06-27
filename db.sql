CREATE Database powerbi;
USE powerbi;


CREATE TABLE users(
  username VARCHAR (20),
  password BINARY(100),

  PRIMARY KEY (username)
);

INSERT INTO users VALUES ('admin',md5('admin'));


CREATE TABLE dashboards(
  username VARCHAR (20),
  url VARCHAR (500) NOT NULL,

  FOREIGN KEY (url) REFERENCES users(username)
);