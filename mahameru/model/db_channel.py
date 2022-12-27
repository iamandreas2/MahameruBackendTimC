import click
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import current_app, g
from flask.cli import with_appcontext
from pymongo import MongoClient


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
Helper function to query all contact on system 
"""
def insert_channel(channel):
    collection = get_collection("channel")
    result = collection.insert_one(channel)
    return result.inserted_id

def get_channel_wID(id):
    collection = get_collection("channel")
    result = collection.find_one({"_id":ObjectId(id)})
    return collection.find(result)

def get_channel(filter={}):
    collection = get_collection("channel")
    return collection.find(filter)

def update_channel(id,channel):
    # param 1 > channel_old , param 2 > channel_new
    collection = get_collection("channel")
    current_app.logger.debug(id)
    current_app.logger.debug(channel)
    result = collection.update_one({"_id":ObjectId(id)},{"$set":channel},upsert=False)
    return result.matched_count


def delete_channel(id):
    collection = get_collection("channel")
    result = collection.delete_one({"_id": ObjectId(id)})
    return  "channel has been deleted"
  
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
    #app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)