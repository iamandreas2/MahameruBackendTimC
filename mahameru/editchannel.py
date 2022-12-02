from flask import Flask, jsonify, request
import uuid
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from channel import *

bp = Blueprint('bp', __name__,
                        template_folder='templates')


'''bp = {
    "_id": '',
    'channel.id': '',
    'name': '',
    'created_at': '',
    'updated_at': ''
}'''

# bps
@bp.route('/contact', methods=['GET'])
def getchannel():
    try:
        bp['_id'] + '3'
        bp['Channel.id'] = '1'
        bp['name'] = 'Group 1'
        bp['created_at'] = '28/11/2022'
        bp['updated_at'] = ''
        response = jsonify(bp)
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message': 'Failed to create channel'})
        response.status_code = 400
    finally:
        return response


@bp.route('/createcontact', methods=['PUT'])
def getUser():
    try:
        bp['_id'] = request.json['_id']
        bp['channel.id'] = request.json['Channel.id']
        bp['name'] = request.json['name']
        bp['created_at'] = request.json['created_at']
        bp['updated_at'] = request.json['updated_at']

        response = jsonify(bp)
        response.status_code = 200
        response= jsonify({'id': bp['Channel.id']})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message': 'Failed to create channel'})
        response.status_code = 400
    finally:
        return response



@ bp.route('/delcon', methods=['DELETE'])
def deletechannel():
        return jsonify({'mesage': 'deleting the channel that you want'})


if __name__ == "__editchannel_":
    bp.run(debug=True)
