to run all tests, do `python -m unittest discover wiki_table`

What is a numeric column?
Sometimes numeric column can have strange unit attached with them, it's impossible to predict all possible units or postfix, hence we can only exclude the column that start with numbers but isn't numerical. The only kind of column of that sort I can think of is time and date.

Therefore, any column with all of it's cell starting with a number that's can't be interpreted as time or date is a numeric column.
