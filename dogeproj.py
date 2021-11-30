from flask import Flask, render_template, request
from difflib import get_close_matches
from random import randint
import csv
import requests

app = Flask(__name__)
akc_breeds = []  # list of akc breeds
akc_breed_names = []  # list of names of breeds
wiki_url = "https://wiki-text-scraper-361.herokuapp.com/requestText"


class Breed:
    """Represents an AKC breed"""

    def __init__(self, name, color, size, height, weight, life, personality, activity, coat, group):
        self.name = name
        self.color = color
        self.size = size
        self.height = height
        self.weight = weight
        self.life = life
        self.personality = personality
        self.activity = activity
        self.coat = coat
        self.group = group


# parse csv file containing akc breed info
with open('./static/akc-breeds.csv', 'r') as csv_akc:
    csv_reader = csv.reader(csv_akc)
    # create a Breed object for each line & add to list of akc breeds
    for row in csv_reader:
        akc_breeds.append(Breed(row[0], row[1].split(';'), row[2], row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9]))
        akc_breed_names.append(row[0])


@app.route('/')
def home():
    return render_template('doge-home.html')


@app.route('/search', methods=['POST'])
def search():
    user_search = request.form.get('search-breed')

    for breed in akc_breeds:
        if breed.name.upper() == user_search.upper():
            param = {'wikipage': user_search, 'sentences': 3}
            r = requests.get(url=wiki_url, params=param)
            data = r.json()
            text = data['wikitext']
            img = "/static/imgs/akc/" + breed.name + ".png"
            return render_template('doge-result.html', dog=breed, text=text, img=img)

    close_breeds = get_close_matches(user_search, akc_breed_names)
    if len(close_breeds) == 1:
        return render_template('doge-search-similar.html', search=user_search, similar1=close_breeds[0])
    elif len(close_breeds) == 2:
        return render_template('doge-search-similar.html', search=user_search, similar1=close_breeds[0],
                               similar2=close_breeds[1])
    elif len(close_breeds) == 3:
        return render_template('doge-search-similar.html', search=user_search, similar1=close_breeds[0],
                               similar2=close_breeds[1], similar3=close_breeds[2])
    else:
        return render_template('doge-not-found.html', search=user_search)


@app.route('/similar', methods=['POST'])
def similar():
    selected_breed = request.form['similar-breed-btn']
    for breed in akc_breeds:
        if breed.name == selected_breed:
            param = {'wikipage': selected_breed, 'sentences': 3}
            r = requests.get(url=wiki_url, params=param)
            data = r.json()
            text = data['wikitext']
            img = "/static/imgs/akc/" + breed.name + ".png"
            return render_template('doge-result.html', dog=breed, text=text, img=img)


@app.route('/random', methods=['POST'])
def random():
    index = randint(0, len(akc_breed_names)-1)
    breed_name = akc_breed_names[index]
    for breed in akc_breeds:
        if breed.name == breed_name:
            param = {'wikipage': breed_name, 'sentences': 3}
            r = requests.get(url=wiki_url, params=param)
            data = r.json()
            text = data['wikitext']
            img = "/static/imgs/akc/" + breed.name + ".png"
            return render_template('doge-result.html', dog=breed, text=text, img=img)


if __name__ == "__main__":
    app.run(debug=True)
