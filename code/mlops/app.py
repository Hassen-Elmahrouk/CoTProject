from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson import json_util
from flask_cors import CORS
from pymongo import MongoClient
import json  # Import the json module


app = Flask(__name__)
CORS(app)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/my_data'
mongo = PyMongo(app)

# Route to retrieve data from the MongoDB collection
@app.route('/api/annotations', methods=['GET'])
def get_annotations():
    # Retrieve data from the MongoDB collection
    annotations = mongo.db.Hous.find()

    # Convert MongoDB documents to JSON format
    annotations_json = json_util.dumps(annotations)

    return jsonify({'annotations': json.loads(annotations_json)})

if __name__ == '__main__':
    app.run(debug=True)
