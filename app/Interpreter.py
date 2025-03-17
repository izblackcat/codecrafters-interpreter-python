from app.expressions.Visitor import Visitor
from app.token_type import TokenType
from app.Error import Error

# from app.utils.value import StringValue, NumberValue, BooleanValue


class Interpreter(Visitor):

    def __init__(self):
        super().__init__()
        self.err = Error()

    def visit_literal_expr(self, literal):
        return literal.value

    def visit_grouping_expr(self, grouping):
        return self.evaluate(grouping.expression)

    def visit_binary_expr(self, binary):
        left = self.evaluate(binary.left)
        right = self.evaluate(binary.right)
        match binary.operator.token_type:
            case TokenType.MINUS.name:
                self.check_number_operands(binary.operator, left, right)
                return left - right
            case TokenType.SLASH.name:
                self.check_number_operands(binary.operator, left, right)
                return left / right

            case TokenType.STAR.name:
                self.check_number_operands(binary.operator, left, right)
                return left * right

            case TokenType.PLUS.name:
                # print(f"left ::: {left} and right ::: {isinstance(right, str)}")
                is_left_string = isinstance(left, str)
                is_right_string = isinstance(right, str)
                is_left_number = isinstance(left, (int, float)) and not isinstance(
                    left, bool
                )
                is_right_number = isinstance(right, (int, float)) and not isinstance(
                    right, bool
                )
                is_left_bool = isinstance(left, bool)
                is_right_bool = isinstance(right, bool)

                # String concatenation
                if is_left_string and is_right_string:
                    return left + right

                # Numeric addition
                if is_left_number and is_right_number:
                    return left + right

                # Boolean addition (if you want to support this)
                if is_left_bool and is_right_bool:
                    return left + right  # This will add them as 0s and 1s

                # Otherwise, it's a type error
                raise RuntimeException(
                    binary.operator, "Operands must be two number or strings."
                )

            case TokenType.GREATER.name:
                self.check_number_operands(binary.operator, left, right)
                return left > right

            case TokenType.GREATER_EQUAL.name:
                self.check_number_operands(binary.operator, left, right)
                return left >= right

            case TokenType.LESS.name:
                self.check_number_operands(binary.operator, left, right)
                return left < right

            case TokenType.LESS_EQUAL.name:
                self.check_number_operands(binary.operator, left, right)
                return left <= right

            case TokenType.BANG_EQUAL.name:
                return not self.is_equal(left, right)

            case TokenType.EQUAL_EQUAL.name:
                return self.is_equal(left, right)

    def visit_unary_expr(self, unary):
        right = self.evaluate(unary.right)
        match unary.operator.token_type:
            case TokenType.MINUS.name:
                self.check_number_operand(unary.operator, right)
                return -right
            case TokenType.BANG.name:
                return not self.is_truthy(right)

        return None

    def interpret(self, expr):
        try:
            value = self.evaluate(expr=expr)
            print(self.stringify(value))
        except RuntimeException as err:
            self.err.runtime_error(err=err)

    def stringify(self, object):
        if object is None:
            return "nil"
        elif isinstance(object, bool):
            return str(object).lower()
        elif isinstance(object, (int, float)):
            text = str(object)
            if text.endswith(".0"):
                text = text[0 : len(text) - 2]
            return text
        else:
            return str(object)

    def evaluate(self, expr):
        return expr.accept(self)

    def is_truthy(self, object):
        if object is None:
            return False
        elif object is False:
            return False
        elif object == "false":
            return False
        else:
            return True

    def is_equal(self, left, right):
        if left is None and right is None:
            return True
        elif left is None:
            return False
        else:
            return left == right

    def check_number_operand(self, operator, operand):
        if isinstance(operand, (float, int)):
            return
        raise RuntimeException(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeException(operator, "Operands must be numbers.")


class RuntimeException(RuntimeError):

    def __init__(self, token, message):
        self.message = message
        self.token = token
