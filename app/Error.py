import sys

from app.token_type import TokenType


class Error:

    hadError = False

    def __init__(self):
        pass

    def error(self, line, token=None, message=None):
        if line:
            self.report(line=line, where="", message=message)

        if token:
            if token.token_type == TokenType.EOF:
                self.report(token.line, " at end", message)
            else:
                self.report(token.line, f" at '{token.lexeme}'", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Error.hadError = True
