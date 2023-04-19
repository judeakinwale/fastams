from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = 'testblog'
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@cluster0.z2vm0.mongodb.net/testblogdb?retryWrites=true&w=majority'

mongo = PyMongo(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = mongo.db.users.find_one({'username': data['username']})
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# User registration
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    existing_user = mongo.db.users.find_one({'username': username})

    if existing_user:
        return jsonify({'message': 'Username already exists!'})

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({'username': username, 'password': hashed_password})

    return jsonify({'message': 'User registered successfully!'})

# User login
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = mongo.db.users.find_one({'username': username})

    if not user:
        return jsonify({'message': 'User not found!'})

    if check_password_hash(user['password'], password):
        token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'message': 'Invalid password!'})

# Blog posts
@app.route('/posts', methods=['POST'])
@token_required
def add_post(current_user):
    title = request.json['title']
    content = request.json['content']

    mongo.db.posts.insert_one({'title': title, 'content': content, 'author': current_user['username']})

    return jsonify({'message': 'Post added successfully!'})

@app.route('/posts', methods=['GET'])
@token_required
def get_posts(current_user):
    posts = mongo.db.posts.find({'author': current_user['username']})

    output = []

    for post in posts:
        output.append({'id': str(post['_id']), 'title': post['title'], 'content': post['content']})

    return jsonify({'posts': output})

@app.route('/posts/<id>', methods=['GET'])
@token_required
def get_post(current_user, id):
    post = mongo.db.posts.find_one({'_id': ObjectId(id), 'author': current_user['username']})

    if not post:
        return jsonify({'message': 'Post not found!'})

    return jsonify({'posts': output})


@app.route('/posts/<id>', methods=['PUT'])
@token_required
def update_post(current_user, id):
    post = mongo.db.posts.find_one({'_id': ObjectId(id), 'author': current_user['username']})

    if not post:
        return jsonify({'message': 'Post not found!'})

    mongo.db.posts.update_one({'_id': ObjectId(id)}, {'$set': {'title': request.json['title'], 'content': request.json['content']}})

    return jsonify({'message': 'Post updated successfully!'})


@app.route('/posts/<id>', methods=['DELETE'])
@token_required
def delete_post(current_user, id):
    post = mongo.db.posts.find_one({'_id': ObjectId(id), 'author': current_user['username']})

    if not post:
        return jsonify({'message': 'Post not found!'})

    mongo.db.posts.delete_one({'_id': ObjectId(id)})

    return jsonify({'message': 'Post deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
