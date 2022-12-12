from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound
from .model.db_channel import *
from bson.json_util import dumps
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

bp = Blueprint('channel', __name__,
                        template_folder='templates')

''''
Feedback : 
    1. Check database diagram, field yg wajib diisi
    2. Untuk route ini pada key created_at dan updated_at digenerate oleh sistem
    3. Akses ke database untuk simpan data seharusnya dipisahkan kedalam file terpisah
    4. Konfigurasi baca dari settings.cfg
    5. Kembalikan ObjectID dari data yg telah diinsert
    6. Jangan pergunakaan request.json untuk post namun pergunakan request.form.
    7. Nama route diganti dengan /addchannel.
'''

@bp.route('/addchannel',methods=['POST']) # KELAR
def add_channel(): #YANG BENER
    form = request.form
    channel = {}
    channel["name"] = form['name']
    channel["desc"] = form['description']
    channel["owner"] =form['owner_id']
    channel["members"] = form['members_id']
    channel["createdate"] = form['created_at'] # ini diganti jadi system yg ambil

    if request.method == "POST" and form['name']:
        _id = insert_channel(channel)
        resp = dumps(_id)
        current_app.logger.debug(_id)
        return resp
    else:
        return "Unable to store data into database"

'''
Feedback : 
    1. Check database diagram, field yg wajib diisi
    2. Untuk route ini pada key created_at dan updated_at digenerate oleh sistem
    3. Akses ke database untuk simpan data seharusnya dipisahkan kedalam file terpisah
    4. Konfigurasi baca dari settings.cfg
    5. Pada kondisi " if " pastikan checking kondisinya benar
    6. Kembalikan ObjectID untuk row yang berhasil di update sebagai json
    7. Nama route ubah ke updatechannel/<id> untuk mencerminkan fungsi
'''

@bp.route('/updatechannel/<id>',methods=['PUT']) # jadiin update channel
def update_channel(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _desc = _json['description']
    _owner = _json['owner_id']
    _members = _json['members_id']

    if _name and _desc and _owner and _members and request.method == "PUT":
        mongo = PyMongo(current_app)
        mongo.db.channel.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'description':_desc,'owner_id:': _owner, "members_id" : _members}})
        resp = jsonify("User updated successfully")
        resp.status_code = 200
        return resp
    else:
        return 

'''
Feedback : 
    1. Nama route ubah ke /channel untuk mencerminkan fungsi
'''

@bp.route('/channel') #tampilin channel (kelar)
def channel_all():
    mongo = PyMongo(current_app)
    channel = mongo.db.channel.find()
    resp = dumps(channel)
    return resp

'''
Feedback : 
    1. Nama route ubah ke channel/<id> untuk mencerminkan fungsi
    2. Jika tidak ada channel yg ditemukan, kembalikan string "Tidak ada channel dengan objectID yang dicari"
'''

@bp.route('/channel/<id>') # tampilin channel sesuai dengan channel ID
def channel_one(id):
    mongo = PyMongo(current_app)
    channel = mongo.db.channel.find_one({'_id':ObjectId(id)})
    resp = dumps(channel)
     return resp
    else:
        return "There is no channel with the objectID being searched for"

'''
Feedback : 
    1. Nama route ubah ke deletechannel/<id> untuk mencerminkan fungsi
'''
@bp.route('/deletechannel/<id>',methods=['DELETE']) # hapus channel sesuai dengan channel ID
def delete_channel(id):
    mongo = PyMongo(current_app)
    _id = mongo.db.channel.delete_one({'id':ObjectId(id)})
    resp = jsonify("channel deleted successfully")
    resp.status_code = 200
    return resp