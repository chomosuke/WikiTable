from column import Column
from bs4 import BeautifulSoup

def html_to_columns(html: str) -> list[Column]:
    soup = BeautifulSoup(html, 'html.parser')

    # class exist to filter out tables in references
    tables = soup.find_all('table', class_='wikitable')

    all_columns = []
    for table in tables:
        # all the wikipedia table I can find have a tbody
        columns = []
        if table.thead != None: # has a thead
            need_skip_row = False
            for th in table.thead.tr.find_all('th', recursive=False):
                columns.append(Column(th.get_text().strip(), []))
        else: # only have tbody
            need_skip_row = True # need to skip the first row in tbody later
            for th in table.tbody.find('tr', recursive=False).find_all('th', recursive=False):
                columns.append(Column(th.get_text().strip(), []))

        trs = table.tbody.find_all('tr', recursive=False)
        for tr in trs:
            if need_skip_row:
                need_skip_row = False
                continue
            tds = tr.find_all(lambda tag: tag.name == 'td' or tag.name == 'th')
            for i in range(len(tds)):
                columns[i].content.append(tds[i].get_text().replace('\xa0', ' ').strip())

        all_columns.extend(columns)
    return all_columns
