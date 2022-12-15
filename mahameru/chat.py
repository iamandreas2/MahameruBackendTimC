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

@bp.route('/chats')
def join_table():
    joined = get_chat_collection()
    hasil = dumps(joined)
    current_app.logger.debug(hasil)
    return hasil

@bp.route('/sendchat', methods=['POST'])
def send_chat():
    try:
        form = request.form 
        chat = {}
        chat["to_user"] = ObjectId(form['to_user'])
        chat["from_user"] = ObjectId(form['from_user'])
        chat["message"] = form['message']
        chat["created_at"] = datetime.datetime.now()

        if request.method == "POST" and form['message']:
            _id = sendchat(chat)
            resp = dumps(_id)
            current_app.logger.debug(_id)
            return resp
        else:
            return "Unable to send chat"
    except:
        return "check if the inputted data is correct"
    
@bp.route('/getchats')
def chat_all():
    chats = get_byAll()
    resp = dumps(chats)
    return resp

@bp.route('/getchat/id')
def chat_byID():
    form = request.form
    chatID = form['_id']
    conv = ObjectId(chatID)
    chats = get_byID(conv)
    resp = dumps(chats)
    return resp

@bp.route('/deletechat', methods=['DELETE'])
def delete_chat():
    form = request.form
    chatID = form['_id']
    conv = ObjectId(chatID)
    chats = deletechat(conv)
    resp = dumps(chats)
    return resp

if __name__ == "__main__":
    bp.run(debug=True)
