'''
Chase Dallmann & John Petrie
4/28/2024
Shell
We pledge that all the code we have written is our own code and not copied from any other source 4/28/24
'''

import Lexer
import Parser
import Interpreter

#The menu that will determine how the input is read
while True:
    option = input("Enter '1' to enter a command, '2' to read commands from a file: ")
    if option == '1': #Getting the input from a manual entry in the console
        text = input("Enter a Token: ")
        if not text.endswith('\n'):
            text += '\n'
    elif option == '2': #Getting the input from bankinginput.txt to read from
        with open('bankinginput.txt', 'r') as file:
            lines = file.readlines()
        text = ''.join(line.rstrip() + '\n' for line in lines)
    else:
        continue
    result, error = Lexer.run(text) #Getting tokens from the Lexer
    if not result == '':
        parser = Parser.Parser(result) #Creating the parser and passing through the tokens
        astList = parser.parse() #Generating the AST from the paser
        Interpreter.Interpreter(astList).interpret() #Banking logic that takes the AST and preforms operations
