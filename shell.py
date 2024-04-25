import Lexer
import Parser
import Nodes
import Token

while True:
    text = input("Enter a Token: ")
    result, error = Lexer.run('<stdin>', text)
    parser = Parser.Parser(result)
    ast = parser.parse()

    if error:
        print(error.as_string())
    else:
        print(ast)
