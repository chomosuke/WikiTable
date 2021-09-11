from bs4.element import whitespace_re
from column import Column

import re
num = re.compile("[0-9]*\.?[0-9]+")
start_with_num = re.compile("[0-9]*\.?[0-9]+.*")
integer = re.compile("^[0-9]+$")
whitespace = re.compile('^ *$')

# the hope is that this parser is powerful enough to recognize all possible date or time format
from dateutil import parser

def filter_num_columns(columns: list[Column]) -> list[Column]:
    columns = list(filter(is_num_column, columns))
    for column in columns:
        for i in range(len(column.content)):
            column.content[i] = float(num.match(column.content[i]).group(0))
    return columns

def is_num_column(column: Column) -> bool:
    # looking for a cell to set is_num = False
    for cell in column.content:
        if start_with_num.match(cell):
            try:
                parse_res = parser.parse(cell, fuzzy_with_tokens=True)
                # parsed successfully

                # check if parsed number into time
                for token in parse_res[1]:
                    cell = cell.replace(token, '')
                if integer.match(cell):
                    continue

                # remove white space from fuzzy_tokens
                tokens = list(filter(lambda token : whitespace.match(token) == None, parse_res[1]))
                if len(tokens) == 1:
                    unparsed = parse_res[1][0]
                    if unparsed == cell[-len(unparsed):]:
                        # the start of the string has been parsed to time
                        return False
                elif len(tokens) == 0:
                    # entire string has been parsed to time
                    return False
            except:
                # does not parse to date
                continue
        else:
            return False
    return True
