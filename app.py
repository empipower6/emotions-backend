
import re
from flask import Flask,request
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import csv
import json

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

# Download Gunter's Words
# Opening JSON file
f = open('emotionChart/words.json')
 # returns JSON object as 
 # a dictionary
data = json.load(f)
f.close()

#Functions 
def analyzeWord(word):
  for char in data:
   if char["word"] == word:
    return char
  return False

def analyzeText(txt):
        #delete all of the non- alphanumeric characters
        noCharText= re.sub(r'[^\w]', ' ', txt)
        wordArr = noCharText.split(' ')
        emotionWordCount = 0
        emotionSum = {
        "POSITIVE": 0,
        "NEGATIVE": 0,
        "ANGER": 0,
        "ANTICIPATION": 0,
        "DISGUST": 0,
        "FEAR": 0,
        "JOY": 0,
        "SADNESS": 0,
        "SURPRISE": 0,
        "TRUST": 0
        }
        for word in wordArr:
                wordEmotions = analyzeWord(word)
                if wordEmotions:
                        emotionSum['POSITIVE'] += wordEmotions['POSITIVE']
                        emotionSum['NEGATIVE'] += wordEmotions['NEGATIVE']
                        emotionSum['ANGER'] += wordEmotions['ANGER']
                        emotionSum['ANTICIPATION'] += wordEmotions['ANTICIPATION']
                        emotionSum['DISGUST'] += wordEmotions['DISGUST']
                        emotionSum['FEAR'] += wordEmotions['FEAR']
                        emotionSum['JOY'] += wordEmotions['JOY']
                        emotionSum['SADNESS'] += wordEmotions['SADNESS']
                        emotionSum['SURPRISE'] += wordEmotions['SURPRISE']
                        emotionSum['TRUST'] += wordEmotions['TRUST']
                        emotionWordCount += 1
        
        for emotion in emotionSum:
                emotionSum[emotion] = round((emotionSum[emotion]*100)/emotionWordCount,1)
        return emotionSum


#Routes
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


@app.route('/api/gunterwords',methods=['POST'])
def gunterwords():
 req = request.get_json()

 result = analyzeText(req['textAnalyze'])
 return result
         

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()
