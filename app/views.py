'''
    File name: views.py
    Authors: Kenny Le
    Date created: 7/25/2018
    Date last modified: 8/8/2018
    Python Version: 3.6
'''

# Python application to randomly select and return a movie's title and plot using wikipediaapi

import wikipedia
import wikipediaapi
import random
import requests
from bs4 import BeautifulSoup
from flask import render_template, request
from app import app


#################### Helper Methods ####################

# return url
def get_url(page):
    return page.fullurl

# return title and plot information
def get_title_and_section_content(page):
    try:
        ret_text = page.sections[0].text
        if len(ret_text) >= 500:
            ret_text = ret_text.replace('\\','')
            return page.title, ret_text
    except IndexError:
        return page.title, "No plot information available."
    return page.title, "No plot information available."

# randomly select title from list
def get_random_movie(movies):
    wiki = wikipediaapi.Wikipedia('en')
    random_title = random.choice(list(movies.keys()))
    wiki_page = wiki.page(random_title)
    return wiki_page, movies[random_title]

# get movie poster image
def get_movie_image_file(wiki_page_url, title):
    ret_file = ''
    page_req = requests.get(wiki_page_url)
    page_soup = BeautifulSoup(page_req.content, 'lxml')
    img_links = page_soup.findAll("a", {"class":"image"})
    for img_link in img_links:
        img_src = img_link.img['src']
        print(img_src)
        if 'wikimedia' + title[:3] in img_src or 'poster' in img_src or 'Poster' in img_src:
            ret_file = img_src
            break
    return ret_file

# parse for movie titles and directors
def fill_structures(wikitable, var_dict, exist_check):
    start_substring = 'title="'
    end_substring = '">'
    first_letter_of_title = ''
    for row in wikitable.findAll('tr'):
        title_cell = row.findAll('th')
        str_title_cell = str(title_cell)

        director_cell = row.findAll('td')
        str_director_cell = str(director_cell)

        start_pt_title = str_title_cell.find(start_substring)
        first_letter_title = str_title_cell[start_pt_title + 7: start_pt_title + 8]

        start_pt_director = str_director_cell.find(start_substring)
        first_letter_director = str_director_cell[start_pt_director + 7: start_pt_director + 8]

        end_substring_title = end_substring + first_letter_title
        end_substring_director = end_substring + first_letter_director

        if start_substring in str_title_cell and exist_check not in str_title_cell:
            end_pt_title = str_title_cell.find(end_substring_title)
            end_pt_director = str_director_cell.find(end_substring_director)

            title = str_title_cell[start_pt_title + 7: end_pt_title]
            director = str_director_cell[start_pt_director + 7: end_pt_director]
            var_dict[title] = director

        end_substring = '">'
        first_letter_of_title = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movie', methods=['POST', 'GET'])
def movie():
    wiki_url = 'https://en.wikipedia.org/wiki/List_of_horror_films_of_'
    list_of_titles = []
    titles_and_directors = {}
    year = ''
    message = ''
    check = '(page does not exist)'

    if request.method == 'POST':
        select = str(request.form.get('time-drop-down'))
        if select != 'null':
            year = select
        else:
            return render_template('index.html', message='Please select a Year')

    wiki_url = wiki_url + year
    req = requests.get(wiki_url)
    soup = BeautifulSoup(req.content, 'lxml')
    table = soup.find('table', {'class':'wikitable sortable'})

    fill_structures(table, titles_and_directors, check)

    page = get_random_movie(titles_and_directors)
    title, content = get_title_and_section_content(page[0])
    url = get_url(page[0])
    img_file = get_movie_image_file(url, title)

    return render_template('movie.html',
                            title=title, content=content, director=page[1],
                            url=url, image_url=img_file)
