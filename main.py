from flask import Flask, jsonify, request
from flask_cors import CORS

from search import search

app = Flask(__name__)

CORS(app)


@app.route('/search', methods=['POST'])
def main():
    course_name = request.json['course_name']
    keyword = request.json['keyword']
    return jsonify(search(course_name, keyword))


if __name__ == "__main__":
    app.run(debug=True, port=7021)
