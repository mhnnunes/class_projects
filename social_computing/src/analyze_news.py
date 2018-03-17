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
from sys import exit
from os import getcwd
from os import listdir
from os.path import join
from nltk import FreqDist
from os.path import isfile
# from analysis import get_week
from datetime import datetime
from dateutil.parser import parse
from analysis import write_output
from analysis import get_date_info
from analysis import pre_process_text
from json_functions import load_utf8_JSON
from analysis import tokenize_remove_stopwords

TWEETS_DIR = 'tweets'
FOLHA_DIR = 'folha-texts'
G1_DIR = 'g1-texts'

DAILY = join('analyses', 'daily')
WEEKLY = join('analyses', 'by-week')


def most_frequent_words(filename, amount):
    with codecs.open(filename, 'rb', 'utf-8') as f:
        text = f.read()
        tokens = tokenize_remove_stopwords(text)
        fd = FreqDist(tokens)
        most_frequent = []
        for word, freq in fd.most_common(amount):
            most_frequent.append((word, freq))
    return most_frequent


def write_csv(filename, rows):
    try:
        with codecs.open(filename, 'wb', 'utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in rows:
                writer.writerow(row)
    except Exception as e:
        print('ERROR on write: ', e)


def joint_analysis(analysis_frequency=WEEKLY, amt_most_frequent=20):
    for file in listdir(analysis_frequency):
        spl = file.split('_')
        week = int(spl[1].split('.')[0])
        # Get tweets' filename
        tweets_file = join(TWEETS_DIR, str(week) + '.txt')
        # Get frequencies
        most_common_tweet = most_frequent_words(tweets_file, amt_most_frequent)
        most_common_news = most_frequent_words(join(analysis_frequency, file),
                                               amt_most_frequent)
        # Summarize analyses into rows
        rows = []
        for key, item in enumerate(most_common_tweet):
            rows.append([item[0], item[1], most_common_news[key][0],
                        most_common_news[key][1]])
        # Write csv
        write_csv('result_week_' + str(week) + '.csv', rows)


def build_key_by_frequency(date, frequency=WEEKLY):
    date_info = get_date_info(date)
    if frequency == WEEKLY:
        return date_info['week']
    elif frequency == DAILY:
        return (date_info['day'], date_info['month'], date_info['year'])
    else:
        # ERROR!
        print("ERROR on build_key_by_frequency:  ", str(date))
        exit(-1)


def cluster_by_frequency(texts, frequency=WEEKLY, date_field='timestamp'):
    dates = {}
    for file in texts:
        textdate = parse(file[date_field])
        candidate_key = build_key_by_frequency(textdate, frequency)
        if candidate_key not in dates.keys():
            # dates[candidate_key] = file['text']
            dates[candidate_key] = 1
        else:
            # dates[candidate_key] += (' ' + file['text'])
            dates[candidate_key] += 1
    return dates


def stringify_key(key):
    if isinstance(key, tuple):
        if key[1] >= 10:
            if key[0] >= 10:
                return str(key[2]) + '_' + str(key[1]) + '_' + str(key[0])
            else:
                return str(key[2]) + '_' + str(key[1]) + '_' + '0' + str(key[0])
        else:
            if key[0] >= 10:
                return str(key[2]) + '_' + '0' + str(key[1]) + '_' + str(key[0])
            else:
                return str(key[2]) + '_' + '0' + str(key[1]) + '_' + '0' + str(key[0])
    else:
        return str(key)

def pre_process_and_write_results(analyses, directory,
                                  analysis_frequency=WEEKLY):
    for key, values in analyses.items():
        processed = pre_process_text(values)
        write_output(join(getcwd(), directory, analysis_frequency,
                     stringify_key(key) + '.txt'), processed)


def import_files(directory):
    files_in_dir = []
    for file in listdir(directory):
        # print('analysing file:  ', file)
        fullpath = join(getcwd(), directory, file)
        if isfile(fullpath):
            # print('loading file:  ', file)
            dicts = load_utf8_JSON(fullpath)
            file_info = dicts[0]
            files_in_dir.append(file_info)
    return files_in_dir


def main():
    # Import and cluster Folha de São Paulo files
    files_in_dir = import_files(FOLHA_DIR)
    days = cluster_by_frequency(files_in_dir, DAILY, 'timestamp')
    # print(days)
    # print(days.keys())
    # pre_process_and_write_results(days, FOLHA_DIR, DAILY)
    # weeks = cluster_by_frequency(files_in_dir, WEEKLY, 'timestamp')
    # # print(weeks.keys())
    # pre_process_and_write_results(weeks, FOLHA_DIR, WEEKLY)
    # # Import and cluster G1 files
    files_in_dir = import_files(G1_DIR)
    result = []
    daysg1 = cluster_by_frequency(files_in_dir, DAILY, 'lastModified')
    print("G1: ", list(map(lambda x: stringify_key(x), daysg1.keys())))
    for day in sorted(list(set(daysg1.keys()).union(set(days.keys()))),
                      key=lambda x: datetime.strptime(stringify_key(x),
                                                      '%Y_%m_%d')):
        # daily_result = np.empty((3), dtype=object)
        date = datetime.strptime(stringify_key(day), '%Y_%m_%d')
        if date.year > 2013:
            result.append([date.strftime('%b_%d'),
                           days[day] if day in days.keys() else 0,
                           daysg1[day] if day in daysg1.keys() else 0])
    print('result: ', result)
    np.savetxt(join(getcwd(), 'news_daily.csv'),
               np.array(result, dtype=object), fmt='%s,%d,%d', delimiter=',',
               header='datedelta, folha, g1')
    # pre_process_and_write_results(daysg1, G1_DIR, DAILY)
    # weeks = cluster_by_frequency(files_in_dir, WEEKLY, 'lastModified')
    # # print(weeks.keys())
    # pre_process_and_write_results(weeks, G1_DIR, WEEKLY)


if __name__ == "__main__":
    main()
