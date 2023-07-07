from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:8080/')
db = client['super_awesome_database']
collection = db['users']

@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find({}, {'_id': 0}))
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = collection.find_one({'id': id}, {'_id': 0})
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_id = user_data.get('id')
    if not user_id or collection.find_one({'id': user_id}):
        return jsonify({'error': 'Invalid or duplicate user ID'}), 400
    user = {
        'id': user_id,
        'name': user_data.get('name'),
        'email': user_data.get('email'),
        'password': user_data.get('password')
    }
    collection.insert_one(user)
    return jsonify({'id': user_id, 'message': 'User created successfully'})

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user_data = request.get_json()
    update_fields = {}
    if 'name' in user_data:
        update_fields['name'] = user_data['name']
    if 'email' in user_data:
        update_fields['email'] = user_data['email']
    if 'password' in user_data:
        update_fields['password'] = user_data['password']

    if not update_fields:
        return jsonify({'error': 'No fields provided for update'}), 400

    result = collection.update_one({'id': id}, {'$set': update_fields})
    if result.modified_count:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({'id': id})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
