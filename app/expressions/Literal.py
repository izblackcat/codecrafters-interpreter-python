from expressions.Expr import Expr


class Literal(Expr):

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)
