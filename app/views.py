# views.py

# Kenny Le
# Python application to randomly select and return a movie's title and plot using wikipediaapi

import wikipedia
import wikipediaapi
import random
import requests
from bs4 import BeautifulSoup
from flask import render_template, request
from app import app

wiki_url = 'https://en.wikipedia.org/wiki/List_of_horror_films_of_2011'
list_of_titles = []

req = requests.get(wiki_url)
soup = BeautifulSoup(req.content, 'lxml')
table = soup.find('table', {'class':'wikitable sortable'})

#################### Helper Methods ####################

# return title and plot information
def get_title_and_section_content(page):
    try:
        ret_text = page.sections[0].text
        if len(ret_text) >= 250:
            ret_text = ret_text.replace('\\','')
        return page.title, ret_text
    except IndexError:
        return page.title, "No plot information available."
    return page.title, "No plot information available."

# randomly select title from list
def get_random_movie(movies):
    wiki = wikipediaapi.Wikipedia('en')
    wiki_page = wiki.page(movies[random.randint(0, len(movies)-1)])
    return wiki_page

# parse for movie titles for use with wikipediaapi
def fill_list_of_titles(wikitable, var_list):
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
            title = str_cell[start_pt + 7: end_pt]
            var_list.append(title)
        end_substring = '">'
        first_letter_of_title = ''

# main
@app.route('/')
def index():
    return render_template('index.html')
