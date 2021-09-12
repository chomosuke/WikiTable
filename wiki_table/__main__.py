# the cmd interface will be here.
from filter_num_columns import filter_num_columns
from html_to_columns import html_to_columns
import urllib.request
import matplotlib.pyplot as plt

import re
wikiurl = re.compile('https?://.*\.wikipedia\.org')

while True:
    url = input('pls enter wikipedia url: ')
    if wikiurl.match(url) == None:
        print('not a valid wikipedia url')
        continue
    try:
        response = urllib.request.urlopen(url)
        break
    except:
        print('not a valid wikipedia url or bad internet connection')
html = response.read()
columns = html_to_columns(html)
num_columns = filter_num_columns(columns)
for num_column in num_columns:
    print('found column with head:', num_column.name)
    print('and content:', num_column.content)
    go_ahead = input('would you like to go ahead with this column? ([n/no = no]/[any other input = yes])')
    if go_ahead == 'n' or go_ahead == 'no':
        continue
    path = input('where would you want your image to be (relative path, default plt.png): ')
    if path == '':
        path = 'plt.png'
    plt.figure()
    plt.bar(range(len(num_column.content)), num_column.content)
    plt.ylabel(num_column.name)
    plt.savefig(path)
    plt.close()
print('no numeric column found')