#!/usr/bin/env python3
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

import re
import codecs
from os.path import join
from os.path import split
from numpy import array
from numpy import savetxt
# from functools import reduce
from gensim import corpora, models
from sentiment import get_union_of_dates
from sentiment import get_intersecting_dates
from sentiment import get_fullpath_by_dataset
from analysis import tokenize_remove_stopwords as tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

FOLHA_DIR = 'folha-texts'
G1_DIR = 'g1-texts'
TWEETS_DIR = 'tweets'

WEEKLY = join('analyses', 'by-week')
DAILY = join('analyses', 'daily')

RESULTS_DIR = join('joint-analyses', 'cosine-similarity')


def build_LDA_model(text):
    # texts = list(map(lambda x: re.sub('ser', '', x), texts))
    # texts = list(map(lambda x: re.sub('queermuseu', '', x), texts))
    # texts = list(map(lambda x: re.sub('sobre', '', x), texts))
    # texts = list(map(lambda x: re.sub('é', '', x), texts))
    # texts = list(map(lambda x: re.sub(' +', ' ', x), texts))
    # texts = list(map(lambda x: x.split(' '), texts))
    text = re.sub('ser', '', text)
    text = re.sub('queermuseu', '', text)
    text = re.sub('exposição', '', text)
    text = re.sub('sobre', '', text)
    text = re.sub(' é ', '', text)
    text = re.sub(' +', ' ', text)
    text = text.split(' ')
    # stemmer = RSLPStemmer()
    # text = [stemmer.stem(word) for word in text]
    # text = list(set(text))
    dictionary = corpora.Dictionary([text])
    # print(dictionary.token2id)
    corpus = [dictionary.doc2bow([word]) for word in text]
    return models.ldamodel.LdaModel(corpus, num_topics=1,
                                    id2word=dictionary)


def get_text_from_paths(paths):
    texts = []
    for path in paths:
        # texts[path] = codecs.open(join(path, date + '.txt'),
        #                           'rb', 'utf-8').read()
        # texts.append(
        #     (path, codecs.open(join(path, date + '.txt'),
        #                        'rb', 'utf-8').read()))
        texts.append(codecs.open(path, 'rb', 'utf-8').read())
    return texts


def cosine_similarity(fullpaths, dates):
    print('dates: ', dates)
    dates = sorted(list(dates))
    results = []
    for date in dates:
        # In case next date exists, calculate cosine similarity from
        # news texts to tweets in next date too
        next_date_index = dates.index(date) + 1
        print('next_date_index', next_date_index)
        try:
            next_date = dates[next_date_index]
            print('next date:  ', next_date)
            paths = fullpaths + [fullpaths[2]]
            paths = list(map(lambda x: join(x, date + '.txt'), paths))
            paths[-1] = join(split(paths[-1])[0], next_date + '.txt')
        except Exception:
            paths = fullpaths
            paths = list(map(lambda x: join(x, date + '.txt'), paths))
        # Append path to files on date to list of fullpaths
        texts = get_text_from_paths(paths)
        print('date:  ', date)
        print('date + 1:  ', int(date) + 1)
        # print('paths:', texts.keys())
        # =============== COSINE SIMILARITY ==============
        tfidf = TfidfVectorizer(tokenizer=tokenize)
        tfs = tfidf.fit_transform(texts)
        cosine = (tfs * tfs.T)
        result = [int(date), cosine[(0, 2)], cosine[(1, 2)]]
        # print(cosine)
        print('cosine g1-tweet: ', cosine[(0, 2)])
        print('cosine folha-tweet: ', cosine[(1, 2)])
        if next_date in dates:
            result += [cosine[(0, 3)], cosine[(1, 3)]]
            print('cosine g1-tweet: ', cosine[(0, 3)])
            print('cosine folha-tweet: ', cosine[(1, 3)])
        else:
            result += [0.0, 0.0]
        print('result: ', result)
        results.append(result)
        # for key, value in cosine:
        #     print('key:  ', key)
        #     print('value:  ', value)
        print(tfs * tfs.T)
    header = 'date, g1-tweet-cur, folha-tweet-cur, g1-tweet-next, '
    header += 'folha-tweet-next'
    write_csv(join(RESULTS_DIR, 'weekly.csv'), header, array(results))


def find_topics(fullpaths, dates):
    # Append path to files on date to list of fullpaths
    for date in sorted(dates):
        paths = list(map(lambda x: join(x, date + '.txt'), fullpaths))
        texts = get_text_from_paths(paths)
        print(len(texts))
        print('date: ', date)
        # ============== LDA ===================
        # Run LDA in each text
        for text in texts:
            # print('path:  ', path)
            model = build_LDA_model(text)
            print(model.print_topics(num_words=3))
            # for key, topic in model.print_topics(num_topics=1, num_words=3):
            #     print('key: ', key)
            #     print('topic: ', topic)
            #     print('spl topic: ', list(map(lambda x: x.split('*'),
            #                                   topic.split('+'))))
            # print(model.print_topics(num_topics=3, num_words=3))


def write_csv(fullpath, header, data):
    savetxt(fullpath, data, fmt='%8f', delimiter=',', header=header)


if __name__ == "__main__":
    fullpaths = get_fullpath_by_dataset(WEEKLY)
    dates = get_intersecting_dates(fullpaths)
    # cosine_similarity(fullpaths, dates)
    find_topics(fullpaths, dates)
