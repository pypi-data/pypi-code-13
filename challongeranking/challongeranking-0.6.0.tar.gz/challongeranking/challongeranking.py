import challonge
import os.path
import sqlite3

# The rating that previously unrated players start at
_new_player_rating = 1200


def setCredentials(username, apikey):
    challonge.set_credentials(username, apikey)


def processTournament(tournamentName, dbName):
    """Calculate new ratings for a single tournament.

    Goes through all matches of a tournament and calculates changes in
    participant ratings throughout the tournament.

    Arguments:
        tournamentName:
            tournament name (e.g. 'mytournament' if the tournament
            URL is 'challonge.com/mytournament').
            If the tournament is in a sub-domain then the argument should be
            of form 'subdomain-tournament' (e.g. myorganisation-mytournament
            for 'myorganisation.challonge.com/mytournament')

        dbName:
            database filename.
            If the file doesn't exist, it will be created.
    """

    global __player_cache, __rating_cache
    __player_cache = dict()
    __rating_cache = dict()

    if not os.path.exists(dbName):
        db = __createDatabase(dbName)
    else:
        db = sqlite3.connect(dbName)

    # Do not process tournaments that have already been processed
    tournament = challonge.tournaments.show(tournamentName)
    if __find_tournament(tournament['id'], db) == True:
        return

    players = challonge.participants.index(tournament['id'])
    for player in players:
        __player_cache[player['id']] = player
        __update_player_name(db, player)
        __add_participation(db, tournament, player)

    for match in challonge.matches.index(tournament['id']):
        __process_match(match, db)

    __add_tournament(tournament['id'], db)
    db.commit()
    db.close()


def __add_participation(db, tournament, player):
    if player['email-hash'] is not None:
        c = db.cursor()
        c.execute('INSERT INTO participations VALUES (?,?)',
                  (tournament['id'], player['email-hash']))


def __process_match(match, db):
    c = db.cursor()
    player1 = __player_cache[match['player1-id']]
    player2 = __player_cache[match['player2-id']]

    if player1['email-hash'] is None or player2['email-hash'] is None:
        return

    if match['winner-id'] == player1['id']:
        winner = 0
    else:
        winner = 1

    p1_rating = __player_rating(player1, db)
    p2_rating = __player_rating(player2, db)

    p1_new_rating, p2_new_rating = __update_ratings((p1_rating, p2_rating),
                                                    winner)
    c.execute('UPDATE players SET rating=? WHERE id=?',
              (p1_new_rating, player1['email-hash']))
    c.execute('UPDATE players SET rating=? WHERE id=?',
              (p2_new_rating, player2['email-hash']))

    __rating_cache[player1['id']] = p1_new_rating
    __rating_cache[player2['id']] = p2_new_rating


def __player_rating(player, db):
    """Returns the rating of a player.
    Arguments:
        player = the player as returned by the challonge API
        db = previously opened database connection
    """
    key = player['id']
    if key not in __rating_cache:
        c = db.cursor()
        c.execute('SELECT rating FROM PLAYERS WHERE id=?',
                  (player['email-hash'],))
        rating = c.fetchone()[0]
        __rating_cache[key] = rating
    else:
        rating = __rating_cache[key]

    return rating


def __add_tournament(tournament_id, db):
    c = db.cursor()
    c.execute('INSERT INTO tournaments VALUES(?)', (tournament_id,))


def __find_tournament(tournament_id, db):
    c = db.cursor()
    c.execute('SELECT id FROM tournaments WHERE id=?', (tournament_id,))

    return c.fetchone() is not None


def __update_ratings(old_ratings, winner):
    """Calculate new ratings for players.

    Args: ratings - tuple of current player ratings before match
    winner - index of the winner's rating
    (i.e. 0 = player1 and 1 = player2)

    Returns a tuple containing new ratings.
    """
    r1, r2 = old_ratings
    R1 = 10 ** (r1 / 400)
    R2 = 10 ** (r2 / 400)
    E1 = R1 / float(R1 + R2)
    E2 = R2 / float(R1 + R2)

    S1 = 0
    S2 = 0
    if winner == 0:
        S1 = 1
    else:
        S2 = 1

    K = 32
    p1_new_rating = int(round(r1 + K * (S1 - E1)))
    p2_new_rating = int(round(r2 + K * (S2 - E2)))

    return (p1_new_rating, p2_new_rating)


def __update_player_name(db, player):
    """Keeps list of names (aliases) used by a player up to date.

    Arguments:
        db - previously opened database connection
        player - the player as returned by challonge API
    """
    c = db.cursor()
    id = player['email-hash']

    if player['name'] is not None:
        player_tournament_name = player['name']
    else:
        player_tournament_name = player['challonge-username']

    c.execute('SELECT id FROM players WHERE id=?', (id,))
    row = c.fetchone()
    if row is None:
        new_player_record = (player['email-hash'],
                             player_tournament_name,
                             _new_player_rating)
        c.execute('INSERT INTO players VALUES(?,?,?)', new_player_record)
    else:
        c.execute('SELECT nick FROM players WHERE id=?', (id,))
        stored_name = c.fetchone()[0]
        if stored_name != player_tournament_name:
            c.execute('SELECT alias FROM aliases WHERE player_id=?', (id,))
            if c.fetchone() is None:
                c.execute('INSERT INTO aliases VALUES(?,?)',
                          (player_tournament_name, id))


def __createDatabase(dbName):
    """Sets up a fresh sqlite3 database with the filename dbName.
    Returns a connection to the created database.
    """

    newdb = sqlite3.connect(dbName)
    c = newdb.cursor()

    queries = [
        "CREATE TABLE players(id TEXT PRIMARY KEY, nick TEXT, rating INT)",

        "CREATE TABLE aliases(alias TEXT, player_id TEXT,"
        " FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE)",

        "CREATE TABLE tournaments(id INT PRIMARY KEY)",

        "CREATE TABLE participations(player_id INT, tournament_id INT,"
        " FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE,"
        " FOREIGN KEY(tournament_id) REFERENCES tournaments(id)"
        " ON DELETE CASCADE)"
    ]
    for query in queries:
        c.execute(query)
        newdb.commit()

    return newdb
