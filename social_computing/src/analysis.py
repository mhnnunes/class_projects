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

import re
import sys
import codecs
import numpy as np
from os import getcwd
from os.path import join
from nltk.tokenize import *
from datetime import datetime
from nltk.corpus import stopwords
from dateutil.parser import parse
# from analyze_news import stringify_key

USERNAME = 0
DATE = 1
TEXT = 4


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


def grabUrls(text):
    """ ref: https://mail.python.org/pipermail/tutor/2002-September/017228.html
    """
    """Given a text string, returns all the urls we can find in it."""
    urls = '(?: %s)' % '|'.join("""http telnet gopher file wais
    ftp""".split())
    ltrs = r'\w'
    gunk = r'/#~:.?+=&%@!\-'
    punc = r'.:?\-'
    any = " ?%(ltrs)s%(gunk)s%(punc)s" % {'ltrs': ltrs,
                                          'gunk': gunk,
                                          'punc': punc}

    url = r"""
        \b                            # start at word boundary
            %(urls)s    :?             # need resource and a colon
            [%(any)s]  +?             # followed by one or more
                                      #  of any valid character, but
                                      #  be conservative and take only
                                      #  what you need to....
        (?=                           # look-ahead non-consumptive assertion
                [%(punc)s]*           # either 0 or more punctuation
                (?:   [^%(any)s]      #  followed by a non-url char
                    |                 #   or end of the string
                      $
                )
        )
        """ % {'urls': urls,
               'any': any,
               'punc': punc}

    url_re = re.compile(url, re.VERBOSE | re.MULTILINE)
    return url_re.findall(text)


def get_week_text(week):
    text = [tweet[TEXT] for tweet in week]
    return reduce(lambda x, y: x + ' ' + y, text)


def tokenize_remove_stopwords(text, language='portuguese'):
    tokenizer = RegexpTokenizer(r'\w+')
    # Tokenize
    tokens = tokenizer.tokenize(text)
    stops = set(stopwords.words(language))
    # Remove stopwords
    return filter(lambda x: x not in stops, tokens)


def remove_URLs(text):
    # Remove space after start of URL
    text = text.replace('//\ ', '//')
    text = text.replace('www. ', 'www.')
    urls = grabUrls(text)
    # Remove URLs and mentions
    mentions = re.findall(r'@\w+', text)
    for removable in (urls + mentions):
        text = text.replace(removable, '')
    text = re.sub(r'pic.twitter.com/\w+', '', text)
    return text


def remove_dates(text):
    return re.sub(r'(?:(?:[0-9]{2}[:\/,]){2}[0-9]{2,4}|am|pm)', '', text)


def pre_process_text(text):
    # Remove double quotes
    text = text.replace('"', '')
    # Remove URLs and mentions
    text = remove_URLs(text)
    # Remove dates
    text = remove_dates(text)
    # All to lower case
    text = text.lower()
    # Tokenize and remove stopwords
    filtered = tokenize_remove_stopwords(text)
    compressed = reduce(lambda x, y: x + ' ' + y, filtered)
    compressed = re.sub(r' \w ', ' ', compressed)
    return compressed


def get_date_info(date):
    current_year, current_week, day_of_week = date.isocalendar()
    month = date.month
    day_of_month = date.day
    return {
        'year': current_year,
        'month': month,
        'day': day_of_month,
        'week': current_week
    }


def get_week(date):
    current_year, current_week, day_of_week = date.isocalendar()
    return current_week


def cluster_by_day(rows):
    days = {}
    for row in rows:
        date = row[DATE]
        day = date.day
        month = date.month
        year = date.year
        # current_year, current_week, day_of_week = date.isocalendar()
        if (day, month, year) not in days.keys():
            days[(day, month, year)] = row[TEXT]
            # days[(day, month, year)] = 1
        else:
            days[(day, month, year)] += ' ' + row[TEXT]
            # days[(day, month, year)] += 1
    return days


