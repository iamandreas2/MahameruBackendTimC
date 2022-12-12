import click
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId 
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
def insert_user(id, user):
    collection = get_collection("user")
    #_id = mongo.db.user.insert_one({"userid": _userid, "name": _name, "nickname": _nickname ,"notelp": _notelp, "pin" : _pin, "created_at" : createdat,  "contact_id" : contactid })
    result = collection.insert_one(user)
    return result.inserted_id

def get_user_wID(id):
    collection = get_collection("user")
    result = collection.find_one({"_id": ObjectId(id)})
    return collection.find(result)

'''
    Todo : Find duplicate update user function
'''
def update_users(id, user):
    # param 1 > user_old , param 2 > user_new
    collection = get_collection("user")
    current_app.logger.debug(id)
    current_app.logger.debug(user)
   
    result = collection.update_one({"_id": ObjectId(id)},  { "$set": user }, upsert=False)
    return result.matched_count

def get_user(filter={}):
    collection = get_collection("user")
    return collection.find(filter)


def delete_user(id):
    collection = get_collection("user")
    result = collection.delete_one({"_id": ObjectId(id)})
    return  "user has been deleted"

    
