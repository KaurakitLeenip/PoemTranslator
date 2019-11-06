from flask import Flask, render_template, request
from google.cloud import translate_v2 as translater
import random
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/kleenip/Downloads/Translate-8c4224ab5c22.json"
app = Flask(__name__)

@app.route('/')
def main():
    # return render_template('index.html')
    pass

# @app.route('/result', methods = ['POST'])
def get_result():
    poem = request.form['raw_input']
    iterations = request.form['num_iterations']

def translate(raw, iterations):
    translate_client = translater.Client()
    res = raw
    for i in range(iterations):
        res = (translate_client.translate(raw, get_language()))['translatedText']
        res = translate(res, 'en')['translatedText']

def get_language():
    languages = ['af','sq','am','ar','hy',
                 'az','eu','be','bn','bs',
                 'bg','ca','ceb','zh','zh-TW',
                 'co','hr','cs','da','nl','er',
                 'fi','fr','fy','gl','ka','de',
                 'el','gu','ht','ha','haw','he',
                 'hi','hmn','hu','is','ig','id',
                 'ga','it','ja','jw','kn','kk',
                 'km','ko','ku','ky','lo','la',
                 'lv','lt','lb','mk','mg','ms',
                 'ml','mt','mi','mr','mn','my',
                 'mn','my','ne','no','ny','ps',
                 'fa','pl','pt','pa','ro','ru',
                 'sm','gd','sr','st','sn','sd',
                 'sd','si','sk','sl','so','es',
                 'su','sw','sv','tl','tg','ta',
                 'te','th','tr','uk','ur','uz',
                 'vi','cy','xh','yi','yo','zu']
    return random.choice(languages)


translate("testing the program", 3)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
