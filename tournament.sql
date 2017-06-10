-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players (
	id serial PRIMARY KEY,
	name text NOT NULL
);

DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE matches (
	id serial primary key,
	winner int references players(id),
	loser int references players(id)
);

CREATE VIEW wins AS
SELECT players.id, players.name, COUNT(matches.winner) as wins
FROM players LEFT JOIN matches
ON players.id = matches.winner
GROUP BY players.id;

CREATE VIEW matchesplayed AS 
SELECT players.id, 
(SELECT count(*) FROM matches WHERE players.id in (matches.winner, matches.loser)) as matches 
FROM players 
GROUP BY players.id;

CREATE VIEW standings AS 
SELECT wins.id, wins.name, wins.wins, matchesplayed.matches 
FROM wins LEFT JOIN matchesplayed 
ON wins.id = matchesplayed.id
ORDER BY wins.wins DESC, matchesplayed.matches ASC;
