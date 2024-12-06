class Token:

    TOKENS = {
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN",
        "{": "LEFT_BRACE",
        "}": "RIGHT_BRACE",
        "*": "STAR",
        ".": "DOT",
        ",": "COMMA",
        "+": "PLUS",
        "-": "MINUS",
        ";": "SEMICOLON",
        "/": "SLASH",
        "=": "EQUAL",
        "<": "LESS",
        ">": "GREATER",
        "!": "BANG",
    }

    def __init__(self, token_type, lexeme, literal):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"