def clusterize_by_week(rows):
    weeks = []
    clusters = []
    tweets_this_week = []
    for row in rows:
        current_week = get_week(row[DATE])
        if current_week not in weeks:
            # New week
            weeks.append(current_week)
            if tweets_this_week:
                clusters.append(tweets_this_week)
            tweets_this_week = []
        tweets_this_week.append(row)
    return weeks, clusters


def read_input(filename):
    try:
        # Read rows from input
        with codecs.open(filename, 'rb', 'utf-8') as csvfile:
            # Read header line
            row1 = csvfile.readline().split('|')
            rows = []
            # Read and process lines
            # Problem on splitting on a character, this character may be
            # contained on the tweets text
            for i, row in enumerate(csvfile):
                spl = row.split("|")
                while len(spl) > len(row1):
                    spl[TEXT] += spl[TEXT + 1]
                    del spl[TEXT + 1]
                rows.append(spl)
    except Exception as e:
        print("ERROR READING INPUT: ", str(e))
        print(row)
        sys.exit(-1)
    return rows


def write_output(filename, text):
    try:
        with codecs.open(filename, 'wb', 'utf-8') as out:
            out.write(text)
    except Exception as e:
        print('ERROR ON write ', filename)
        print(e)
        sys.exit(-1)


def write_weeks(weeks, week_text):
    for index, week in enumerate(weeks):
        try:
            text = week_text[index]
        except Exception as e:
            print('could not find text for index ', index)
            print(e)
            return
        print('week ', week)
        filename = join('tweet-analyses', str(week) + '.txt')
        print(filename)
        write_output(filename, text)


def write_days(days):
    DAILY_DIR = 'tweets/analyses/daily'
    print('==================== writing')
    for key, value in days.items():
        # print key
        (d, m, y) = key
        write_output(join(getcwd(), DAILY_DIR, stringify_key(key) +
                          '.txt'), value)


def main(filename):
    # Read input
    rows = read_input(join(getcwd(), 'tweets', filename))
    # Convert the date to datetime format, for all rows
    rows = list(map(lambda x: x[:DATE] + [parse(x[DATE])] + x[DATE + 1:],
                    rows))
    # weeks, clusters = clusterize_by_week(rows)
    days = cluster_by_day(rows)
    # print(days.keys(), len(days.keys()))
    result = []
    # for day in sorted(list(days.keys()),
    #                   key=lambda x: datetime.strptime(stringify_key(x),
    #                                                   '%Y_%m_%d')):
    #     date = datetime.strptime(stringify_key(day), '%Y_%m_%d')
    #     if date.year > 2013:
    #         # print(stringify_key(day), days[day])
    #         result.append([date.strftime('%b_%d'), days[day]])
    # initial_date = datetime.strptime(result[0][0], '%Y_%m_%d')
    # new_result = list(map(lambda x: [datetime.strptime(x[0], '%Y_%m_%d'), x[0]], result))
    # print(result)
    # np.savetxt(join(getcwd(), 'tweets', 'analyses', 'daily',
    #                 'mapping_tweets_daily.csv'),
    #            np.array(result, dtype=object), fmt='%s,%d', delimiter=',',
    #            header='datedelta, tweets')
    # print(weeks, len(weeks), len(clusters))
    # # print get_week_text(clusters[0])
    # week_text = [get_week_text(week) for week in clusters]
    # # Process text!!
    for key, value in days.items():
        days[key] = pre_process_text(value)
        days[key] = re.sub(r' \w ', ' ', days[key])
    # processed_text = [pre_process_text(text) for text in week_text]
    # Remove single letters from processed text
    # processed_text = [re.sub(r' \w ', ' ', text) for text in processed_text]
    # # Write output
    write_days(days)
    # write_weeks(weeks, processed_text)


if __name__ == "__main__":
    filename = "output_got.csv"
    main(filename)
