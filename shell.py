import Lexer
import Parser
import Nodes
import Token
import account_manager

while True:
    option = input("Enter '1' to enter a command, '2' to read commands from a file:, 3: Account Manager ")
    if option == '1':
        text = input("Enter a Token: ")
        if not text.endswith('\n'):
            text += '\n'
    elif option == '2':
        with open('test.txt', 'r') as file:
            lines = file.readlines()
        text = ''.join(line.rstrip() + '\n' for line in lines)
        result, error = Lexer.run(text)
        parser = Parser.Parser(result)
        astList = parser.parse()
        if error:
            print(error.as_string())
        else:
            print(astList)
    elif option == '3':
        choice = input("Enter '1' to create an account, '2' view account list, '3' delete an account")
        manager = account_manager.AccountManager()
        if choice == '1':
            text = input("Please enter your First and Last name")
            result, error = Lexer.run(text)
            parser = Parser.Parser(result)
            account = parser.id()
            manager.addAccount(account)
        elif choice == '2':
            manager.loadAccounts()
        elif choice == '3':
            text = input("Please enter the account ID to delete: ")
            manager.dropAccount(text)