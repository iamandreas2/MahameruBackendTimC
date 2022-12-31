from flask import Flask, jsonify, request, current_app
import uuid
import datetime
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from .model.db_chat import *
from flask_pymongo import PyMongo
import datetime

bp = Blueprint('chat', __name__,
                        template_folder='templates')

@bp.route('/getchat/all')
def get_chats():
    chats = get_byAll()
    result = dumps(chats)
    return result

#.strftime("%m/%d/%Y, %H:%M:%S")
@bp.route('/sendchat', methods=['POST'])
def send_chat():
    date = datetime.datetime.now().isoformat()
    date_time = date
    json = request.json 
    telp = json['telp']
    from_user = json['from_user']
    message = json['message']
    sent = date_time

    if request.method == "POST":
        _id = sendchat(telp, ObjectId(from_user), message, sent)
        chat = dumps(_id)
        resp = "chat _id : " + chat
        current_app.logger.debug(_id)
        return resp
    else:
        return "Unable to send chat"
    # except:
    #     return "failed to send chat"

@bp.route('/getchat/id/<id>')
def chatbyID():
    conv = ObjectId(id)
    chats = getbyID(conv)
    resp = dumps(chats)
    return resp

@bp.route('/getchat/nick/<nickname>')
def chat_byNickname(nickname):
    chats = get_byNick(nickname)
    resp = dumps(chats)
    return resp

@bp.route('/updatechat/<id>', methods = ['PUT'])
def updatechat(id):
    json = request.json
    chat = {}
    chat["message"] = json['message']
    chat["update_at"] = datetime.datetime.now()

    if json['message']:
        _id = update_chats(id, chat)
        resp = dumps(_id)
        return resp
    else:
        return "Failed to update chat"

@bp.route('/deletechat/<id>', methods=['DELETE'])
def deletechat(id):
    chat = delete_chat(id)
    resp = dumps(chat)
    return resp

@bp.route('/channelmessages/<id>', methods=['GET'])
def listchannels(id):
    conv = ObjectId(id)
    chats = get_channel_messages(conv)
    answer = dumps(chats)
    return answer

# ini untuk diplay message pada messaging system
# a = from_user. input sendiri (logged in user)
@bp.route('/chatwith/<telp>')
def get_personal_telp(telp):
    a = '63a57ff9381277a6d7336e4d'
    to_user = telp
    from_user = a
    chats = get_chatwith_telp(to_user, from_user)

    # Initialize an empty list to store the chat messages
    chat_messages = []

    # Iterate over the cursor and extract the chat messages
    # with the sender and recipient information
    for chat in chats:
        if chat['from_user'] == from_user:
            sender_data = chat['sender data'][0]
            recipient_data = chat['reciever data'][0]
        else:
            sender_data = chat['reciever data'][0]
            recipient_data = chat['sender data'][0]
        chat_message = {
            'message': chat['message'],
            'sent': chat['sent'],
            'status': chat['status'],
            'sender': sender_data['name'],
            'recipient': recipient_data['name'],
        }
        chat_messages.append(chat_message)

    # Serialize the list of chat messages as a JSON string
    resp = json.dumps(chat_messages)
    return resp

# @bp.route('/getinfo/<val>')
# def find_info(val):
#     current_app.logger.debug("start :")
#     find = find_user_and_chat(val)
#     resp = dumps(find)
#     current_app.logger.debug(resp)
#     current_app.logger.debug(find)
#     return resp

@bp.route('/getinfo/<val>', methods=['GET'])
def find_info(val):
        chat_cursor = find_chat(val)
        user_cursor = find_friend(val)
        if chat_cursor and user_cursor:
            # Convert ObjectId objects to strings
            chat_list = [{k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()} for doc in chat_cursor]
            user_list = [{k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()} for doc in user_cursor]
            result = chat_list + user_list
            if len(result) != 0:
                return jsonify(result)
            else:
                return "nothing was found"

    
#display chat pada inbox sesuai dengan user dan message terbaru
@bp.route('/inbox/<user_id>', methods=['GET'])
def inbox(user_id):
    resp = display_inbox(user_id)
    return dumps(resp)
    
if __name__ == "__main__":
    bp.run(debug=True)