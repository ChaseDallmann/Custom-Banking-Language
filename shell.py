'''
Chase Dallmann & John Petrie
4/28/2024
Shell
We pledge that all the code we have written is our own code and not copied from any other source 4/28/24
'''

import Lexer
import Parser
import Interpreter
import os

#The menu that will determine how the input is read
while True:
    option = input("Enter '1' to enter a command, '2' to read commands from a file: ")
    if option == '1': #Getting the input from a manual entry in the console
        text = input("Enter a Token: ")
        if not text.endswith('\n'):
            text += '\n'
        if text.lower() == 'exit\n':
            print('Exit entry found: Closing Banking Program')
            os._exit(0)
        if text.lower() == 'test\n':
            text = ('TEST MODE CREATE\nTEST MODE TM000003 + 234\nTEST MODE TM000003 * 2\n'
                    'TEST MODE TM000003 - 168\nTEST MODE TM000001 DROP\nTEST MODE TM123456 + 100000\n'
                    'TEST MODE TM000002 withdraw 1000\nTEST MODE TM908652 CREATE\nTEST MODE TM908652 + 7347\n')
    elif option == '2': #Getting the input from bankinginput.txt to read from
        with open('bankinginput.txt', 'r') as file:
            lines = file.readlines()
        text = ''.join(line.rstrip() + '\n' for line in lines)
    else:
        print('Invalid option, please enter 1 or 2')
        continue
    result, error = Lexer.run(text) # Generating tokens from the Lexer based on the passed string
    if not result == '':
        parser = Parser.Parser(result) # Creating the parser and passing through the tokens
        astList = parser.parse() # Generating the AST from the paser
        Interpreter.Interpreter(astList).interpret() # Banking logic that takes the list of ASTs and preforms operations

