#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Removing all the match records from the database."""

    conn = connect()
    c = conn.cursor()

    """Removing all the match records from the table 'matches'. """
    c.execute("DELETE FROM matches")

    conn.commit()
    conn.close()


def deletePlayers():
    """Removing all the player records from the database."""

    conn = connect()
    c = conn.cursor()

    """Removing all the player records from the table 'players'. """
    c.execute("DELETE FROM players")

    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()

    """Counting the number of rows in the table 'players'. """
    c.execute("SELECT count(*) from players")
    count = c.fetchone()
    conn.close()
    return count[0]


def registerPlayer(name):
    """Adding a player to the tournament database.
    Args:
      name: the player's full name.
    """
    conn = connect()
    c = conn.cursor()

    """Adding a player into the table 'players'. """
    c.execute("INSERT INTO players(name) VALUES(%s)", (name,))

    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()

    """Getting a list of tuples which contains (id, name, wins and number of matches). """
    c.execute("SELECT players.id , players.name , subq1.wins, subq.matches FROM players, subq, subq1 WHERE players.id = subq.id AND players.id=subq1.id ORDER BY subq1.wins DESC;")
    l = c.fetchall()

    conn.close()
    return l


def reportMatch(winner, loser):
    """Recording the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()

    """Inserting information regarding the match and the winner in the table 'matches'. """
    c.execute("INSERT INTO matches(winner, loser) values(%s, %s)", (winner, loser))
    conn.commit()

    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()

    """ Getting the results sorted on on the basis of points of players. """
    c.execute("SELECT players.id, players.name FROM players, scores WHERE players.id=scores.id ORDER BY scores.points")
    l = c.fetchall()
    conn.close()

    result = []
    for i in range(0, len(l), 2):
        result.append((l[i][0], l[i][1], l[i+1][0], l[i+1][1]))
    return result