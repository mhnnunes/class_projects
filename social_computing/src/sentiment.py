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


import csv
import codecs
import numpy as np
from os import getcwd
from os import listdir
from numpy import array
from os.path import join
from numpy import savetxt
from os.path import isfile
from functools import reduce
from datetime import datetime
from polyglot.text import Text
from analysis import stringify_key

FOLHA_DIR = 'folha-texts'
G1_DIR = 'g1-texts'
TWEETS_DIR = 'tweets'

WEEKLY = join('analyses', 'by-week')
DAILY = join('analyses', 'daily')


def get_text_polarity(text):
    if text is None:
        return None
    # Get polyglot text object for tweets text and news text
    poly_text = Text(text)
    # Return list containing words polarity for each word in text
    return list(map(lambda x: float(x.polarity), poly_text.words))


def get_dates_by_dataset(fullpaths):
    # Get dates for each dataset
    print('fullpaths: ', fullpaths)
    dates = map(listdir, fullpaths)
    dates = map(lambda x: map(lambda y: y.split('.')[0], x), dates)
    dates = map(set, dates)
    return dates


def get_union_of_dates(fullpaths):
    dates = get_dates_by_dataset(fullpaths)
    # Get union of dates
    print('dates before intersection:  ', dates)
    return dates[0].union(dates[1]).intersection(dates[2])
    # return reduce(lambda x, y: x.union(y), dates)


def get_intersecting_dates(fullpaths):
    dates = get_dates_by_dataset(fullpaths)
    # Intersect the sets
    print('dates before intersection:  ', dates)
    return reduce(lambda x, y: x.intersection(y), dates)
    # return dates[0].intersection(dates[1]).intersection(dates[2])


def get_fullpath_by_dataset(frequency):
    fullpath_g1 = join(getcwd(), G1_DIR, frequency)
    fullpath_folha = join(getcwd(), FOLHA_DIR, frequency)
    fullpath_tweets = join(getcwd(), TWEETS_DIR, frequency)
    # return [fullpath_g1, fullpath_folha]
    return [fullpath_g1, fullpath_folha, fullpath_tweets]


def get_polarity_given_paths(paths):
    texts = {}
    for index, path in enumerate(paths):
        if isfile(path):
            if index == 0:
                texts['G1'] = codecs.open(path, 'rb', 'utf-8').read()
                texts['G1'] = np.mean(np.array(get_text_polarity(texts['G1'])))
            elif index == 1:
                texts['Folha'] = codecs.open(path, 'rb', 'utf-8').read()
                texts['Folha'] = \
                    np.mean(np.array(get_text_polarity(texts['Folha'])))
            else:
                texts['Twitter'] = codecs.open(path, 'rb', 'utf-8').read()
                texts['Twitter'] = \
                    np.mean(np.array(get_text_polarity(texts['Twitter'])))
        else:
            if index == 0:
                texts['G1'] = None
            elif index == 1:
                texts['Folha'] = None
            else:
                texts['Twitter'] = None
    return texts


def get_medias_polarity(frequency):
    polarities = []
    # Save fullpaths for all medias
    fullpaths = get_fullpath_by_dataset(frequency)
    # print('fullpaths: ', )
    # Get dates in common in all medias
    dates = get_union_of_dates(fullpaths)
    # dates = get_intersecting_dates(fullpaths)
    print('dates', dates)
    dates = sorted(list(map(lambda date: datetime.strptime(stringify_key(date),
                            '%Y_%m_%d'), dates)))
    for date in dates:
        paths = list(map(lambda x: join(x, str(date.strftime('%Y_%m_%d')) +
                                        '.txt'), fullpaths))
        print('date (week number or full date):  ',
              date.strftime('%Y_%m_%d'))
        texts = get_polarity_given_paths(paths)
        d = date.strftime('%b_%d')
        result = [d,
                  texts['G1'] if texts['G1'] is not None else None,
                  texts['Folha'] if texts['Folha'] is not None
                  else None,
                  texts['Twitter'] if texts['Twitter'] is not None
                  else None]
        result = list(map(lambda x:
                          np.array(x) if x is not None else np.nan, result))
        print('l: ', result)
        # l = reduce(lambda x, y: np.concatenate((x, y)), l)
        result = np.array(result, dtype=object)
        polarities.append(result)
    #     # Get text polarity for each dataset
        # for key, text in texts.items():
        #     pol = get_text_polarity(text)
        #     # texts[key] = np.mean(np.array(pol))
        #     polarities.append([d, key, np.mean(np.array(pol, dtype=float))
        #                        if pol is not None else None])
    #     # Apply mean to polarities, obtain avg polarity by dataset
    #     avg_pol = map(lambda x: np.mean(np.array(x)), pol)

    #     print('avg g1 polarity: ', avg_pol[0])
    #     print('avg folha polarity: ', avg_pol[1])
    #     print('avg tweets polarity: ', avg_pol[2])
    #     print([date] + avg_pol)
    #     polarities.append([date] + avg_pol)

    return polarities


def write_csv(fullpath, header, rowlist):
    with open(fullpath, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in rowlist:
            writer.writerow(row)


def analyze_text_polarities():
    # weekly_polarities = get_medias_polarity(WEEKLY)
    # print(weekly_polarities)
    # fullpath = join(getcwd(), 'sentiment_analysis_weekly.csv')
    # header = ['week', 'avg.g1', 'avg.folha', 'avg.tweet']
    # rowlist = sorted(weekly_polarities, key=lambda x: x[0])
    # write_csv(fullpath, header, rowlist)
    print(' =====  ANALYZING DAILY  ======')
    daily_polarities = get_medias_polarity(DAILY)
    # fullpath = join(getcwd(), 'sentiment_analysis_daily.csv')
    # header = ['week', 'avg.g1', 'avg.folha', 'avg.tweet']
    header = 'date,G1,Folha,Twitter'
    print(array(daily_polarities, dtype=object))
    savetxt(join(getcwd(), 'news_twitter_sentiment.csv'),
            array(daily_polarities, dtype=object),
            delimiter=',', fmt='%s,%6f,%6f,%6f', header=header)
    # rowlist = sorted(daily_polarities, key=lambda x:
    #                  datetime.strptime(x[0], '%Y_%m_%d'))
    # write_csv(fullpath, header, rowlist)


if __name__ == "__main__":
    analyze_text_polarities()
