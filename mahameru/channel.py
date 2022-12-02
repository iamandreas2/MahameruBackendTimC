from flask import Flask, jsonify, request
import uuid
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from editchannel import *

bp = Blueprint('channel', __name__,
                        template_folder='templates')


# placeholder data
'''user = {
    'userid': '',
    'name': '',
    'no_telp': '',
    'pin': '',
    'created_at': '',
    'updated_at': '',
    'contact_id': ''
}'''

# User 
@bp.route('/get', methods=['GET'])
def getchannel():
    data = getchannel()
    return data

# TODO : fix this so it match with the given docs

@bp.route('/createchannel', methods=['POST'])
def createchannel():
        try:
            # for testing purpose only getting one request json
            bp['name'] = request.json['channel']
            bp['created_at'] = request.json['created_at']
            bp['updated_at'] = request.json['updated_at']
            bp['userid'] = uuid.uuid4()

            response = jsonify({'id' : bp['channel.id']})
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify({'message' : 'Failed to create channel'})
            response.status_code = 400
        finally:
            return response

# TODO : dont modify it untill the above route is fixed
@bp.route('/createchannel', methods=['PUT'])
def edituser():
        try:
            bp['channel.id'] = request.json['channel.id']
            bp['name'] = request.json['name']
            bp['updated_at'] = request.json['updated_at']

            response = jsonify({'id' : bp['channel.id']})
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify({'message': 'Failed to create channel'})
            response.status_code = 400
        finally:
            return response

@bp.route('/createchannel/<string:channel_id>', methods=['GET'])
def newchannel(channel_id):
    try:
        # this code must be changed after implementing the database
        if channel_id == '2c535c8b-5d2b-4a72-9268-1c83aaf61902':
            response = jsonify({'Channel': 'Group 1'})
            response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Failed to get channel'})
        response.status_code = 400
    finally:
        return response

@bp.route('/delchannel', methods=['DELETE'])
def deletechannel():
    # this code must be fixed after implmenting the database and getting clarity from director
    return jsonify({'mesage' : 'deleting the channel that you want'})

if __name__ == "__channel__":
        bp.run(debug=True)