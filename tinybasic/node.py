class Node:
    def __init__(self, category, value=None, children=None):
        self.category = category  
        self.value = value        
        self.children = children if children else []  

    def __repr__(self):
        if self.children:
            return f'{self.category}({self.value}, {self.children})'
        return f'{self.category}({self.value})'

# Specific node types
class ProgramNode(Node):
    def __init__(self, statements):
        super().__init__('Program', children=statements)

class StatementNode(Node):
    def __init__(self, value, children=None):
        super().__init__('Statement', value, children)

class ComparisonNode(Node):
    def __init__(self, left_expr, operator, right_expr):
        super().__init__('Comparison', value=operator, children=[left_expr, right_expr])

class ExpressionNode(Node):
    def __init__(self, value, children=None):
        super().__init__('Expression', value, children)

class TermNode(Node):
    def __init__(self, value, children=None):
        super().__init__('Term', value, children)

class UnaryNode(Node):
    def __init__(self, operator, operand):
        super().__init__('Unary', value=operator, children=[operand])

class PrimaryNode(Node):
    def __init__(self, value):
        super().__init__('Primary', value=value)
        
class NumberNode(Node):
    def __init__(self, value):
        super().__init__('Number', value=value)
        
class IdentNode(Node):
    def __init__(self, value):
        super().__init__('Ident', value=value)

class NewLineNode(Node):
    def __init__(self, value):
        super().__init__('NewLine')
