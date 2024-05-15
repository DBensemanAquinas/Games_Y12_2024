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


@app.route('/')
def render_home():
    """ display the home page """
    return render_template("index.html")

@app.route("/games")
def render_games():
    type = request.args.get('type')
    sort = request.args.get('sort')
    query = "SELECT * FROM game"
    if sort is not None:
        query = query + " ORDER BY " + sort
    conn = create_connection(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    games = cur.fetchall()
    conn.close()
    return render_template("games.html", games=games, type=type)


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
    type = "list"
    return render_template("games.html", games=games, type=type)

if __name__ == '__main__':
    app.run()
