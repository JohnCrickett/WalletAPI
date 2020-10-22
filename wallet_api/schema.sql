DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS transactions;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  balance INTEGER NOT NULL
);

CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  transaction_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sender_id INTEGER NOT NULL,
  receiver_id INTEGER NOT NULL,
  value INTEGER NOT NULL,
  FOREIGN KEY (sender_id) REFERENCES user (id),
  FOREIGN KEY (receiver_id) REFERENCES user (id)
);
