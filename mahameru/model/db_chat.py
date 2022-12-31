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


def idmatch(data):
    col = get_collection("user")
    pipeline = [{"$match": { "nickname" : data }},{"$lookup" : {"from": "chat", "localField": "_id", "foreignField": "from_user", "as": "sent chat" }}]
    data = col.aggregate(pipeline)
    return data

def number_match(number):
    col = get_collection("friend_profile")
    pipeline = [{"$match" : {"phone_number" : number}}, {"$lookup" : {"from" : "user", "localField" : 'user_id', "foreignField" : '_id', "as" : 'friend data'}}]
    data = col.aggregate(pipeline)
    data_list = list(data)
    a = data_list[0]
    b = a['friend data'][0]
    current_app.logger.debug(a)
    current_app.logger.debug(b)
    if a['phone_number'] == b["notelp"]:
        current_app.logger.debug("masuk ke if")
        status = "1"
    else:
        current_app.logger.debug("else mas")
        status = "0"
    return status
    
def sendchat(telp, from_user, message, created_at):
    collection = get_collection("chat")
    a = number_match(telp)
    if a == '1':
        result = collection.insert_one({"telp" : telp, "from_user" : from_user, "message" : message, "sent" : created_at, "status" : True})
    elif a == '0':
        result = collection.insert_one({"telp" : telp, "from_user" : from_user, "message" : message, "sent" : created_at, "status" : False})  
    return result.inserted_id

def update_chats(id, chat):
    # param 1 > chat_old , param 2 > chat_new
    collection = get_collection("chat")
    current_app.logger.debug(id)
    current_app.logger.debug(chat)
    result = collection.update_one({"_id": ObjectId(id)},  { "$set": chat }, upsert=False)
    return ObjectId(id)

def delete_chat(id):
    collection = get_collection("chat")
    result = collection.delete_one({"_id": ObjectId(id)})
    return ObjectId(id)

def getbyID(id):
    collection = get_collection("chat")
    result = collection.find_one({"_id" : ObjectId(id)})
    return collection.find_one(result)

def get_byAll():
    collection = get_collection("chat")
    result = collection.find({}, {"_id" : 0})
    return list(result)

def get_byNick(nick):
    collection = get_collection("chat")
    data = idmatch(nick)
    return list(data)

#route yang melisting message by channel id
def get_channel_messages(id):
    collection = get_collection("chat")
    result = collection.find({"to_user" : id}, {"_id" : 0})
    return result

# kode lama
#buat web api untuk listing chat by (a) user_from dan user_to, (b) baris message dan user_to
# def get_chatwith_id(reciever, sender):
#     collection = get_collection('chat')
#     current_app.logger.debug("info :")
#     current_app.logger.debug(reciever)
#     current_app.logger.debug(sender)
#     result = collection.find({"telp" : reciever, "from_user" : sender}, {"_id" : 0, "status" : 0})
#     current_app.logger.debug(result)
#     return result

def get_chatwith_telp(reciever, sender):
    collection = get_collection('chat')
    pipeline = [{"$match" : {"telp" : reciever, "from_user" : sender}}, {"$lookup" : {"from" : "user", "localField" : 'telp', "foreignField" : 'notelp', "as" : 'reciever data'}}]
    data = collection.aggregate(pipeline)
    current_app.logger.debug(data)
    return data

#find chat by value
# def find_user_chat(val):
#     collection = get_collection("chat")
#     collection2 = get_collection("friend_profile")
#     result = collection.find({"$text" : {"$search" : val}})
#     result2 = collection2.find({"$text" : {"$search" : val}})
#     resp = {}
#     resp["chat"] = dumps(result)
#     resp["Friends"] = dumps(result2)
#     current_app.logger.debug(resp)
#     return resp

#find chat by value
# def find_user_chat(val):
#     collection = get_collection("chat")
#     collection2 = get_collection("friend_profile")
#     pipeline = [{"$match" : {"$telp" :{"$search" : val}}}, {"$lookup" : {"from" : "user", "localField" : 'telp', "foreignField" : 'notelp', "as" : 'reciever data'}}]
#     result = collection.find({"$text" : {"$search" : val}})
#     result2 = collection2.find({"$text" : {"$search" : val}})
#     resp = {}
#     resp["chat"] = dumps(result)
#     resp["Friends"] = dumps(result2)
#     current_app.logger.debug(resp)
#     return resp

#filter chat in inbox by date
def display_inbox():
    collection = get_collection("user")
    pipeline = [{"$lookup": {"from": "chat", "let": {"user_id": "$_id"}, "pipeline": [{"$match": {"user_id": "$$user_id"}}, {"$sort": {"datetime": -1}}, {"$limit": 1}], "as": "latest_chat"}}]
    result = collection.aggregate(pipeline)
    return result

#find chat by value
def find_chat(val):
    collection = get_collection("chat")
    pros = {"message": {"$regex": "^" + val, "$options": "i"}}
    cursor = collection.find(pros)
    current_app.logger.debug(cursor)
    return cursor

def find_friend(val):
    collection = get_collection("friend_profile")
    pros = {"nama": {"$regex": "^" + val, "$options": "i"}}
    cursor = collection.find(pros)
    return cursor