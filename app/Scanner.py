from .Token import Token


class Scanner:

    def __init__(self, source_file) -> None:
        self.source = source_file
        self.current = 0
        self.start = 0
        self.line = 1
        self.tokens = []
        self.errors = []

    def scan_file(self):
        while not self.is_the_last_token():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token("EOF", "", "null"))
        return self.tokens, self.errors

    def scan_token(self):
        # this is what iterates the source file:
        token = self.advance()

        match token:
            case "(":
                self.add_token("LEFT_PAREN")
            case ")":
                self.add_token("RIGHT_PAREN")
            case "{":
                self.add_token("LEFT_BRACE")
            case "}":
                self.add_token("RIGHT_BRACE")
            case ",":
                self.add_token("COMMA")
            case ".":
                self.add_token("DOT")
            case "-":
                self.add_token("MINUS")
            case "+":
                self.add_token("PLUS")
            case ";":
                self.add_token("SEMICOLON")
            case "*":
                self.add_token("STAR")
            case "!":
                self.add_token("BANG_EQUAL" if self.match_token("=") else "BANG")
            case "=":
                self.add_token("EQUAL_EQUAL" if self.match_token("=") else "EQUAL")
            case "<":
                self.add_token("LESS_EQUAL" if self.match_token("=") else "LESS")
            case ">":
                self.add_token("GREATER_EQUAL" if self.match_token("=") else "GREATER")
            case "/":
                if self.match_token("/"):
                    while self.look_a_head() != "\n" and not self.is_the_last_token():
                        self.advance()
                else:
                    self.add_token("SLASH")
            case " ":
                pass
            case "\t":
                pass
            case "\r":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.scan_string()
            case _:
                self.error(f"[line {self.line}] Error: Unexpected character: {token}")

    def scan_string(self):
        while self.look_a_head() != '"' and not self.is_the_last_token():
            self.advance()
            if self.look_a_head() == "\n":
                self.line += 1

        if self.is_the_last_token():
            self.error(f"[line {self.line}] Error: Unterminated string.")
            return

        self.advance()

        string = self.source[self.start + 1 : self.current - 1]
        self.add_token(token_type="STRING", literal=string)

    def add_token(self, token_type, literal="null"):
        lexeme = self.source[self.start : self.current]
        token = Token(token_type=token_type, lexeme=lexeme, literal=literal)
        self.tokens.append(token)

    def is_the_last_token(self):
        return self.current >= len(self.source)

    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    # peek
    def look_a_head(self):
        if self.is_the_last_token():
            return "\0"
        return self.source[self.current]

    def match_token(self, token):
        if self.is_the_last_token():
            return False
        if self.source[self.current] != token:
            return False
        self.current += 1
        return True

    def error(self, error_message):
        # [line 1] Error: Unexpected character: $
        self.errors.append(error_message)
