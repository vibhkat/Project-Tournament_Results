-- Creating the database 'tournament'.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Connecting to the database 'tournament'.
\c tournament;

-- Creating table 'players' to store the information about players.
CREATE TABLE players( id SERIAL primary key,
		      name TEXT);

-- Creating table 'matches' to store the matches in a tournament and the who was the winner.
CREATE TABLE matches( matchid SERIAL primary key,
		      winner integer references players(id),
		      loser integer references players(id));

-- Creating view 'playerhistory' to obtain the matche history of the players.
CREATE VIEW playerHistory as SELECT matchid, winner AS id FROM matches UNION SELECT matchid, loser AS id FROM matches;

-- Creating view 'scores' to obtain scores of the players.
CREATE VIEW scores AS SELECT players.id as id ,COALESCE(q.points,0)as points 
		      FROM players left join (SELECT winner, count(*) AS points FROM matches GROUP BY winner) AS q 
		      ON players.id = q.winner;

-- Creating view 'subq1'
CREATE VIEW subq1 AS SELECT players.id , scores.points AS wins FROM players LEFT JOIN scores ON players.id = scores.id;

-- Creating view 'subq'
CREATE VIEW subq AS SELECT players.id , count(playerhistory.matchid) AS matches FROM players LEFT JOIN playerhistory ON players.id = playerhistory.id GROUP BY players.id;
