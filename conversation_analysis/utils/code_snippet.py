from enum import Enum


class CodeSnippetKind(Enum):
    INLINE = r'(?<!`)`(?!`).*?(?<!`)`(?!`)'
    MULTILINE = r"(?s)(?P<quotes>```|''').*?(?P=quotes)"

    def __repr__(self):
        return self.name