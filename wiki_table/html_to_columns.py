from column import Column
from bs4 import BeautifulSoup

def html_to_columns(html: str) -> list[Column]:
    soup = BeautifulSoup(html, 'html.parser')

    # only wikitable class to filter out tables in references
    tables = soup.find_all('table', class_='wikitable')

    all_columns = []
    for table in tables:
        # all the wikipedia table I can find have a tbody
        columns = []
        
        # Weirdly, no page source of wikitable contain a thead, even though it shows up in the browser
        # I think it could be javascript generated
        trs = table.tbody.find_all('tr', recursive=False)

        # create Columns
        need_skip_rows = 0
        if all(t.name == 'th' for t in trs[0].find_all(recursive=False)):
            # there are headers for this table, 
            # find all header and create Columns
            first_line_ths = trs[0].find_all('th', recursive=False)

            need_fill_columns = []
            for th in first_line_ths:
                # in case there are nested headers
                if get_span(th, 'colspan') == 1:
                    columns.append(Column(th.get_text().strip(), []))
                else:
                    for i in range(get_span(th, 'colspan')):
                        columns.append(Column('', []))
                        need_fill_columns.append(columns[-1])

            need_skip_rows += 1 # need to skip some rows in tbody later

            # time to check for more ths
            for tr in trs[need_skip_rows:]:
                ths = tr.find_all(recursive=False)
                if all(t.name == 'th' for t in ths):
                    i = 0
                    j = 0
                    while i < len(ths):
                        # check if rowspan fill the remaining rows for head
                        if get_span(ths[i], 'colspan') == 1:
                            need_fill_columns[j].name = ths[i].get_text().strip()
                            i += 1
                            j += 1
                        else:
                            j += get_span(ths[i], 'colspan')
                            i += 1
                    need_skip_rows += 1
                else:
                    break
        else:
            # there's no header for this table
            # use the first row to create columns
            for _ in trs[0].find_all(recursive=False):
                columns.append(Column('', []))

        # we need a datastructure to keep all the cells with rowspan > 1
        # now i've written that down, it's actually pretty easy
        # an array recording the excess number of rowspan of the last cell of the columns
        rowspans = []
        for _ in columns:
            rowspans.append(0)

        for tr in trs[need_skip_rows:]:
            tds = tr.find_all(lambda tag: tag.name == 'td' or tag.name == 'th')

            # skip footer (or header in middle of a table for some reason)
            # if a row only have th, it's a footer/header
            # if a row has any cell that take more than 1 column and it's not empty, it's a footer/header
            if (all(t.name == 'th' for t in tds)
             or any(get_span(t, 'colspan') != 1 and len(t.get_text().strip()) != 0 for t in tds)):
                continue

            i = 0
            j = 0
            while i < len(tds):
                # react to rowspans
                while j < len(rowspans) and rowspans[j] > 0:
                    rowspans[j] -= 1
                    j += 1
                if j >= len(rowspans):
                    break

                # record rowspans
                rowspans[j] += get_span(tds[i], 'rowspan') - 1

                # replace <br/> with \n so one cell can be split into multiple cell later
                # this addresses test_html_to_columns.py line 28
                # credit to https://stackoverflow.com/questions/12545897/convert-br-to-end-line
                for br in tds[i].find_all('br'):
                    br.replace_with('\n')

                cells = (tds[i].get_text()
                    # replace all the non-breaking white space with ordinary white space
                    .replace('\xa0', ' ')
                    .strip()).split('\n')

                for cell in cells:
                    if len(cell) != 0: # empty cell => missing data
                        columns[j].content.append(cell)
                j += 1
                i += 1

        # filter out possible index
        # for length <= 3, can't definitively know if it's index or just coincidence
        isIndex = len(columns[0].content) > 3
        for i in range(len(columns[0].content) - 1):
            try:
                index1 = int(columns[0].content[i])
                index2 = int(columns[0].content[i + 1])
            except:
                isIndex = False
                break
            if index1 + 1 != index2:
                isIndex = False
                break
        if isIndex:
            columns = columns[1:]

        all_columns.extend(columns)
    return all_columns

def get_span(th, span):
    try:
        return int(th[span])
    except:
        return 1