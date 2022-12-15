import click
import pymongo
from flask import current_app, g, request, jsonify
from flask.cli import with_appcontext
from bson.son import SON
from bson.json_util import dumps
from bson.objectid import ObjectId

def get_db():
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]

def get_chat_collection():
    col = get_collection("chat")
    pipeline = [ {"$lookup" : {"from" : "user", "localField" : "to_user", "foreignField" : "_id", "as": "chat_details" } }]
    data = col.aggregate(pipeline)
    current_app.logger.debug(data)
    return data

def deletechat(id):
    collection = get_collection("chat")
    result = collection.delete_one({"_id" : ObjectId(id)})
    print(str(id) + " been deleted")
    return id

def sendchat(chat):
    collection = get_collection("chat")
    result = collection.insert_one(chat)
    return result.inserted_id

def get_byID(id):
    collection = get_collection("chat")
    result = collection.find_one({"_id" : ObjectId(id)})
    return collection.find_one(result)

def get_byDate(chat):
    collection = get_collection("chat")
    result = collection.insert_one(chat)
    return result.inserted_id

def get_byAll():
    collection = get_collection("chat")
    result = collection.find({}, {"_id" : 0})
    return list(result)