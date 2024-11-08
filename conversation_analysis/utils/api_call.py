from enum import Enum


class ApiCallStyle(Enum):
    # ELMB = r'[a-zA-Z]\w* [\(\w]'
    # ELMG = r'[a-zA-Z]\w* [\(\w]'
    PYTHON = r'[a-zA-Z]\w*\s*\('
    CLOJURE = r'\([a-zA-Z]\w* [a-zA-Z_]\w*'
    RACKET = r'\([a-zA-Z]\w* [a-zA-Z_]\w*'
    JAVASCRIPT = r'[a-zA-Z]\w*\('  # e.g., functionName(argument)
    CSHARP = r'[a-zA-Z]\w*\('  # e.g., functionName(argument)
    SWIFT = r'[a-zA-Z]\w*\('  # e.g., functionName(argument)

    def __repr__(self):
        return self.name