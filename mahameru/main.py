from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# placeholder data
Channel = {
    'userid': '',
    'name': '',
    'no_telp': '',
    'pin': '',
    'created_at': '',
    'updated_at': '',
    'contact_id': ''
}

# User 
@app.route('/user', methods=['GET'])
def getchannel():
    try:
        Channel['userid'] = 'Tegar'
        Channel['no_telp'] = '085157527749'
        Channel['pin'] = '123456'
        Channel['created_at'] = '23/11/2022'
        Channel['updated_at'] = ''
        Channel['contact_id'] = 2
        response = jsonify(Channel)
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message': 'Failed to create user'})
        response.status_code = 400
    finally:
        return response

# TODO : fix this so it match with the given docs
@app.route('/createuser', methods=['POST'])
def createchannel():
    try:
        # for testing purpose only getting one request json
        Channel['name'] = request.json['user']
        Channel['no_telp'] = request.json['no_telp']
        Channel['pin'] = request.json['pin']
        Channel['created_at'] = request.json['created_at']
        Channel['updated_at'] = request.json['updated_at']
        Channel['userid'] = uuid.uuid4()

        response = jsonify({'id' : Channel['userid']})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Failed to create channnel'})
        response.status_code = 400
    finally:
        return response

# TODO : dont modify it untill the above route is fixed
@app.route('/createchannel', methods=['PUT'])
def editUser():
    try:
        Channel['userid'] = request.json['userid']
        Channel['name'] = request.json['name']
        Channel['no_telp'] = request.json['no_telp']
        Channel['pin'] = request.json['pin']
        Channel['updated_at'] = request.json['updated_at']

        response = jsonify({'id' : Channel['userid']})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message': 'Failed to create channel'})
        response.status_code = 400
    finally:
        return response

@app.route('/createchannel/<string:user_id>', methods=['GET'])
def newUser(user_id):
    try:
        # this code must be changed after implementing the database
        if user_id == '2c535c8b-5d2b-4a72-9268-1c83aaf61902':
            response = jsonify({'user': 'Tegar'})
            response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify({'message' : 'Failed to get Channel'})
        response.status_code = 400
    finally:
        return response

@app.route('/user', methods=['DELETE'])
def deletechannel():
    # this code must be fixed after implmenting the database and getting clarity from director
    return jsonify({'mesage' : 'deleting the user that you want'})

# here I put my whole inner development thought, feel free to notice ;)
# lack of clarity are truly painful
# and lack of concistency is somewhat agonizing
# the docs should tell the whole truth but sadly it just gives more confusion
# -[m.s.a] 2022

if __name__ == "__main__":
    app.run(debug=True)
