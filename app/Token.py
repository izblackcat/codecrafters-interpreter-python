class Token:

    KEYWORDS = {
        "and": "AND",
        "class": "CLASS",
        "else": "ELSE",
        "false": "FALSE",
        "for": "FOR",
        "fun": "FUN",
        "if": "IF",
        "nil": "NIL",
        "or": "OR",
        "print": "PRINT",
        "return": "RETURN",
        "super": "SUPER",
        "this": "THIS",
        "true": "TRUE",
        "var": "VAR",
        "while": "WHILE",
    }

    def __init__(self, token_type, lexeme, literal):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"
