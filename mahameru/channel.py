from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound
from .model.db_channel import *
from bson.json_util import dumps
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
import datetime

bp = Blueprint('channel', __name__,
                        template_folder='templates')

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mahamerudb']
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

@bp.route('/addchannel',methods=['POST']) 
def add_channel(): 
    form = request.form
    channel = {}
    channel["name"] = form['name']
    channel["desc"] = form['description']
    channel["owner"] =form['owner_id']
    channel["members"] = form['members_id']
    channel["createdate"] = datetime.datetime.now() # ini diganti jadi system yg ambil

 
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
def updatechannel(id): # kelar
    form = request.form
    channel = {}
    channel["name"] = form['name']
    channel["desc"] = form['description']
    channel["owner"] =form['owner']
    channel["createdate"] = datetime.datetime.now()
    #current_app.logger.debug(id)


    if form['name']:
        count = update_channel(id, channel) # db_channel belum benar
       
        #current_app.logger.debug(_id)
        return str(count)
        #return
    else:
        return "Failed to update channel"

'''
Feedback : 
    1. Nama route ubah ke /channel untuk mencerminkan fungsi
'''
@bp.route('/channels')#tampilin channel (kelar)
def channel_all():
    channel = get_channel()
    resp = dumps(channel)
    return resp
'''
Feedback : 
    1. Nama route ubah ke channel/<id> untuk mencerminkan fungsi
    2. Jika tidak ada channel yg ditemukan, kembalikan string "Tidak ada channel dengan objectID yang dicari"
'''

@bp.route('/channel/<id>') # tampilin channel sesuai dengan channel ID
def channel_one(id):
    channel = get_channel_wID(id)
    resp = dumps(channel)
    return resp

@bp.route('/list_channels', methods=['POST'])
def list_channels():
  data = request.form
  member_channels = db.channel_members.find({'member_id': data['member_id']})
  member_channel_ids = [channel['channel_id'] for channel in member_channels]
  owner_channels = db.channels.find({'owner_id': data['owner_id']})
  owner_channel_ids = [channel['_id'] for channel in owner_channels]
  all_channel_ids = member_channel_ids + owner_channel_ids
  return 'Daftar channel: ' + ', '.join(all_channel_ids)


@bp.route('/add_channel_member', methods=['POST'])
def add_channel_member():
  data = request.form
  new_channel_member = {
    'channel_id': data['channel_id'],
    'member_id': data['member_id']
  }
  result = db.channel_members.insert_one(new_channel_member)
  if result.acknowledged:
    return 'Channel member berhasil ditambahkan!'
  else:
    return 'Gagal menambahkan channel member!'

@bp.route('/remove_channel_member', methods=['POST'])
def remove_channel_member():
  data = request.form
  result = db.channel_members.delete_one({'channel_id': data['channel_id'], 'member_id': data['member_id']})
  if result.deleted_count > 0:
    return 'Channel member berhasil dihapus!'
  else:
    return 'Gagal menghapus channel member!'


@bp.route('/deletechannel/<id>',methods=['DELETE']) # hapus channel sesuai dengan user ID
def deletechannel(id):
    channel = delete_channel(id)
    resp = dumps(channel)
    return resp