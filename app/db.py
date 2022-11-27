import click
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]


def init_db_command():    
    init_db()
    click.echo('database tidak ditemukan')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)