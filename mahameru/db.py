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

"""
Helper function to query all user on system 
"""
def get_channel(filter={}):
    collection = get_collection("channel")
    return collection.find(filter)

def get_channel(filter={}):
    collection = get_collection("channel")
    return collection.find_one(filter)

def create_channel(data):
    collection = get_collection("channel")
    row = collection.create_one(data)
    return row

def update_channel(filter, update):
    collection = get_collection("channel")    
    return collection.update_one(filter, update)    

def delete_channel(data):
    collection = get_collection("channel")
    collection.delete_one(data)

def channel_id(channel{}):
    collection = channel_id("Member")
    return collection.find(channel)

def channel_id(editchannel={}):
    collection = get_collection("id channel")
    return collection.find(editchannel)

def Created_at(editchannel={}):
    collection = get_collection("dibuat")
    return collection.created_one(editchannel)

def Updated_at(editchannel={}):
    collection = get_collection("diupdate")
    row = collection.update_one(editchannel)
    return row
    
def close_db(e=None):
    db = g.pop(current_app.config['DATABASE'], None)
    if db is not None:
        db.close()
        
def init_db():
    """clear the existing data and create new tables."""    
    db = get_db()    
    db.client.drop_database(current_app.config['DATABASE'])
    
@click.command('init-db')
@with_appcontext
def init_db_command():    
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

