import Lexer

while True:
    text = input("Enter a Token: ")
    result, error = Lexer.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)
