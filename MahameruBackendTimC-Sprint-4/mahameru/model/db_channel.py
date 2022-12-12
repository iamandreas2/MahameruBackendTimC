import click
import pymongo
from bson.json_util import dumps
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
Helper function to query all contact on system 
"""
def insert_channel(channel):
    collection = get_collection("channel")
    #_id = mongo.db.channel.insert_one({"channelid": _channelid, "name": _name, "nickname": _nickname ,"notelp": _notelp, "pin" : _pin, "created_at" : createdat,  "contact_id" : contactid })
    result = collection.insert_one(channel)
    return result.inserted_id

def get_channel_wID(id):
    collection = get_collection("channel")
    result = collection.find_one({'_id':ObjectId(id)})
    resp = dumps(channel)

def update_channel(channel):
    # param 1 > channel_old , param 2 > channel_new
    collection = get_collection("channel")
    result = collection.update_one(channel_old, channel)
    