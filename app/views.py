# views.py

# Kenny Le

import wikipediaapi
import wikipedia
import requests
from bs4 import BeautifulSoup
import random
from flask import render_template
from app import app

base_url = 'https://en.wikipedia.org'
wiki_url = 'https://en.wikipedia.org/wiki/List_of_horror_films_of_2018'
list_of_titles = []

req = requests.get(wiki_url)
soup = BeautifulSoup(req.content, 'lxml')
table = soup.find('table', {'class':'wikitable sortable'})

start_substring = 'title="'
end_substring = '">'
first_letter_of_title = ''

for row in table.findAll('tr'):
    cell = row.findAll('th')
    str_cell = str(cell)
    start_pt = str_cell.find(start_substring)
    first_letter_of_title = str_cell[start_pt + 7: start_pt + 8]
    end_substring = end_substring + first_letter_of_title
    if start_substring in str_cell:
        end_pt = str_cell.find(end_substring)
        article = str_cell[start_pt + 7: end_pt]
        list_of_titles.append(article)
    end_substring = '">'
    first_letter_of_title = ''

for title in list_of_titles:
    print(title)

@app.route('/')
def index():
    return render_template('index.html')
