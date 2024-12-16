import sys

from app.Scanner import Scanner


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
        tokenize(file_contents)
    elif command == "parse":
        parse()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


def tokenize(file):
    scanner = Scanner(file)
    tokens, errors = scanner.scan_file()

    for token in tokens:
        print(token)

    for error in errors:
        print(error, file=sys.stderr)

    if errors:
        sys.exit(65)
    else:
        sys.exit(0)


def parse():
    print("parse")


if __name__ == "__main__":
    main()
