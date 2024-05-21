""" Game information """
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

DATABASE = "game_data.db"


def create_connection(db_file):
    """ Create a connection to the sql database
    Parameters: 
    db_file - The name of the file
    Returns: A connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)
    return None

def get_genres():
    query = "SELECT DISTINCT genre FROM game"
    conn = create_connection(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    genres = cur.fetchall()
    conn.close()
    for genre in genres:
        print(genre['genre'])
    return genres


@app.route('/')
def render_home():
    """ display the home page """
    return render_template("index.html", genres=get_genres())

@app.route("/games")
def render_games():
    type = request.args.get('type')
    sort = request.args.get('sort')
    genre = request.args.get('genre')

    query = "SELECT * FROM game"
    if genre is not None:
        query = query + " WHERE genre = ?"
    if sort is not None:
        query = query + " ORDER BY " + sort
    conn = create_connection(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if genre is None:
        cur.execute(query)
    else:
        cur.execute(query, (genre, ))
    games = cur.fetchall()
    conn.close()
    return render_template("games.html", games=games, type=type, genres=get_genres())


@app.route("/search")
def render_search():
    search = request.args.get('search')
    query = "SELECT * FROM game WHERE title LIKE ? OR platform LIKE ? OR genre LIKE ? OR publisher LIKE ?"
    search = "%" + search + "%"
    conn = create_connection(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (search, search, search, search))
    games = cur.fetchall()
    conn.close()
    type = "table"
    return render_template("games.html", games=games, type=type)

if __name__ == '__main__':
    app.run()
