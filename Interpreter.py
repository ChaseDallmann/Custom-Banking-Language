'''
Chase Dallmann & John Petrie
4/28/2024
Interpreter
We pledge that all the code we have written is our own code and not copied from any other source 4/28/24
'''

import json


class Interpreter:

    # Constructor
    def __init__(self, astList):
        self.astList = astList # List of ASTs to be interpreted
        self.response = '' # Response string to be built and printed
        self.initials = '' # Initials of the user, for generating accounts
        if astList[0].nameNode.firstName.value == 'TEST' and astList[0].nameNode.lastName.value == 'MODE': # If the first AST contains the name TEST MODE, it will enter testing mode
            self.testing = True
            self.test_list = [ # List of expected responses for testing mode
                "Agent: TEST MODE created account TM000003",
                "Agent: TEST MODE deposited 234 into account TM000003. New balance: 234",
                "Agent: TEST MODE applied 100% interest to account TM000003. New balance: 468",
                "Agent: TEST MODE withdrew 168 from account TM000003. New balance: 300",
                "Agent: TEST MODE deleted account TM000001",
                "Agent: TEST MODE attempted to access account TM123456 which does not exist",
                "Agent: TEST MODE attempted to withdraw 1000 from account TM000002. Insufficient funds. Balance: 100.",
                "Agent: TEST MODE created account TM908652",
                "Agent: TEST MODE deposited 7347 into account TM908652. New balance: 7347"
            ]
            with open('Testing.JSON', 'r') as f: # If in testing mode, it will read the data from the Testing.JSON file
                self.data = json.loads(f.read())
        else:
            self.testing = False
            with open('Accounts.JSON', 'r') as f: # If not in testing mode, it will read the data from the Accounts.JSON file
                self.data = json.loads(f.read())

    def get_balance(self, account_id): # Function to get the balance of an account
        self.data.get(account_id)
        if account_id not in self.data:
            self.response += f" attempted to access account {
                account_id} which does not exist"
            return None
        return self.data[account_id]

    def change_balance(self, account_id, new_balance): # Function to change the balance of an account
        self.data[account_id] = new_balance

    def save_data(self): # Function to save the updated data to the JSON file
        with open('Accounts.JSON', 'w') as f:
            json.dump(self.data, f)

    # Generates a new account ID at the lowest possible number for the initials
    def generate_account_id(self):
        new_account_id = self.initials + '000001'

        while new_account_id in self.data:  # This is a linear brute force search for the next available account ID
            # Complexity O(n) where n is the number of accounts However, the number of accounts is expected to be low
            new_number = int(new_account_id[2:]) + 1
            # zfill pads the number with zeros to ensure it is 6 digits long
            new_account_id = self.initials + str(new_number).zfill(6)

        return new_account_id # Returns the new account ID

    # Visit is called by the interpreter with a node as an argument

    def visit(self, node):
        # Get's the method name to call conditionally based on the node's type
        method_name = f'visit_{type(node).__name__}'
        # Get the method from the interpreter object
        visitor = getattr(self, method_name, self.no_visit_method)
        # Call the method with the node, will visit nodes recursively
        return visitor(node)

    # If the node is a NoneType, return nothing and move on
    def visit_NoneType(self, node):
        return

    # If the node is a TransactionNode, visit the nameNode and operatorNode
    def visit_TransactionNode(self, node):
        # Handle TransactionNode objects
        self.visit(node.nameNode)
        self.visit(node.operatorNode)

    # If the node doesn't have a visit method, raise an exception
    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    # If the node is a NumberNode, return the value
    def visit_NumberNode(self, node):
        return node.value

    # If the node is a NameNode, set the Agent name and initials
    def visit_NameNode(self, node):
        self.response += f'Agent: {node.firstName.value} {node.lastName.value}'
        self.initials += f'{node.firstName.value[0]}{node.lastName.value[0]}'

    # If the node is an IDNode, return the balance of the account
    def visit_IDNode(self, node):
        return self.get_balance(node.account_id)

    # If the node is an OperatorNode, handle the operation
    def visit_OperatorNode(self, node):
        # Handling Creation of accounts. Supports naming the accound ID manually, or generating a new one.
        if node.operation == 'CREATE':
            if node.IDNode is not None and node.IDNode.account_id is not None:  # Check if the account ID is specified
                if node.IDNode.account_id in self.data:  # Check if the account ID already exists
                    self.response += f" attempted to create account {
                        node.IDNode.account_id} which already exists"
                    return
                new_account_id = node.IDNode.account_id  # Use the specified account ID
                # Create the account with a balance of 0
                self.data[node.IDNode.account_id] = 0
            else:
                new_account_id = self.generate_account_id()  # Generate a new account ID
                self.data[new_account_id] = 0
            # Respond with the new account ID
            self.response += f' created account {new_account_id}'
            return
        # Handling deletion of accounts with a DROP operation
        if node.operation == 'DROP':
            if node.IDNode.account_id not in self.data:
                self.response += f" attempted to delete account {
                    node.IDNode.account_id} which does not exist"
                return
            else:
                del self.data[node.IDNode.account_id]
                self.response += f' deleted account {node.IDNode.account_id}'
                return
        # Handling viewing of accounts with a VIEW operation
        if node.operation == 'VIEW':
            if node.IDNode.account_id not in self.data:
                self.response += f" attempted to view account {
                    node.IDNode.account_id} which does not exist"
                return
            else:
                balance = self.get_balance(node.IDNode.account_id)
                self.response += f' viewed account {
                    node.IDNode.account_id}. Balance: {balance}'
                return
        current_balance = self.visit(node.IDNode)
        if current_balance is None:
            return
        # Handling depositing standard operations
        # Handling deposits
        if node.operation == '+':
            new_balance = self.visit(node.IDNode) + self.visit(node.NumberNode) # visit the IDNode and NumberNode to get the values and add them
            self.change_balance(node.IDNode.account_id, new_balance)
            # Append the new balance and corresponding message to the response
            self.response += f' deposited {node.NumberNode.value} into account {
                node.IDNode.account_id}. New balance: {new_balance}'
        # Handling withdrawals
        elif node.operation == '-':
            new_balance = self.visit(node.IDNode) - self.visit(node.NumberNode) # visit the IDNode and NumberNode to get the values and subtract them
            if new_balance < 0:
                # Append the insufficient funds message to the response
                self.response += f' attempted to withdraw {node.NumberNode.value} from account {
                    node.IDNode.account_id}. Insufficient funds. Balance: {self.visit(node.IDNode)}.'
                return
            # if not insufficient funds, append the new balance to the response and update the balance
            self.change_balance(node.IDNode.account_id, new_balance)
            self.response += f' withdrew {node.NumberNode.value} from account {
                node.IDNode.account_id}. New balance: {new_balance}'
        # Handling interest
        elif node.operation == '*':
            new_balance = round(self.visit(node.IDNode) * # visit the IDNode and NumberNode to get the values and multiply them
                                self.visit(node.NumberNode), 2)
            self.change_balance(node.IDNode.account_id, new_balance)
            # Multiply the interest by 100 to get the percentage and append to response
            self.response += f' applied {(node.NumberNode.value * 100) - 100}% interest to account { 
                node.IDNode.account_id}. New balance: {new_balance}' 
        else:
            raise Exception(f"Invalid operation: {node.operation}")

    def interpret(self):
        iteration = 0
        for ast in self.astList:
            self.response = ''
            self.initials = ''
            self.visit(ast)
            if self.testing == False: # Base case if not in testing mode, saves the results to the JSON file
                self.save_data()
            if self.response == '':
                print("ERROR: No response")
            if not self.testing: # Base case if not in testing mode, prints the response for each AST
                print(self.response)
            elif self.testing: # Testing mode, compares the response to the expected response
                print(f'GENERATED: {self.response}')
                print(f'EXPECTED: {self.test_list[iteration]}')
                if self.response == self.test_list[iteration]:
                    print("TEST PASSED")
                else:
                    print("TEST FAILED")
            iteration += 1
        if self.testing == True:
            print(f'GENERATED DATA: {self.data}')
            print("EXPECTED DATA: {'TM000002': 100, 'TM000003': 300, 'TM908652': 7347}")
