from flask import Flask, request

api = Flask(__name__)

@api.route('/profile/<searchResult>')
def my_profile(searchResult):
    response_body = {
        "name": searchResult,
        "about": "Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body