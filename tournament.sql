-- Creating the database 'tournament'.
CREATE DATABASE tournament;

-- Connecting to the database 'tournament'.
\c tournament;

-- Creating table 'players' to store the information about players.
CREATE TABLE players( id SERIAL primary key,
		      name TEXT);

-- Creating table 'matches' to store the matches in a tournament and the who was the winner.
CREATE TABLE matches( matchid SERIAL primary key,
		      player1 integer references players(id),
		      player2 integer references players(id),
		      winner integer references players(id));

-- Creating table 'playerhistory' to store the matches played by the players.
CREATE TABLE playerHistory(id integer references players(id),
			   matchid integer references matches(matchid));

-- Creating view 'scores' to obtain scores of the players.
CREATE VIEW scores AS SELECT players.id as id ,COALESCE(q.points,0)as points 
		      FROM players left join (SELECT winner, count(*) AS points FROM matches GROUP BY winner) AS q 
		      ON players.id = q.winner;

-- Creating view 'subq1'
CREATE VIEW subq1 as select players.id , scores.points as wins from players left join scores on players.id = scores.id;

-- Creating view 'subq'
CREATE VIEW subq as select players.id , count(playerhistory.matchid) as matches from players left join playerhistory on players.id = playerhistory.id group by players.id;
