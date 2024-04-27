import json

class Interpreter:
    
    # Constructor
    def __init__(self, astList):
        self.astList = astList
        self.response = ''
        self.initials = ''
        with open('Accounts.JSON', 'r') as f:
            self.data = json.loads(f.read())
    
    def get_balance(self, account_id):
        self.data.get(account_id)
        if account_id not in self.data:
            self.response += f" attempted to access account {account_id} which does not exist"
            return None
        return self.data[account_id]
    
    def change_balance(self, account_id, new_balance):
        self.data[account_id] = new_balance
        
    def save_data(self):
        with open('Accounts.JSON', 'w') as f:
            json.dump(self.data, f)
    
    def find_highest_account_id(self, initials):
        highest_number = 0
        highest_account_id = None

        for account_id in self.data.keys():
            account_initials, number = account_id[:2], account_id[2:]
            number = int(number)  # Convert the number to an integer

            if account_initials == initials and number > highest_number:
                highest_number = number
                highest_account_id = account_id

        return highest_account_id
    
    def generate_account_id(self):
        highest_account_id = self.find_highest_account_id(self.initials)
        if highest_account_id is None:
            new_account_id = self.initials + '000001'
        else:
            new_number = int(highest_account_id[2:]) + 1
            new_account_id = self.initials + str(new_number).zfill(6)
        return new_account_id
        
    
    # Visit is called by the interpreter with a node as an argument
    def visit(self, node):
        # Get's the method name to call conditionally based on the node's type
        method_name = f'visit_{type(node).__name__}'
        # Get the method from the interpreter object
        visitor = getattr(self, method_name, self.no_visit_method)
        # Call the method with the node
        return visitor(node)
    
    def visit_NoneType(self, node):
        return
    
    def visit_TransactionNode(self, node):
        # Handle TransactionNode objects
        self.visit(node.nameNode)
        self.visit(node.operatorNode)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node):
        return node.value
    
    def visit_NameNode(self, node):
        self.response += f'Agent: {node.firstName.value} {node.lastName.value}'
        self.initials += f'{node.firstName.value[0]}{node.lastName.value[0]}'

    def visit_IDNode(self, node):
        return self.get_balance(node.account_id)

    def visit_OperatorNode(self, node):
        # Handling Creation of accounts. Supports naming the accound ID manually, or generating a new one.
        if node.operation == 'CREATE':
            if node.IDNode is not None and node.IDNode.account_id is not None:
                if node.IDNode.account_id in self.data:
                    self.response += f" attempted to create account {node.IDNode.account_id} which already exists"
                    return
                new_account_id = node.IDNode.account_id
                self.data[node.IDNode.account_id] = 0
            else:
                new_account_id = self.generate_account_id() # Generate a new account ID
                self.data[new_account_id] = 0
            self.response += f' created account {new_account_id}'
            return
        # Handling deletion of accounts with a DROP operation
        if node.operation == 'DROP':
            if node.IDNode.account_id not in self.data:
                self.response += f" attempted to delete account {node.IDNode.account_id} which does not exist"
                return
            else:
                del self.data[node.IDNode.account_id]
                self.response += f' deleted account {node.IDNode.account_id}'
                return
        # Handling viewing of accounts with a VIEW operation
        if node.operation == 'VIEW':
            if node.IDNode.account_id not in self.data:
                self.response += f" attempted to view account {node.IDNode.account_id} which does not exist"
                return
            else:
                balance = self.get_balance(node.IDNode.account_id)
                self.response += f' viewed account {node.IDNode.account_id}. Balance: {balance}'
                return
        current_balance = self.visit(node.IDNode)
        if current_balance is None:
        # Standard Command Operations
            return
        if node.operation == '+':
            new_balance = self.visit(node.IDNode) + self.visit(node.NumberNode)
            self.change_balance(node.IDNode.account_id, new_balance)
            self.response += f' deposited {node.NumberNode.value} into account {node.IDNode.account_id}. New balance: {new_balance}'
        elif node.operation == '-':
            new_balance = self.visit(node.IDNode) - self.visit(node.NumberNode)
            self.change_balance(node.IDNode.account_id, new_balance)
            self.response += f' withdrew {node.NumberNode.value} from account {node.IDNode.account_id}. New balance: {new_balance}'
        elif node.operation == '*':
            new_balance = round(self.visit(node.IDNode) * self.visit(node.NumberNode), 2)
            self.change_balance(node.IDNode.account_id, new_balance)
            self.response += f' applied {(node.NumberNode.value * 100) - 100}% interest to account {node.IDNode.account_id}. New balance: {new_balance}'
        else:
            raise Exception(f"Invalid operation: {node.operation}")
        
    def interpret(self):
        for ast in self.astList:
            self.response = ''
            self.initials = ''
            self.visit(ast)
            self.save_data()
            if self.response == '':
                print("ERROR: No response")
            else:
                print(self.response)
            
            