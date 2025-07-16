class Program:
    def __init__(self, statements):
        self.statements = statements

class VariableDeclaration:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Literal:
    def __init__(self, value):
        self.value = value

class Identifier:
    def __init__(self, name):
        self.name = name

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class ConsoleLog:
    def __init__(self, argument):
        self.argument = argument

class IfStatement:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Block:
    def __init__(self, statements):
        self.statements = statements

class FunctionDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnStatement:
    def __init__(self, expression):
        self.expression = expression

class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ArrayLiteral:
    def __init__(self, elements):
        self.elements = elements

class ObjectLiteral:
    def __init__(self, pairs):  # lista de (chave, valor)
        self.pairs = pairs

class MemberAccess:
    def __init__(self, object_, key, is_dot=False):
        self.object = object_
        self.key = key
        self.is_dot = is_dot  # true: obj.key / false: obj["key"]

class LambdaFunction:
    def __init__(self, params, expression):
        self.params = params
        self.expression = expression

class ForEachStatement:
    def __init__(self, var, iterable, body, kind='of'):
        self.var = var
        self.iterable = iterable
        self.body = body
        self.kind = kind

class Comment:
    def __init__(self, text):
        self.text = text

class ClassDeclaration:
    def __init__(self, name, constructor=None, methods=None):
        self.name = name
        self.constructor = constructor  # ConstructorDeclaration
        self.methods = methods or []    # lista de FunctionDeclaration

class ConstructorDeclaration:
    def __init__(self, params, body):
        self.params = params
        self.body = body

class MethodDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body