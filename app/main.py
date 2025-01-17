import sys

from app.Scanner import Scanner
from app.Parser import Parser
from app.ast_printer import AstPrinter
from app.Error import Error
from app.Interpreter import Interpreter


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    with open(filename) as file:
        file_contents = file.read()

    if command == "tokenize":
        tokens = tokenize(file_contents)
        for token in tokens:
            print(token)

        if Error.hadError:
            # print(65)
            sys.exit(65)

    elif command == "parse":
        tokens = tokenize(file_contents)
        expr = parse(tokens)
        print(AstPrinter().print_expr(expr=expr))

    elif command == "evaluate":
        tokens = tokenize(file_contents)
        expr = parse(tokens=tokens)
        evaluate(expr=expr)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


def tokenize(file):
    scanner = Scanner(file)
    tokens = scanner.scan_file()

    return tokens


def parse(tokens):

    parser = Parser(tokens)

    expr = parser.parse()

    if Error.hadError:
        sys.exit(65)

    return expr


def evaluate(expr):

    interpreter = Interpreter()

    interpreter.interpret(expr=expr)

    if Error.hadError:
        sys.exit(65)


if __name__ == "__main__":
    main()
