import sys

from app.token_type import TokenType


class Error:

    hadError = False
    hadRuntimeError = False

    def __init__(self):
        pass

    def runtime_error(self, err):
        print(f"{err.message} \n[line {err.token.line}]", file=sys.stderr)
        Error.hadRuntimeError = True

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
