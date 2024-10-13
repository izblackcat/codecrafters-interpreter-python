import sys


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

    error = False


    i = 0
    while i < len(file_contents):

        c = file_contents[i];

        line_number = file_contents.count("\n", 0, file_contents.find(c)) + 1

        match (c):
            case '(':
                print("LEFT_PAREN ( null")
            case ')':
                print("RIGHT_PAREN ) null")
            case '{':
                print("LEFT_BRACE { null")
            case '}':
                print("RIGHT_BRACE } null")
            case '*':
                print("STAR * null")
            case '.':
                print("DOT . null")
            case ',':
                print("COMMA , null")
            case '+':
                print("PLUS + null")
            case '-':
                print("MINUS - null")
            case ';':
                print("SEMICOLON ; null")
            case '=':
                if i < len(file_contents) - 1 and file_contents[i + 1] == "=":
                    print("EQUAL_EQUAL == null")
                    i += 2
                    continue
                else:
                    print("EQUAL = null")
            case _:
                error = True
                print(f"[line {line_number}] Error: Unexpected character: {c}", file=sys.stderr)
        i += 1
    print("EOF  null")
    
    if error : 
        sys.exit(65)
    else:
        sys.exit(0)
    

if __name__ == "__main__":
    main()
