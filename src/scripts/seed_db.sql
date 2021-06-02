INSERT INTO game(name, min_players, max_players)
VALUES('Settlers of Catan', 2, 4);

INSERT INTO game(name, min_players, max_players)
VALUES('Chess', 2, 2);

INSERT INTO game(name, min_players, max_players)
VALUES('Checkers', 2, 2);

INSERT INTO game(name, min_players, max_players)
VALUES('Munchkin', 3, 6);

INSERT INTO game(name, min_players, max_players)
VALUES('Halo', 1, 16);

INSERT INTO game(name, min_players, max_players)
VALUES('Call of Duty', 1, 16);

INSERT INTO availability(user_id, time_avail)
VALUES(1, '2021-05-24 02:55:05');

INSERT INTO availability(user_id, time_avail)
VALUES(1, '2021-05-25 02:55:05');

INSERT INTO interest(user_id, game_id)
VALUES(1, 1);

INSERT INTO interest(user_id, game_id)
VALUES(1, 2);