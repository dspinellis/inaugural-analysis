#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
import sys
from textstat.textstat import textstat

metrics = [
    {
        'name': 'SMOG index',
        'f': textstat.smog_index,
        'color': 'BurlyWood',
    },
    {
        'name': 'Flesh reading ease',
        'f': textstat.flesch_reading_ease,
        'color': 'GoldenRod',
    },
    {
        'name': 'Gunning fog index',
        'f': textstat.gunning_fog,
        'color': 'IndianRed',
    },
    {
        'name': 'Number of words',
        'f': textstat.lexicon_count,
        'color': 'LightBlue',
    },
    {
        'name': 'Number of difficult words',
        'f': textstat.difficult_words,
        'color': 'Indigo',
    },
]

records = []
for file_name in sys.argv[1:]:
    with open(file_name, 'r') as myfile:
        data = myfile.read().replace('\n', ' ')
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

data = np.zeros((len(records),), dtype=[('year', 'i4'),
                                        ('label', 'U20'),
                                        ('full_name', 'U30')] + [
                                            (x['name'], 'f4') for x in metrics])
data[:] = records
df = pd.DataFrame(data)
df = df.sort_values(by=['year'])
plt.xticks(rotation=45)
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().set_size_inches(10, 5)

print(df)
for m in metrics:
    name = m['name']
    print(name)
    sns.reset_orig()
    g = sns.barplot(x="label", y=name, data=df, color=m['color'])
    g.set_xticklabels(g.get_xticklabels(), rotation=30)
    g.set(ylabel=name, xlabel='Inaugural Address')
    file_name = name.replace(' ', '_') + '.png'
    g.get_figure().savefig(file_name, dpi=150)
