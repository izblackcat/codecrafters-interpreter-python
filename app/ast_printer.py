from expressions.Visitor import Visitor
from expressions.Binary import Binary
from expressions.Grouping import Grouping
from expressions.Unary import Unary
from expressions.Literal import Literal


class AstPrinter(Visitor):

    def visit_binary_expr(self, binary_expr):
        return self.parenthesize(
            binary_expr.operator, binary_expr.left, binary_expr.right
        )

    def visit_unary_expr(self, unary_expr):
        return self.parenthesize(unary_expr.operator, unary_expr.right)

    def visit_literal_expr(self, literal_expr):
        if not literal_expr.value:
            return "nil"
        return literal_expr.value

    def visit_grouping_expr(self, grouping_expr):
        return self.parenthesize("group", grouping_expr.expression)

    ## helper :
    def parenthesize(self, name, *exprs):
        result = "(" + name
        for expr in exprs:
            result = result + " "
            result = result + str(expr.accept(self))

        result += ")"
        return result

    def print_expr(self, expr):
        return expr.accept(self)


def main():
    # - 123 * (45.9 - 2)

    literal = Literal(123)
    left = Unary("-", literal)

    literal = Literal(45.9)
    right = Grouping(literal)
    expr = Binary(left, "*", right)

    res = AstPrinter().print_expr(expr)
    # (* (- 123) (group 45.9))
    print(res)

    expr = Binary(Unary("-", Literal(123)), "*", Binary(Literal(45.9), "-", Literal(2)))

    print(AstPrinter().print_expr(expr))


if __name__ == "__main__":
    main()
