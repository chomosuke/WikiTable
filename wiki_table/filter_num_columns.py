from column import Column

import re
# from https://stackoverflow.com/questions/638565/parsing-scientific-notation-sensibly
num = re.compile("^[+\-]?\d*(?:\.\d+)?(?:[eE][+\-]?\d+)?")
start_with_num = re.compile("^[+\-]?\.?\d+.*$")
num_endstr = re.compile("^[+\-]?\d*(?:\.\d+)?(?:[eE][+\-]?\d+)?$")
whitespace = re.compile('^ *$')

# the hope is that this parser is powerful enough to recognize all possible date or time format
from dateutil import parser

def filter_num_columns(columns: list[Column]) -> list[Column]:
    columns = list(filter(is_num_column, columns))
    for column in columns:
        for i in range(len(column.content)):
            match = num.match(column.content[i]).group(0)
            column.content[i] = float(match)
    return columns

def is_num_column(column: Column) -> bool:

    if len(column.content) == 0:
        return False # an empty column isn't a num column

    # looking for a cell to set is_num = False
    for cell in column.content:
        if start_with_num.match(cell):
            try:
                parse_res = parser.parse(cell, fuzzy_with_tokens=True)
                # parsed successfully

                # check if accidentally parsed a integer into datetime
                for token in parse_res[1]:
                    cell = cell.replace(token, '')
                if num_endstr.match(cell): # num but guaranteed to match the whole string
                    continue

                # remove white space from fuzzy_tokens
                tokens = list(filter(lambda token : whitespace.match(token) == None, parse_res[1]))

                # check if the start of the string has been parsed into datetime
                if len(tokens) == 1:
                    unparsed = parse_res[1][0]
                    if unparsed == cell[-len(unparsed):]:
                        # the start of the string has been parsed to datetime
                        return False
                elif len(tokens) == 0:
                    # entire string has been parsed to datetime
                    return False
            except:
                # does not parse to date
                continue
        else:
            return False
    return True
