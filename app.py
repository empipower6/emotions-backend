
from flask import Flask,request
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin

from nrclex import NRCLex
import nltk
import ssl



app = Flask(__name__, static_url_path='', static_folder='frontend/build')

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
    
nltk.download('punkt')

CORS(app)

@app.route('/api/analyze',methods=['POST'])
@cross_origin()
def analysis ():
    req = request.get_json()
    
    text = NRCLex(req['textAnalyze'])
    if req['technique'] =='wordList':
            return {"results": text.words}
    elif req['technique'] == 'affectList':
            return {"results": text.affect_list}
    elif req['technique'] == 'affectDictionary':
            return {"results": text.affect_dict}
    elif req['technique'] == 'emotionalCount':
            return {"results": text.raw_emotion_scores}
    elif req['technique'] == 'highestEmotion':
            return {"results": text.top_emotions}
    elif req['technique'] == 'affectFrequencies':
            return {"results": text.affect_frequencies}
    elif req['technique'] == _:
            return {"results": "Something went wrong"}
    else:
            return {'results':"Something went wrong"}

@app.route('/api/welcome')
@cross_origin()
def Welcome():
    return "Welcome to the API!!!"

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()