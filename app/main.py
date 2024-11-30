import sys

sys.path.append("/home/izarkaoui/Documents/codecrafters-interpreter-python/")

from app.Scanner import Scanner


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    scanner = Scanner(file_contents)
    errors = scanner.scan_file()

    for error in errors:
        print(error, file=sys.stderr)

    if errors:
        sys.exit(65)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
