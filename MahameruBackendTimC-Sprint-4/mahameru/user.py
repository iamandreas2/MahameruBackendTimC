from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound
from .model.db_contact import *
from bson.json_util import dumps
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

bp = Blueprint('contact', __name__,
                        template_folder='templates')

'''
    Feedback : 
    1. Check database diagram, field yg wajib diisi
    2. Untuk route ini pada key created_at dan updated_at digenerate oleh sistem
    '''

@bp.route('/createcontact',methods=['POST']) # KELAR
def add_contact():
    form = request.form
    contact = {}
    contact["name"] = form['name']
    contact["nickname"] = form['nickname']
    contact["notelp"] =form['notelp']
    contact["pin"] = form['pin']
    #contact["createdate"] = form['created_at'] # ini diganti jadi system yg ambil
    #contact["contactid"] = form['contact_id']

    if form['name']:
        count = insert_contact(contact)
        resp = dumps(count)
        current_app.logger.debug(count)
        return resp
    else:
        return "Unable to store data into database"


'''
    Feedback : 
    1. Check database diagram, field yg wajib diisi
    2. Untuk route ini pada key created_at dan updated_at digenerate oleh sistem
    3. Akses ke database untuk simpan data seharusnya dipisahkan kedalam file terpisah
    4. Konfiguras baca dari settings.cfg
    5. Pada kondisi " if " pastikan checking kondisinya benar
    6. Kembalikan ObjectID untuk row yang berhasil di update sebagai json
    7. Nama route ubah ke updatecontact untuk mencerminkan tujuan
    8. Field updated_at ditarik dari datesystem tanpa menyentuh existing data di field created_at
    
'''

@bp.route('/updatecontact/<id>', methods = ['PUT'])
def updatecontact(id): # kelar
    form = request.form
    contact = {}
    contact["name"] = form['name']
    contact["nickname"] = form['nickname']
    contact["notelp"] =form['notelp']
    contact["pin"] = form['pin']
    #contact["updatedate"] = form['created_at'] # ini juga sistem yang input
    #contact["contactid"] = form['contact_id']

    #current_app.logger.debug(id)


    if form['name']:
        count = update_contacts(id, contact) # db_contact belum benar
       
        #current_app.logger.debug(_id)
        return str(count)
        #return
    else:
        return "Failed to update contact"


'''
    Feedback :
    1. nama route ganti ke /contacts
    2. Jika tidak ada contact yg ditemukan, kembalikan string "Tidak ada contact"
'''

@bp.route('/contacts') #tampilin contact (kelar)
def contact_all():
    contact = get_contact()       
    resp = dumps(contact)
    return resp

'''
    Feedback :
    1. Jika tidak ada contact yg ditemukan, kembalikan string "Tidak ada contact dengan objectID yang dicari"
'''

@bp.route('/contact/<id>') # tampilin contact sesuai dengan contact ID
def contact_one(id):
    contact = get_contact_wID(id)
    resp = dumps(contact)
    return resp


'''
    Feedback :
    1. Nama route ganti ke /deletecontact
    2. check filter query delete row karena row yang diingikan tidak terhapus
'''
@bp.route('/deletecontact/<id>',methods=['DELETE']) # hapus contact sesuai dengan contact ID
def deletecontact(id):
    contact = delete_contact(id)
    resp = dumps(contact)
    return resp
