INSERT INTO users (username, password, balance)
VALUES
('user1','pbkdf2:sha256:150000$GvVnT6am$378d081b4dc457b29f4f4b586868ad6ba48aa3dd0921ca57a1e8769249183a47', 0),
('user2','pbkdf2:sha256:150000$vAjo9nvm$4ddc5af00da79c82947064dcf63260865303c26094b56d5d4b4f54766762c590', 500),
('user3','pbkdf2:sha256:150000$qWCOMov3$dcc6846d8bdfdf0040900186539ac660636b2e42bac1c3be3efb7eb05f366a31', 1750),
('user4','pbkdf2:sha256:150000$APaopus6$a5ac347123855f8aa9c56bfbf2df7b647dc05e4b85f7356407441ef09e4d1730', 500),
('user5','pbkdf2:sha256:150000$NO9FGhBO$f7267d0ea798388a8595f1ccb54fd400a0968534f1eecb70b09921a463376716', 0);

INSERT INTO transactions (sender_id, receiver_id, value)
VALUES (1,2,500);
