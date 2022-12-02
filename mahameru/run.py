from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# placeholder data
channel = {
    'channel.id': '',
    'name': '',
    'created_at': '',
    'updated_at': '',
    'Member_id': ''
}

# User 
@app.route('/channel', methods=['GET'])
def getchannel():
    try:
        channel['channelid'] = 3
        channel['name'] = 'group 1'
        channel['created_at'] = '28/11/2022'
        channel['updated_at'] = ''
        channel['Member_id'] = 7
        response = jsonify(channel)
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message': 'Failed to create channel'})
        response.status_code = 400
    finally:
        return response

# TODO : fix this so it match with the given docs
@app.route('/createchannel', methods=['POST'])
def createchannel():
    try:
        # for testing purpose only getting one request json
        channel['name'] = request.json['channel']
        channel['created_at'] = request.json['created_at']
        channel['channel.id'] = uuid.uuid4()

        response = jsonify({'id' : channel['channel.id']})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Failed to create channel'})
        response.status_code = 400
    finally:
        return response
    
# TODO : dont modify it untill the above route is fixed
@app.route('/createchannel', methods=['PUT'])
def editChannel():
    try:
        channel['channel.id'] = request.json['channel.id']
        channel['name'] = request.json['name']
        channel['updated_at'] = request.json['updated_at']

        response = jsonify({'id' : channel['channel.id']})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message': 'Failed to create channel'})
        response.status_code = 400
    finally:
        return response

@app.route('/createchannel/<string:channel_id>', methods=['GET'])
def newChannel(channel_id):
    try:
        # this code must be changed after implementing the database
        if channel_id == '2c535c8b-5d2b-4a72-9268-1c83aaf61902':
            response = jsonify({'channel': 'Group 1'})
            response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Failed to get channel'})
        response.status_code = 400
    finally:
        return response

@app.route('/channel', methods=['DELETE'])
def deleteChannel():
    # this code must be fixed after implmenting the database and getting clarity from director
    return jsonify({'mesage' : 'deleting the user that you want'})



if __name__ == "__main__":
    app.run(debug=True)
