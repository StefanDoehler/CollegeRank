import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
import database
from web_scrapers import *
from data_manipulation import *
import sys

#create the application
app = Flask(__name__)
app.config.from_object(__name__)

#Load default configuration and override configuration from envvar
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='xxxxxx',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def scrape_websites():
    data_sets = []
    possible_data_sets = [
        scrape_best_colleges(),
        scrape_niche(),
        scrape_us_news(),
        scrape_college_raptor(),
        scrape_best_schools()
    ]

    for ds in possible_data_sets:
        if isinstance(ds, dict):
            data_sets.append(ds)
        else:
            print ds + " is broken"  # the broken url is returned from scraper in the case of failure

    school_list = combine_data_sets(data_sets)

    if school_list is None:
        print "Data set is broken"
        sys.exit(1)

    proper_names = parse_school_names(school_list)
    final_list = calculate_average_rank_and_location(proper_names)
    database.delete_tables()
    database.create_schema()

    con = database.connect_db()
    cursor = con.cursor()
    for name, info in final_list.iteritems():
        if not info[0]:
            continue
        database.add_school(name, info, con, cursor)

    cursor.close()
    con.close()


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource("schema.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print "Initalized the database"

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    schools = database.query_all_schools(75)
    print schools
    return render_template('show_entries.html', entries=entries, schools=schools)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

app.run()
