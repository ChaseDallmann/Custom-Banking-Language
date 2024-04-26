class Interpreter:
    # Visit is called by the interpreter with a node as an argument
    def visit(self, node):
        # Get's the method name to call conditionally based on the node's type
        method_name = f'visit_{type(node).__name__}'
        # Get the method from the interpreter object
        visitor = getattr(self, method_name, self.no_visit_method)
        # Call the method with the node
        return visitor(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node):
        return node.value

    def visit_OperatorNode(self, node):
        if node.operation == '+':
            return self.visit(node.node_a) + self.visit(node.node_b)
        elif node.operation == '-':
            return self.visit(node.node_a) - self.visit(node.node_b)
        elif node.operation == '*':
            return self.visit(node.node_a) * self.visit(node.node_b)
        else:
            raise Exception(f"Invalid operation: {node.operation}")
