from flask import Flask, jsonify, request
from search import search_result

api = Flask(__name__)

@api.route('/profile')
def my_profile():
    searchResult = request.args.get('query')
    typeName = request.args.get('type')
    print(typeName)
    results = search_result(searchResult, typeName)[0]
    return jsonify(results)