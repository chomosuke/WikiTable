from typing import NamedTuple

Column = NamedTuple('Column', [('name', str), ('content', [str])])

def html_to_columns(html: str) -> list(Column):
    pass
