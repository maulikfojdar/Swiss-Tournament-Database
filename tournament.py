#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def dbQuery(query, fetchQuery=None):
    """This is a common method used for running query operations"""
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    if fetchQuery is not None:
        results = cur.fetchall()
    else:
        conn.commit()
    conn.close()
    if fetchQuery is not None:
        return results


def dbQuery_with_args(query, params=None):
    """This is a common method used for running query operations"""
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    dbQuery("DELETE FROM matches")


def deletePlayers():
    """Remove all the player records from the database."""
    dbQuery("DELETE FROM players")


def countPlayers():
    """Returns the number of players currently registered."""
    num = dbQuery("SELECT count(*) FROM players", True)
    return num[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
        
        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema, not in your Python code.)
        
        Args:
        name: the player's full name (need not be unique).
        """
    dbQuery_with_args("INSERT INTO players (name) VALUES (%s)", (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
        
        The first entry in the list should be the player in first place, or player
        tied for first place if there is currently a tie.
        
        Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
        """
    return dbQuery("select * from standings", True)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
        
        Args:
        winner:  the id number of the player who won
        loser:  the id number of the player who lost
        """
    dbQuery_with_args("insert into matches (winner, loser)" +
                      "values (%s,%s)", (winner, loser))


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
    standings = playerStandings()
    result = []
    for x in range(0, len(standings) - 1):
        if x % 2 == 0:
            result.append((standings[x][0], standings[x][1],
                           standings[x+1][0], standings[x+1][1]))
        else:
            x = x + 1
    return result
