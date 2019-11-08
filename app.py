from flask import Flask, render_template, request
from google.cloud import translate_v2 as translater
from google.oauth2 import service_account
import random

app = Flask(__name__)
credentials = service_account.Credentials.from_service_account_file(
    '/home/kleenip/Downloads/translateapipoem-2c244528fce0.json'
)
translate_client = translater.Client(credentials=credentials)

@app.route('/')
def main():
    return render_template('index.html', poem=[])
    # pass

@app.route('/result', methods=['GET', 'POST'])
def get_result():
    poem = request.form['raw_input'].split('\r\n')
    res = []
    iterations = int(request.form['num_iterations'])
    # print(poem, iterations)
    for line in poem:
        res.append(translate(line, iterations))

    return render_template('index.html', poem=res, original='\r\n'.join(poem))


def translate(raw, iterations):
    res = raw
    for i in range(iterations):
        target_lang = get_language()
        print("translating to language: {1}".format(res, target_lang))
        res = (translate_client.translate(raw, target_lang))['translatedText']
    res = translate_client.translate(res, 'en')['translatedText']
    return res

def get_language():
    results = translate_client.get_languages()
    choice = random.choice(results)
    return choice['language']

test = """Infinite in mystery is the gift of the Goddess
We seek it thus, and take to the sky
Ripples form on the water's surface
The wandering soul knows no rest."""
# print(translate(test, 50))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
