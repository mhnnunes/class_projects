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
from json_functions import dump_utf8_JSON
from json_functions import load_utf8_JSON


def summarize_text(strings):
    """ Concatenates strings forming the article text.
    Arguments:
        strings {list(str)} -- list of strings composing the article body
    Returns:
        text {str} -- full article text
    """
    text = ''
    for phrase in strings:
        text += phrase

    return text


def get_publication_date(page):
    """ Extract article's publication date.
    Arguments:
        page {BeautifulSoup} -- soup object containing parsed page
    Returns:
        published {str/bool} -- publication date in success. False in failure.
    """
    p = page.find_all('p', class_='content-publication-data__updated')
    if len(p) > 0:
        published = p[0].find_all('time',
                                  itemprop='datePublished')[0]['datetime']
    else:
        p = page.find_all('article', class_='post')
        if len(p) > 0:
            p = p[0].find_all('header')
            published = p[0].find_all('time',
                                      class_='post-date')[0]['datetime']
        else:
            return False
    return published


def get_last_modification_date(page):
    """ Extract article's last modification date.
    Arguments:
        page {BeautifulSoup} -- soup object containing parsed page
    Returns:
        modified {str/bool} -- last modified date in success. False in failure.
    """
    modified = False
    p = page.find_all('p', class_='content-publication-data__updated')
    if len(p) > 0:
        modified = p[0].find_all(
            'span', class_='content-publication-data__updated-relative')
        if len(modified) > 0:
            modified = modified[0]
            modified = \
                modified.find_all('time',
                                  itemprop='dateModified')[0]['datetime']
    return modified


def get_headline(page):
    """ Extract article's headline.
    Arguments:
        page {BeautifulSoup} -- soup object containing parsed page
    Returns:
        headline {str/bool} -- article's headlin in success, False otherwise.
    """
    h = page.find_all('h1', itemprop='headline')
    if len(h) > 0:
        return h[0].text
    else:
        return False


def getArticleText(page):
    """ Extract article's text from page.
    Arguments:
        page {BeautifulSoup} -- soup object containing parsed page
    Returns:
        strings {list(str)} -- list of strings containing the article's text
    """
    strings = []
    paragraphs = page.find_all('p', class_='content-text__container')
    for p in paragraphs:
        strings.append(p.text)
    return strings


def extract_article_info_from_URL(url, data):
    """ Extract article's information from URL.
    Arguments:
        url {str} -- article's URL
        data {dict} -- dictionary for saving article's data
    Returns:
        bool -- True in success, False otherwise.
    """
    page = get_page(url)

    # Get time published and time modified
    published = get_publication_date(page)
    # If the control flow executes past previous if statement, we have the
    # date the article has been published on
    if published:
        data['datePublished'] = published
    else:
        return False

    # Get datetime of last modification
    modified = get_last_modification_date(page)
    # If the control flow executes past previous if statement, we have the
    # latest date in which the article has been modified
    data['lastModified'] = modified if modified else published

    # Get headline
    headline = get_headline(page)
    if headline:
        data['headline'] = headline
    # Get <p> tags containing text from article
    strings = getArticleText(page)

    # print 'len:  ', len(strings)
    data['text'] = summarize_text(strings) if len(strings) > 0 else False
    return True


def get_page(url):
    """ Get page content via HTTP request, parse it into a soup object.
    Arguments:
        url {str} -- article's URL
    Returns:
        page {BeautifulSoup} -- soup object containing parsed page
    """
    return BeautifulSoup(requests.get(url).text.encode('utf-8'), "html.parser")


def more_results(page):
    """ Check if empty results page has been reached. If it has, a div with
    class 'nao-encontrado' will be found on page.
    Arguments:
        page {BeautifulSoup} -- soup object containing parsed page
    Returns:
        bool -- True if found, False otherwise
    """
    notFound = page.find_all('div', class_='nao-encontrado')
    return len(notFound) == 0


def search(rawURL, searchTerm):
    """ Perform search for term in main page. Return list of URLs obtained as
    search result.
    Arguments:
        rawURL {str} -- raw URL from page where the search will be performed on
        searchTerm {str} -- term that will be searched for
    Returns:
        links {list(str)} -- list of URLs obtained as search results
    """
    pageNum = 1
    queryURL = string.replace(rawURL, "{QUERY}", searchTerm)
    url = string.replace(queryURL, "{PAGE_NUM}", str(pageNum))
    soup = get_page(url)
    links = []
    # for each search results page
    while(more_results(soup)):
        # Get search results in that page
        print 'page  ', pageNum
        searchResults = soup.find_all('a', class_='busca-titulo')
        for index, result in enumerate(searchResults):
            # Get links
            link = result['href']
            # Parse link
            link = link[link.find('http'):]
            link = link.replace('%3A', ':')
            link = link.replace('%2F', '/')
            link = link[:link.find('&t=')]
            links.append(link)

        # Get new page
        pageNum += 1
        url = string.replace(queryURL, "{PAGE_NUM}", str(pageNum))
        soup = get_page(url)

    # Return only unique URLs
    links = list(set(links))
    print 'link list:   ', len(links)
    return links


def main(searchterm=None, filename=None):
    queryURL = "http://g1.globo.com/busca/?q={QUERY}&page={PAGE_NUM}"
    searchTerm = "Queermuseu" if searchterm is None else searchterm
    print 'searchterm', searchterm
    if filename is None:
        links = search(queryURL, searchTerm)
        linkdict = {}
        for index, url in enumerate(links):
            print index, url
            linkdict[index] = url
        dump_utf8_JSON(os.path.join(os.getcwd(), 'links.json'), [linkdict])
    else:
        dicts = load_utf8_JSON(filename)[0]
        for d in dicts:
            for index, url in d.iteritems():
                data = {}
                print index, url
                data['url'] = url
                if extract_article_info_from_URL(url, data) and data['text']:
                    dump_utf8_JSON(os.path.join(os.getcwd(), 'g1-texts',
                                                str(index) + '.json'), data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web scraper for collecting \
                                     G1 news content')
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
