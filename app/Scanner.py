class Scanner:

    # map : (symbol: NAME) for ex: (',': 'COMMA')

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

    def __init__(self, source_file) -> None:
        self.source_file = source_file
        self.current = 0
        self.errors = []

    def scan_file(self):
        while not self.is_the_last_token():
            token, token_name = self.scan_token()
            if token and token_name:
                print(f"{token_name} {token} null")
        print("EOF  null")
        return self.errors

    def scan_token(self):
        # this is what iterates the source file:
        token = self.advance()
        token_name = self.TOKENS.get(token, "UNKNOWN")

        if token_name == "UNKNOWN":
            line_number = self.get_line_number(token)
            self.errors.append(
                f"[line {line_number}] Error: Unexpected character: {token}"
            )
            return None, None

        if token == "=":
            if self.match_token("="):
                token_name = "EQUAL_EQUAL"
                token = "=="
        if token == "<":
            if self.match_token("="):
                token_name = "LESS_EQUAL"
                token = "<="
        if token == ">":
            if self.match_token("="):
                token_name = "GREATER_EQUAL"
                token = ">="
        if token == "!":
            if self.match_token("="):
                token_name = "BANG_EQUAL"
                token = "!="
        if token == "/":
            if self.match_token("/"):
                self.scan_comment()
                return None, None

        return token, token_name

    def scan_comment(self):
        """
        Ignore everything starting from //
        """
        while (not self.is_the_last_token()) and self.advance() != "\n":
            continue

    def get_line_number(self, token):
        return self.source_file.count("\n", 0, self.source_file.find(token)) + 1

    def is_the_last_token(self):
        return self.current >= len(self.source_file)

    def advance(self):
        self.current += 1
        return self.source_file[self.current - 1]

    def match_token(self, token):
        if not self.is_the_last_token() and self.source_file[self.current] != token:
            return False
        self.current += 1
        return True
