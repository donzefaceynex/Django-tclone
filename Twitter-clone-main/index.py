import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from bad_words import bad_words
import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
CORS(app)
limiter = Limiter(app, key_func=get_remote_address)


app.config['MONGO_URI'] = os.environ.get('MONGO_URI') or 'mongodb://localhost/meower'
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Meower! 😹 🐈'})


@app.route('/mews', methods=['GET'])
def get_mews():
    mews = mongo.db.mews.find()

    return jsonify({'mews': [{'name': mew['name'], 'content': mew['content']} for mew in mews]})


@app.route('/v2/mews', methods=['GET'])
def get_v2_mews():

    skip = int(request.args.get('skip') or 0) or 0  # default to 0 if not provided or invalid value provided (e.g., negative number)

    limit = int(request.args.get('limit') or 5)  # default to 5 if not provided or invalid value provided (e.g., negative number)

    sort = request.args.get('sort') or 'desc'  # default to desc if not provided or invalid value provided (e.g., negative number)

    total = mongo.db.mews.count()

    mews = list(mongo.db.mews \
        .find({}, {'skip': skip, 'limit': limit, 'sort': [('created', 1 if sort == 'asc' else -1)]}))

    return jsonify({'meta': {'total': total, 'skip': skip, 'limit': limit, 'hasMore': total - (skip + limit) > 0}, \
                    'mews': [{'name': mew['name'], 'content': mew['content']} for mew in mews]})

    
@limiter.limit("1 per second")  # rate limit of 1 request per second per IP address (default is 60 requests per minute per IP address)    
@app.route('/mews', methods=['POST'])    
def create_mew():    

    name = request.json['name']    

    content = request.json['content']    

    if len(name) > 50:    

        return jsonify({'message': "Name cannot be longer than 50 characters."}), 422    

    elif len(content) > 140:    

        return jsonify({'message': "Content cannot be longer than 140 characters."}), 422    

    elif name in bad_words:    

        return jsonify({'message': "Name cannot contain profanity."}), 422    

    elif content in bad_words:    

        return jsonify({'message': "Content cannot contain profanity."}), 422    

        																		   # insert the new meow into the database and return it as JSON response                                                                                                                                                                                                                             # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as the created date for the meow document      # note that we are using the current time as t...