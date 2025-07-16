from lexer.tokenizer import tokenize
from ast_nodes.nodes import (
    Program, VariableDeclaration, Literal, Identifier,
    BinaryOp, ConsoleLog, IfStatement, WhileStatement,
    Block, FunctionDeclaration, ReturnStatement, FunctionCall, 
    ArrayLiteral, ObjectLiteral, MemberAccess, LambdaFunction,
    ForEachStatement, Comment, ClassDeclaration, ConstructorDeclaration,
    MethodDeclaration
)

class Parser:
    def __init__(self, code):
        self.tokens = tokenize(code)
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token and token.type == token_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Esperado {token_type}, encontrado {token}")

    def parse_program(self):
        statements = []
        while self.current_token() is not None:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()
        if token.type == 'COMMENT':
            return self.parse_comment()
        elif token.type == 'CLASS':
            return self.parse_class_declaration()
        elif token.type == 'VAR':
            return self.parse_variable_declaration()
        elif token.type == 'CONSOLE':
            return self.parse_console_log()
        elif token.type == 'IF':
            return self.parse_if_statement()
        elif token.type == 'WHILE':
            return self.parse_while_statement()
        elif token.type == 'FUNCTION':
            return self.parse_function_declaration()
        elif token.type == 'RETURN':
            return self.parse_return_statement()
        elif token.type == 'IDENTIFIER':
            # Pode ser chamada de função ou atribuição simples
            # Vamos tentar chamar função primeiro
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token.type == 'LPAREN':
                return self.parse_function_call_statement()
            else:
                return self.parse_assignment()
        elif token.type == 'FOR':
            return self.parse_for_each()
        else:
            raise SyntaxError(f"Token inesperado: {token}")

    def parse_comment(self):
        token = self.eat('COMMENT')
        # Remove o "//" do início do comentário
        comment_text = token.value[2:].strip()
        return Comment(comment_text)

    def parse_variable_declaration(self):
            self.eat('VAR')
            ident = self.eat('IDENTIFIER')
            self.eat('OP_ASSIGN')

            # Tenta arrow function
            if self.current_token().type == 'LPAREN':
                lookahead_pos = self.pos
                try:
                    # faz lookahead de parênteses até o RPAREN
                    self.eat('LPAREN')
                    while self.current_token().type != 'RPAREN':
                        self.eat(self.current_token().type)
                    self.eat('RPAREN')

                    # se vier ARROW, voltamos e chamamos o parser da arrow
                    if self.current_token().type == 'ARROW':
                        self.pos = lookahead_pos
                        func = self.parse_arrow_function()
                        # **consome o ; se houver**
                        if self.current_token() and self.current_token().type == 'SEMICOLON':
                            self.eat('SEMICOLON')
                        return VariableDeclaration(ident.value, func)
                    else:
                        self.pos = lookahead_pos
                except:
                    self.pos = lookahead_pos

            # Caso normal (não-arrow) ou arrow sem bloco
            value = self.parse_expression()
            self.eat('SEMICOLON')
            return VariableDeclaration(ident.value, value)

    def parse_assignment(self):
        ident = self.eat('IDENTIFIER')
        token = self.current_token()

        if token.type == 'OP_ASSIGN':
            self.eat('OP_ASSIGN')
            value = self.parse_expression()
            self.eat('SEMICOLON')
            return VariableDeclaration(ident.value, value)

        elif token.type in ('OP_PLUSEQ', 'OP_MINUSEQ'):
            op_token = self.eat(token.type)
            value = self.parse_expression()
            self.eat('SEMICOLON')
            op = op_token.value[0]  # pega "+" ou "-"
            expr = BinaryOp(Identifier(ident.value), op, value)
            return VariableDeclaration(ident.value, expr)

        elif token.type == 'OP_INCREMENT':
            self.eat('OP_INCREMENT')
            self.eat('SEMICOLON')
            expr = BinaryOp(Identifier(ident.value), '+', Literal(1))
            return VariableDeclaration(ident.value, expr)

        elif token.type == 'OP_DECREMENT':
            self.eat('OP_DECREMENT')
            self.eat('SEMICOLON')
            expr = BinaryOp(Identifier(ident.value), '-', Literal(1))
            return VariableDeclaration(ident.value, expr)

        else:
            raise SyntaxError(f"Operação não suportada: {token}")


    def parse_console_log(self):
        self.eat('CONSOLE')
        self.eat('DOT')
        self.eat('LOG')
        self.eat('LPAREN')
        arg = self.parse_expression()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        return ConsoleLog(arg)

    def parse_if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        then_block = self.parse_block()
        else_block = None
        if self.current_token() and self.current_token().type == 'ELSE':
            self.eat('ELSE')
            else_block = self.parse_block()
        return IfStatement(condition, then_block, else_block)

    def parse_while_statement(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_block(self):
        self.eat('LBRACE')
        statements = []
        while self.current_token() and self.current_token().type != 'RBRACE':
            statements.append(self.parse_statement())
        self.eat('RBRACE')
        return Block(statements)

    def parse_function_declaration(self):
        self.eat('FUNCTION')
        name = self.eat('IDENTIFIER').value
        self.eat('LPAREN')
        params = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            params.append(self.eat('IDENTIFIER').value)
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENTIFIER').value)
        self.eat('RPAREN')
        body = self.parse_block()
        return FunctionDeclaration(name, params, body)

    def parse_return_statement(self):
        self.eat('RETURN')
        expr = self.parse_expression()
        self.eat('SEMICOLON')
        return ReturnStatement(expr)

    def parse_array(self):
        self.eat('LBRACKET')
        elements = []
        if self.current_token().type != 'RBRACKET':
            elements.append(self.parse_expression())
            while self.current_token().type == 'COMMA':
                self.eat('COMMA')
                elements.append(self.parse_expression())
        self.eat('RBRACKET')
        return ArrayLiteral(elements)
    
    def parse_object(self):
        self.eat('LBRACE')
        pairs = []
        if self.current_token().type != 'RBRACE':
            while True:
                key_token = self.eat('IDENTIFIER')
                self.eat('COLON')
                value = self.parse_expression()
                pairs.append((key_token.value, value))
                if self.current_token().type == 'COMMA':
                    self.eat('COMMA')
                else:
                    break
        self.eat('RBRACE')
        return ObjectLiteral(pairs)


    def parse_function_call_statement(self):
        call = self.parse_function_call()
        self.eat('SEMICOLON')
        return call

    def parse_function_call(self):
        name = self.eat('IDENTIFIER').value
        self.eat('LPAREN')
        args = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            args.append(self.parse_expression())
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                args.append(self.parse_expression())
        self.eat('RPAREN')
        return FunctionCall(name, args)

    def parse_expression(self):
      # Suporte para operadores relacionais
      node = self.parse_add_sub()

      while self.current_token() and self.current_token().type in ('GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ', 'EQ_STRICT', 'NEQ_STRICT'):
          op_token = self.eat(self.current_token().type)
          right = self.parse_add_sub()
          node = BinaryOp(node, op_token.value, right)

      return node

    def parse_add_sub(self):
        node = self.parse_mul_div()
        while self.current_token() and self.current_token().type in ('OP_PLUS', 'OP_MINUS'):
            op = self.eat(self.current_token().type).value
            right = self.parse_mul_div()
            node = BinaryOp(node, op, right)
        return node

    def parse_mul_div(self):
        node = self.parse_primary()
        while self.current_token() and self.current_token().type in ('OP_MUL', 'OP_DIV'):
            op = self.eat(self.current_token().type).value
            right = self.parse_primary()
            node = BinaryOp(node, op, right)
        return node

    def parse_arrow_function(self):
        self.eat('LPAREN')
        params = []
        if self.current_token().type != 'RPAREN':
            params.append(self.eat('IDENTIFIER').value)
            while self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENTIFIER').value)
        self.eat('RPAREN')
        self.eat('ARROW')

        if self.current_token().type == 'LBRACE':
            # Arrow function com bloco: vira função normal
            body = self.parse_block()
            return FunctionDeclaration(None, params, body)
        else:
            expr = self.parse_expression()
            return LambdaFunction(params, expr)

    def parse_for_each(self):
        self.eat('FOR')
        self.eat('LPAREN')

        # Ex: var x in arr  ou  var x of arr
        if self.current_token().type == 'VAR':
            self.eat('VAR')
        var_name = self.eat('IDENTIFIER').value

        kind_token = self.current_token()
        if kind_token.type == 'IN':
            self.eat('IN')
            kind = 'in'
        elif kind_token.type == 'OF':
            self.eat('OF')
            kind = 'of'
        else:
            raise SyntaxError(f"Esperado 'in' ou 'of', encontrado: {kind_token}")

        iterable = self.parse_expression()
        self.eat('RPAREN')

        body = self.parse_block()
        return ForEachStatement(var_name, iterable, body, kind)

    def parse_primary(self):
        token = self.current_token()
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            value = float(token.value) if '.' in token.value else int(token.value)
            return Literal(value)
        elif token.type == 'STRING':
            self.eat('STRING')
            # Remove as aspas externas apenas — não adiciona novas
            return Literal(token.value[1:-1])  # remove a primeira e última aspas
        elif token.type == 'TRUE':
            self.eat('TRUE')
            return Literal(True)
        elif token.type == 'FALSE':
            self.eat('FALSE')
            return Literal(False)
        elif token.type == 'IDENTIFIER':
            node = Identifier(token.value)
            self.eat('IDENTIFIER')

            # Tratamento de acessos: obj.prop ou arr[0]
            while self.current_token() and self.current_token().type in ('DOT', 'LBRACKET'):
                if self.current_token().type == 'DOT':
                    self.eat('DOT')
                    key = self.eat('IDENTIFIER').value
                    node = MemberAccess(node, Literal(key), is_dot=True)
                elif self.current_token().type == 'LBRACKET':
                    self.eat('LBRACKET')
                    index = self.parse_expression()
                    self.eat('RBRACKET')
                    node = MemberAccess(node, index)
            return node
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()
            self.eat('RPAREN')
            return node
        elif token.type == 'LBRACKET':
            return self.parse_array()
        elif token.type == 'LBRACE':
            return self.parse_object()
        else:
            raise SyntaxError(f"Token inesperado em expressão: {token}")

    def parse_class_declaration(self):
        self.eat('CLASS')
        class_name = self.eat('IDENTIFIER').value
        self.eat('LBRACE')
        
        constructor = None
        methods = []
        
        while self.current_token() and self.current_token().type != 'RBRACE':
            token = self.current_token()
            
            if token.type == 'CONSTRUCTOR':
                constructor = self.parse_constructor()
            elif token.type == 'IDENTIFIER':
                # Método da classe
                method = self.parse_method()
                methods.append(method)
            elif token.type == 'COMMENT':
                # Ignorar comentários dentro da classe por enquanto
                self.eat('COMMENT')
            else:
                raise SyntaxError(f"Token inesperado dentro da classe: {token}")
        
        self.eat('RBRACE')
        return ClassDeclaration(class_name, constructor, methods)
    
    def parse_constructor(self):
        self.eat('CONSTRUCTOR')
        self.eat('LPAREN')
        
        params = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            params.append(self.eat('IDENTIFIER').value)
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENTIFIER').value)
        
        self.eat('RPAREN')
        body = self.parse_block()
        
        return ConstructorDeclaration(params, body)
    
    def parse_method(self):
        method_name = self.eat('IDENTIFIER').value
        self.eat('LPAREN')
        
        params = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            params.append(self.eat('IDENTIFIER').value)
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENTIFIER').value)
        
        self.eat('RPAREN')
        body = self.parse_block()
        
        return MethodDeclaration(method_name, params, body)
