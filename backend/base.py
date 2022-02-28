from crypt import methods
from flask import Flask, jsonify, request

api = Flask(__name__)

@api.route('/profile/<searchResult>')
def my_profile(searchResult):
    response_body = []
    for i in range(1, 150):
        response_body.append({
            'id': i,
            'song_name': 'song_name' + str(i),
            'singer_name': 'singer_name' + str(i),
            'album': 'album' + str(i),
            'image': 'https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F20%2F2019%2F10%2Ftaylor-swift-albums-1.jpg',
            'lyrics': 'lyrics searched: ' + searchResult + str(i)
        })
    return jsonify(response_body)