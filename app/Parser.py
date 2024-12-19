from expressions.Binary import Binary
from expressions.Grouping import Grouping
from expressions.Unary import Unary
from expressions.Literal import Literal


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        return self.equality()

    def equality(self):
        """
        Corresponds to the grammar rule :
            equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        """

        expr = self.comparison()

        while self.match("BANG_EQUAL", "EQUAL_EQUAL"):
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

        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
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

        while self.match("MINUS", "PLUS"):
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

        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        """
        Corresponds to the grammar rule :
            unary          → ( "!" | "-" ) unary | primary ;
        """
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        """
        Corresponds to the grammar rule :
            primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
        """

        if self.match("TRUE"):
            return Literal(True)
        elif self.match("FALSE"):
            return Literal(False)
        elif self.match("NIL"):
            return Literal(None)
        elif self.match("NUMBER", "STRING"):
            # TODO: this may need to be fixed later!
            return Literal(self.previous().literal)
        elif self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after expression")
            return Grouping(expr)
        raise self.error(self.peek(), "Expect expression")

    def error(self, token, message):
        # raise RuntimeError()
        # TODO: this needs to be reviewed. Where should we put these errors ?
        return Parser.ParseError()

    # ________________________helpers:___________________________

    def match(self, **types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek() == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
            return self.previous()

    def is_at_end(self):
        return self.peek().token_type == "EOF"

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self):
        return self.tokens[self.current]

    class ParseError(RuntimeError): ...
