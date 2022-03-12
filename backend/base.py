from flask import Flask, jsonify, request
from phrase_search import search_result

api = Flask(__name__)

@api.route('/profile/<searchResult>')
def my_profile(searchResult):
    results = search_result(searchResult)[0]
    return jsonify(results)

@api.route('/whole/<id>')
def wholeLyrics(id):
    response_body = []
    response_body.append({
        'id': id,
        'song_name': 'song_name' + str(id),
        'singer_name': 'singer_name' + str(id),
        'album': 'album' + str(id),
        'image':  'https://images.genius.com/14a5edcd1e4382bdfc9bb215540c648e.300x300x1.jpg',
        'lyrics': 'lyrics searched: id:' + id,
        'wholeLyrics': ["Hey Garry, how d'ya spell Dun Laoghaire?",
                        "That's easy, Bob! D.U.N. L.A.O.G.H.A.I.R.E.",
                        "That's how you spell Dun Laoghaire.",
                        "No, you're wrong, pal. That's not how you spell it. That's not how you spell Dun Laoghaire.",
                        'It is.',
                        "It isn't.",
                        'It is!',
                        'It is not!',
                        'It is!',
                        "I'll tell ya how to spell it",
                        "No, you won't",
                        'Now',
                        'All right',
                        'Tired N Weary',
                        'Drab N Dreary',
                        "That's how you spell it, Dun Laoghaire.",
                        'It is not',
                        'It is so',
                        'It is not',
                        'It is',
                        "Well, it's the stupidest way I've ever heard of spelling Dun Laoghaire.",
                        'Well I spell it drunk and beary',
                        'Licentious and leary',
                        "There's only one way out of Dun Laoghaire, you know what it is?",
                        'Off the mail boat piery',
                        "Off the mail boat piery, I'm glad we got out",
                        'Who cares about Dun Laoghaire?',
                        "You're talkin' about me ,home town pal.",
                        'Ah, listen to that.., do do do do......',
                        'Come on everybody, I want the world to spell Dun Laoghaire!',
                        'Are ya ready? 1, 2, 3, 4',
                        'D.U.N. L.A.O.G.H.A.I.R.E. Dun Laoghaire, Dun Laoghaire',
                        'D.U.N. L.A.O.G.H.A.I.R.E. Dun Laoghaire, Dun Laoghaire',
                        'D.U.N. L.A.O.G.H.A.I.R.E. Dun Laoghaire, Dun Laoghaire',
                        'D.U.N. L.A.O.G.H.A.I.R.E. Dun Laoghaire, Dun Laoghaire',
                        'D.U.N. L.A.O.G.H.A.I.R.E. Dun Laoghaire, Dun Laoghaire',
                        'D.U.N. L.A.O.G.H.A.I.R.E. Dun Laoghaire, Dun Laoghaire']
    })
    return jsonify(response_body)