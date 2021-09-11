class Column:
    name: str
    content: list[str]

    def __init__(self, name, content):
        self.name = name
        self.content = content