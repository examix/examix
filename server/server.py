from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)


@app.route("/api/home/", methods=["GET"])
def return_home():
    return jsonify(
        {"message": "Welcome to the Playground!", "people": ["John", "Alfred", "Bobby"]}
    )

@app.route("/api/data/", methods=["GET"])
def get_data():
    books = [
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"id": 2, "title": "Moby Dick", "author": "Herman Melville"},
        {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen"},
    ]
    return jsonify({"books": books})

@app.route("/api/members/", methods=["GET"])
def get_members():
    id1 = random.random()
    id2 = random.random()
    id3 = random.random()
    id4 = random.random()
    id5 = random.random()
    members = [
        {"id": id1, "name": "Nick"},
        {"id": id2, "name": "Emma"},
        {"id": id3, "name": "Oliver"},
        {"id": id4, "name": "Sophia"},
        {"id": id5, "name": "Maria"},
    ]
    return jsonify({"members": members})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
