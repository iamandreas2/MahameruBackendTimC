from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
import uuid

'''Channel = {
    '_id' : '',
    'owner_id' : '',
    'members_id' : '',
    'name': '',
    'description: '',
    'created_at': '',
    'updated_at': '',
}'''

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/mahamerudb"
mongo = PyMongo(app)

@app.route('/add',methods=['POST']) # KELAR
def add_channel():
    _json = request.json
    _name = _json['name']
    _desc = _json['description']
    _owner = _json['owner_id']
    _members = _json['members_id']

    if _name and _desc and _owner and _members and request.method == "POST":
        _id = mongo.db.channel.insert_one({"name": _name,"desc": _desc, "owner_id" : _owner,  "members_id" : _members })
        resp = jsonify("channel Added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/update/<id>',methods=['PUT']) # jadiin update channel
def update_channel(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _desc = _json['description']
    _owner = _json['owner_id']
    _members = _json['members_id']

    if _name and _desc and _owner and _members and request.method == "PUT":
        mongo.db.channel.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'description':_desc,'owner_id:': _owner, "members_id" : _members}})
        resp = jsonify("User updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/show') #tampilin channel (kelar)
def channel_all():
    channel = mongo.db.channel.find()
    resp = dumps(channel)
    return resp

@app.route('/channel/<id>') # tampilin channel sesuai dengan channel ID
def channel_one(id):
    channel = mongo.db.channel.find_one({'_id':ObjectId(id)})
    resp = dumps(channel)
    return resp

@app.route('/delete/<id>',methods=['DELETE']) # hapus channel sesuai dengan channel ID
def delete_channel(id):
    _id = mongo.db.channel.delete_one({'id':ObjectId(id)})
    resp = jsonify("channel deleted successfully")
    resp.status_code = 200
    return resp

if __name__ == "__main__":
    app.run(debug=True)
