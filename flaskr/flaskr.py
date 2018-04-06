import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    return render_template('wiki.html')

@app.route('/predict', methods=['POST'] )
def predict():
    if 'image_url' in request.form:
        return jsonify(
            predict = 'true',
            predict_hash = "asdadas12312312",
        )
    else:
        return jsonify(
                message = "Invalid 'image_url' parameter"
        )

@app.route('/predict/<predict_hash>', methods=['PUT'])
def correct_predict(predict_hash=None):
    if 'correct' in request.form:
        correct = str(request.form['correct'])

        if correct in ("true", "false"):
            return jsonify(
                status = correct,
                correct = correct,
                predict_hash = predict_hash,
            )
        else:
            return jsonify(
                message = "Invalid 'true' or 'false' entries."
            )
    else:
        return jsonify(
                message = "Please, give your opinion"
        )

@app.errorhandler(404)
def page_not_found(error):
    return redirect('/'), 302
