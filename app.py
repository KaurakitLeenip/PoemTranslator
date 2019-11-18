from flask import Flask, render_template, request
from google.cloud import translate_v2 as translater
import random
from nltk import download, pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

download("brown")
download('punkt')
download('wordnet')
download('averaged_perceptron_tagger')
app = Flask(__name__)
# credentials = service_account.Credentials.from_service_account_file(
#     'C:/Users/Kaurakit_Leenip/Downloads/translateapipoem-2c244528fce0.json'
# )
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/kleenip/PycharmProjects/PoemTranslator/translateapipoem-2c244528fce0.json"

translate_client = translater.Client()

@app.route('/')
def main():
    return render_template('index.html', poem=[], original=orig)
    # pass

@app.route('/result', methods=['GET', 'POST'])
def get_result():
    poem = request.form['raw_input'].split('\r\n')
    new_poem = []
    res = ''
    for line in poem:
        newline = ""
        temp = word_tokenize(line)
        temp = pos_tag(temp)
        for word in temp:
            if word[1][0].lower() in ['n','v','r','a']:
                try:
                    synset = wordnet.synsets(word[0], word[1][0].lower())[0]
                    hypermyns = [a.name().split('.')[0] for a in synset.hypernyms() if not '_' in a.name()]
                    hyponyms = [a.name().split('.')[0] for a in synset.hyponyms() if not '_' in a.name()]

                    if hypermyns and hyponyms:
                        choice = random.randint(0, 1)
                        if choice:
                            newline += random.choice(hyponyms)
                        else:
                            newline += random.choice(hypermyns)
                    elif hypermyns and not hypermyns:
                        newline += random.choice(hypermyns)
                    else:
                        newline += random.choice(hyponyms)

                except IndexError:
                    newline += word[0]
                    newline += ' '
                    continue
            else:
                newline += word[0]
            newline += ' '
        new_poem.append(newline)

    iterations = int(request.form['num_iterations'])
    # for line in poem:

    res = translate('<br>'.join(new_poem), iterations).replace('&#39;', "'")
    return render_template('index.html', poem=poem, original='\r\n'.join(res.split('<br>')))


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

orig = """Time passes
Years wane
Fate dances
Wills change

Pages turn
Forgotten names 
Memories burn
in life's flames

To hold on
is sheer folly
But we're drawn
despite what we see

To keep going
One foot after next
Never slowing
Doing our best

It still ends
and the earth still turns 
our attempt transcends
All physical forms"""
# print(translate(test, 50))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
