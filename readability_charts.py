#!/usr/bin/env python
#
# Create charts comparing textual and sentiment analysis metrics
# from text files given as command-line arguments.
#
# (C) Copyright 2017 Diomidis Spinellis
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
import sys
from textblob import TextBlob
from textstat.textstat import textstat

# Functions for calculating metrics
def lexical_variety(text):
    """Return the type-token ratio of the text"""
    words = text.split()
    unique = {}
    for w in words:
        unique[w] = 1
    return len(unique) / len(words) * 100

def polarity(text):
    """Return the text's sentiment polarity (-1 negative, 1 positive)"""
    return TextBlob(text).sentiment.polarity

def subjectivity(text):
    """Return the text's sentiment subjectivity (0 objective, 1 subjective)"""
    return TextBlob(text).sentiment.subjectivity

# Calculated metrics: name, function that calculates them, and chart's color
metrics = [
    {
        'name': 'Polarity',
        'f': polarity,
        'color': 'IndianRed',
    },
    {
        'name': 'Subjectivity',
        'f': subjectivity,
        'color': 'DarkTurquoise',
    },
    {
        'name': 'SMOG index',
        'f': textstat.smog_index,
        'color': 'GoldenRod',
    },
    {
        'name': 'Number of words',
        'f': textstat.lexicon_count,
        'color': 'LightBlue',
    },
    {
        'name': 'Lexical variety',
        'f': lexical_variety,
        'color': 'DarkSeaGreen',
    },
]

# Go though all command-line arguments adding a record for each
# analyzed speech
records = []
for file_name in sys.argv[1:]:
    with open(file_name, 'r') as myfile:
        data = myfile.read().replace('\n', ' ')
        # Parse a speech file name of the form: First M. Last-YEAR.txt
        parts = re.search(r'speeches/((.)[^ ]*( (.)\.)? ([^ ]+))-(\d\d\d\d).txt', file_name)
        full_name = parts.group(1)
        first_name = parts.group(2)
        middle_initial = parts.group(4) or ''
        last_name = parts.group(5)
        year = parts.group(6)
        records.append(
            (year,
             str(first_name + middle_initial + ' ' + last_name + "\n" + year),
             full_name
             ) + tuple([m['f'](data) for m in metrics]))

# Convert records into a data frame, which can be used for charting
data = np.zeros((len(records),), dtype=[('year', 'i4'),
                                        ('label', 'U20'),
                                        ('full_name', 'U30')] + [
                                            (x['name'], 'f4') for x in metrics])
data[:] = records
df = pd.DataFrame(data)
df = df.sort_values(by=['year'])

# Create a bar chart for each one of the metrics
for m in metrics:
    sns.set_style("darkgrid")
    plt.xticks(rotation=45)
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.gcf().set_size_inches(10, 5)
    name = m['name']
    sns.reset_orig()
    g = sns.barplot(x="label", y=name, data=df, color=m['color'])
    g.set_xticklabels(g.get_xticklabels(), rotation=40)
    g.set(ylabel=name, xlabel='')
    file_name = name.replace(' ', '_') + '.png'
    g.get_figure().savefig(file_name, dpi=150)
    plt.gcf().clear()
