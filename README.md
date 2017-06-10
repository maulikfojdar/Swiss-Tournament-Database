# Swiss Tournament Pairings 
Make pairings of players for Swiss-style game tournament using Python and a PostgreSQL database.

## Initialization
To initialize the required tables, run:

```
$ psql -f tournament.sql
```

To run a suite of unit tests,

```
$ python tournament_test.py
```

## Tables available

**players**

Includes the player's name and ID number.

**matches**

ALL match results are recorded here with a match ID numer and the resulting winner or loser.

**wins** _(view)_

Keeps track of the number of wins for each player.

**matchesplayed** _(view)_

Keeps track of the number of matches played by each player.

**standings** _(view)_

Keeps track of the rankings of each player based on wins and number of matches played and ordered by ranking.

## Running a tournament

Use the available Python functions, we can play the game:

METHOD | ACCEPTS | PURPOSE
--- | --- | ---
registerPlayer(name) | _name as string_ | Adds a player to the database to be calculated in pairings and standings.
countPlayers() | _(no input)_ | Counts all registered players.
swissPairings() | _(no input)_ | Returns a list of players grouped into pairs, arranged according to their current standings. Players are paired with those with about the same number of wins.
reportMatch(winner, loser) | _winner as string_, _loser as string_ | Records the result of any given match. 
playerStandings() | _(no input)_ | Returns the number of wins from all players. 
