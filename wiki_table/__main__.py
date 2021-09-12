# the cmd interface will be here.
from filter_num_columns import filter_num_columns
from html_to_columns import html_to_columns
import urllib.request
import matplotlib.pyplot as plt

url = input('pls gib wikipedia url: ')
with urllib.request.urlopen(url) as response:
    html = response.read()
    columns = html_to_columns(html)
    num_columns = filter_num_columns(columns)
    plt.bar(range(len(num_columns[0].content)), num_columns[0].content)
    plt.ylabel(num_columns[0].name)
    plt.savefig('plt')
