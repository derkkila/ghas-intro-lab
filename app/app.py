"""Intentionally insecure demo app for the GHAS intro lab. Do not deploy."""
import os
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "library.db")
NOTES_DIR = os.path.join(BASE_DIR, "notes")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return jsonify({"endpoints": ["/books?title=<text>", "/notes?name=<file>"]})


@app.route("/books")
def search_books():
    title = request.args.get("title", "")
    # FLAW 1: user input is pasted straight into the SQL statement (SQL injection)
    query = "SELECT id, title, author FROM books WHERE title LIKE '%" + title + "%'"
    rows = get_db().execute(query).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/notes")
def read_note():
    name = request.args.get("name", "")
    # FLAW 2: user input builds a file path (path traversal, e.g. ../../etc/passwd)
    path = os.path.join(NOTES_DIR, name)
    with open(path) as f:
        return f.read()


if __name__ == "__main__":
    # FLAW 3: debug mode exposes an interactive debugger to anyone who can reach the app
    app.run(host="0.0.0.0", debug=True)
