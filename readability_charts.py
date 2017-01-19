#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
import sys
from textstat.textstat import textstat

metrics = [
    'SMOG index',
    'Flesh reading ease',
    'Funning fog index',
    'Number of difficult words',
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
             full_name,
             textstat.smog_index(data),
             textstat.flesch_reading_ease(data),
             textstat.gunning_fog(data),
             textstat.difficult_words(data)
        ))

data = np.zeros((len(records),), dtype=[('year', 'i4'),
                                        ('label', 'U20'),
                                        ('full_name', 'U30')] + [
                                            (x, 'f4') for x in metrics])
data[:] = records
df = pd.DataFrame(data)
df = df.sort_values(by=['year'])
print(records)
plt.xticks(rotation=45)
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().set_size_inches(10, 5)

for plot in metrics:
    g = sns.barplot(x="label", y=plot, data=df, color='green')
    g.set_xticklabels(g.get_xticklabels(), rotation=30)
    g.set(ylabel=plot, xlabel='Inaugural Address')
    file_name = plot.replace(' ', '_') + '.png'
    g.get_figure().savefig(file_name, dpi=150)
