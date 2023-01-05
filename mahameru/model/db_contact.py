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
def get_contact(filter={}):
    collection = get_collection("contact")
    return collection.find(filter)

def get_contact_wID(id):
    collection = get_collection("contact")
    result = collection.find_one({"_id": ObjectId(id)})
    return collection.find(result)

def insert_contact(contact):
    collection = get_collection("contact")
    result = collection.insert_one(contact)
    return result.inserted_id


def update_contact(id, contact):
    # param 1 > user_old , param 2 > user_new
    collection = get_collection("contact")
    current_app.logger.debug(id)
    current_app.logger.debug(contact)
   
    result = collection.update_one({"_id": ObjectId(id)},  { "$set": contact }, upsert=False)
    return result.matched_count    

def delete_contact(id):
    collection = get_collection("contact")
    result = collection.delete_one({"_id": ObjectId(id)})
    return  "user has been deleted"


#def close_db(e=None):
    #db = g.pop(current_app.config['DATABASE'], None)
    #if db is not None:
        #db.close()
        

