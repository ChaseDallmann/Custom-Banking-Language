import json

class Interpreter:
    
    # Constructor
    def __init__(self, astList):
        self.astList = astList
        with open('Accounts.JSON', 'r') as f:
            self.data = json.loads(f.read())
    
    def get_balance(self, account_id):
        self.data.get(account_id)
        if account_id not in self.data:
            raise Exception(f"Account {account_id} not found")
        return self.data[account_id]
    
    def change_balance(self, account_id, new_balance):
        self.data[account_id] = new_balance
        
    def save_data(self):
        with open('Accounts.JSON', 'w') as f:
            json.dump(self.data, f)
    
    # Visit is called by the interpreter with a node as an argument
    def visit(self, node):
        # Get's the method name to call conditionally based on the node's type
        method_name = f'visit_{type(node).__name__}'
        # Get the method from the interpreter object
        visitor = getattr(self, method_name, self.no_visit_method)
        # Call the method with the node
        return visitor(node)
    
    def visit_TransactionNode(self, node):
        # Handle TransactionNode objects
        self.visit(node.nameNode)
        self.visit(node.operatorNode)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node):
        return node.value
    
    def visit_NameNode(self, node):
        return f'{node.firstName.value} {node.lastName.value}'

    def visit_IDNode(self, node):
        return self.get_balance(node.account_id)

    def visit_OperatorNode(self, node):
        if node.operation == '+':
            new_balance = self.visit(node.IDNode) + self.visit(node.NumberNode)
            self.change_balance(node.IDNode.account_id, new_balance)
            return new_balance
        elif node.operation == '-':
            new_balance = self.visit(node.IDNode) - self.visit(node.NumberNode)
            self.change_balance(node.IDNode.account_id, new_balance)
            return new_balance
        elif node.operation == '*':
            new_balance = self.visit(node.IDNode) * self.visit(node.NumberNode)
            self.change_balance(node.IDNode.account_id, new_balance)
            return new_balance
        else:
            raise Exception(f"Invalid operation: {node.operation}")
        
    def interpret(self):
        for ast in self.astList:
            self.visit(ast)
            self.save_data()
            
            