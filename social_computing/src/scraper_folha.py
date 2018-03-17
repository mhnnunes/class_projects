#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2017 Matheus Nunes <mhnnunes@dcc.ufmg.br>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import string
import requests
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from json_functions import dump_utf8_JSON
from json_functions import load_utf8_JSON


def summarize_text(strings):
    text = ''
    for phrase in strings:
        text += phrase
    return text


def get_data_from_URL(url, driver):
    # page = get_fully_loaded_page(url, driver)
    page = get_page(url)
    page_data = {}

    page_data['url'] = url

    # Get share count for page, save as string
    # sc_container = page.find_all('span', class_='share-counter')[0]
    # sc = sc_container.find_all('span', class_='counter')[0].text
    # page_data['share_counter'] = sc

    # Get date of posting
    for time in page.find_all('time'):
        if not time.has_attr('class'):
            post_timestamp = time['datetime']
        elif page.find_all('time', class_='news__date-cover'):
            post_timestamp = page.find_all(
                'time', class_='news__date-cover')[0]['datetime']
    page_data['timestamp'] = post_timestamp

    # Get tag containing article body
    articleBody = page.find_all('div', class_='content',
                                itemprop='articleBody')
    if len(articleBody) == 0:
        articleBody = page.find_all('div', class_='news__content')
    if len(articleBody) == 0:
        articleBody = page.find_all('div', class_='entry-content')

    articleBody = articleBody[0]

    # Get <p> tags inside article body
    strings = []
    paragraphs = articleBody.find_all('p')
    for p in paragraphs:
        strings.append(p.text)

    page_data['text'] = summarize_text(strings)
    return page_data


def get_page(url):
    return BeautifulSoup(requests.get(url).text.encode('utf-8'), "html.parser")


def get_fully_loaded_page(url, driver):
    driver.get(url)
    html = driver.page_source
    return BeautifulSoup(html.encode('utf-8'), "html.parser")


def search(urlInicial, paginationURL, hbyPage, searchTerm):

    url = string.replace(urlInicial, "${SEARCH_TERM}", searchTerm)
    print url
    soup = get_page(url)

    resultsCount = str(soup.find_all("h2", class_="search-title"))
    print 'RESULTSCOUNT>  ', resultsCount
    resultsCount = (resultsCount.split(')'))[0]
    resultsCount = resultsCount.split(' ')
    resultsCount = int(resultsCount[len(resultsCount) - 1])
    print 'RESULTSCOUNT>  ', resultsCount

    paginationURL = string.replace(paginationURL, "${SEARCH_TERM}", searchTerm)
    paginationURL = string.replace(paginationURL,
                                   "${RESULTS_COUNT}", str(resultsCount))

    pageCount = (resultsCount / hbyPage)
    print 'pageCount  ', pageCount
    # for each search results page
    links = []
    for page in xrange(pageCount + 1):
        # Get page
        url = string.replace(paginationURL, "${SRESULTS_PAGE}",
                             str(page * hbyPage))
        soup = get_page(url)
        # Get search results in that page
        print 'page  ', page
        searchResults = soup.find_all('h3', class_='search-results-title')
        for index, result in enumerate(searchResults):
            # Get links
            link = result.find_all('a')[0]['href']
            links.append(link)

    links = list(set(links))
    print 'link list:   ', len(links)
    return links


def main(searchterm=None, filename=None):
    initialURL = "http://search.folha.uol.com.br/?q=${SEARCH_TERM}"
    paginationURL = "http://search.folha.uol.com.br/search?q=\
    ${SEARCH_TERM}&site=todos&results_count=${RESULTS_COUNT}&search_time=\
    0.043&url=http%3A%2F%2Fsearch.folha.uol.com.br%2Fsearch%3Fq%3D\
    ${SEARCH_TERM}%26site%3Dtodos&sr=${SRESULTS_PAGE}"
    headlinesbyPage = 25
    searchTerm = "Queermuseu" if searchterm is None else searchterm
    if filename is None:
        links = search(initialURL, paginationURL, headlinesbyPage, searchTerm)
        linkdict = {}
        for index, url in enumerate(links):
            print index, url
            linkdict[index] = url
        dump_utf8_JSON(os.path.join(os.getcwd(), 'links.json'), [linkdict])
    else:
        dicts = load_utf8_JSON(filename)[0]
        driver = webdriver.Firefox()
        for d in dicts:
            for index, url in d.iteritems():
                print index, url
                page_data = get_data_from_URL(url, driver)
                dump_utf8_JSON(os.path.join(os.getcwd(), 'texts', str(index) +
                               '.json'), page_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web scraper for collecting \
                                     Folha de São Paulo news content')
    parser.add_argument('-st', '--searchterm', action='store', type=str,
                        help='Search term - this should not be used in \
                        conjunction with the links filename. When passing a \
                        URL file as argument, this file will be read and the \
                        search term will be ignored in this case')
    parser.add_argument('-f', '--filename', action='store', type=str,
                        help='Full path to the file containing the URLs of the \
                        pages')
    args = parser.parse_args()
    main(args.searchterm, args.filename)
