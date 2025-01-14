from app.expressions.Binary import Binary
from app.expressions.Grouping import Grouping
from app.expressions.Unary import Unary
from app.expressions.Literal import Literal
from app.token_type import TokenType
from app.Error import Error


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.err = Error()

    def parse(self):
        try:
            return self.expression()
        except Parser.ParseError:
            return None

    def expression(self):
        return self.equality()

    def equality(self):
        """
        Corresponds to the grammar rule :
            equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        """
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        """
        Corresponds to the grammar rule :
            comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        """
        expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        """
        Corresponds to the grammar rule :
            term           → factor ( ( "-" | "+" ) factor )* ;
        """
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        """
        Corresponds to the grammar rule :
            factor         → unary ( ( "/" | "*" ) unary )* ;
        """
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        """
        Corresponds to the grammar rule :
            unary          → ( "!" | "-" ) unary | primary ;
        """
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        """
        Corresponds to the grammar rule :
            primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
        """
        if self.match(TokenType.TRUE):
            return Literal("true")
        elif self.match(TokenType.FALSE):
            return Literal("false")
        elif self.match(TokenType.NIL):
            return Literal("nil")
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)
        raise self.error(self.peek(), "Expect expression")

    def error(self, token, message):
        self.err.error(line=None, token=token, message=message)
        return Parser.ParseError()

    def consume(self, type, message):
        if self.check(type.name):
            return self.advance()
        raise self.error(self.peek(), message)

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            match self.peek().type:
                case TokenType.CLASS:
                    pass
                case TokenType.FUN:
                    pass
                case TokenType.VAR:
                    pass
                case TokenType.FOR:
                    pass
                case TokenType.IF:
                    pass
                case TokenType.WHILE:
                    pass
                case TokenType.PRINT:
                    pass
                case TokenType.RETURN:
                    return

            self.advance()

    # ________________________helpers:___________________________

    def match(self, *types):
        for t in types:
            if self.check(t.name):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().token_type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
            return self.previous()

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self):
        return self.tokens[self.current]

    class ParseError(Exception):
        pass
