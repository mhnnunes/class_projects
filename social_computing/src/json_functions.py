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

from json import loads
from json import dump
import codecs


def load_utf8_JSON(fullpath):
    """ Reads a .json (encoded using UTF-8) file line by line, appending each
        loaded dictionary into a list. String objects within each dictionary
        will be encoded using UTF-8.
    Arguments:
        fullpath {str} -- full path to file, including extensions
    Returns:
        dicts {list(dict)} -- list of dictionaries read from file
    """
    dicts = []
    for line in codecs.open(fullpath, 'rb', 'utf-8'):
        dicts.append(loads(line, encoding='utf-8'))
    return dicts


def dump_utf8_JSON(fullpath, data):
    """ Serializes the data (list of dictionaries) and writes it to a
    .json file, assuming the extesion is contained in the full path
    passed as argument.
    Arguments:
        fullpath {str} -- full path to file, including extensions
        data {list(dict)} -- list of objects to be written to the file
    """
    with codecs.open(fullpath, 'wb', 'utf-8') as jsonfile:
        dump(data, jsonfile, ensure_ascii=False)
