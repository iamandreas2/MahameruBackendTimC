import click
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId 
from flask import current_app, g, session
from flask.cli import with_appcontext
from itertools import chain


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
def insert_user(user):
    collection = get_collection("user")

    #_id = mongo.db.user.insert_one({"userid": _userid, "name": _name, "nickname": _nickname ,"notelp": _notelp, "pin" : _pin, "created_at" : createdat,  "contact_id" : contactid })
    result = collection.insert_one(user)
    return result.inserted_id

def login_user(user):
    session['name'] = user['name']
    session['nickname'] = user['nickname']
    session['notelp'] = user['notelp']

def user_exists(nickname):
    collection = get_collection("user")
    # Query the database to see if a user with the given nickname already exists
    result = collection.find_one({"nickname": nickname})
    return result is not None

def get_user_wID(id):
    collection = get_collection("user")
    result = collection.find_one({"_id": ObjectId(id)})
    return collection.find(result)

def get_user_by_phoneno(phoneno):
    collection = get_collection("user")
    # Build the query dictionary using the nickname parameter
    query = {'notelp': phoneno}
    # Query the database for documents that match the query
    result = collection.find(query)
    return result

def get_user_by_nickname(nickname):
    collection = get_collection("user")
    # Build the query dictionary using the nickname parameter
    query = {'nickname': nickname}
    # Query the database for documents that match the query
    result = collection.find(query)
    return result

def get_user_by_partial_nickname(nickname):
    collection_user = get_collection("user")
    collection_contact = get_collection("contact")
    query = {"$or": [
        {"nickname": {"$regex": "^" + nickname, "$options": "i"}},
        {"nickname": {"$regex": "^" + nickname, "$options": "i"}}
    ]}
    cursor = collection_user.find(query)
    cursor_contact = collection_contact.find(query)
    result = []
    for doc in cursor:
        doc['source'] = 'user'
        result.append(doc)
    for doc in cursor_contact:
        doc['source'] = 'contact'
        result.append(doc)
    return result



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


    
