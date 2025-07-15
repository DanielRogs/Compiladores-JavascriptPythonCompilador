from ast_nodes.nodes import Literal, LambdaFunction, FunctionDeclaration


class Transpiler:
    def __init__(self, ast):
        self.ast = ast

    def transpile(self):
        return self.visit(self.ast)

    def indent(self, code, level=1):
        indent_str = '    ' * level  # 4 espaços por nível
        return '\n'.join(indent_str + line if line.strip() else line for line in code.split('\n'))

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method")

    def visit_Program(self, node):
        return "\n".join([self.visit(s) for s in node.statements])

    def visit_VariableDeclaration(self, node):
        if isinstance(node.value, LambdaFunction):
            return f"{node.name} = {self.visit(node.value)}"

        elif isinstance(node.value, FunctionDeclaration) and node.value.name is None:
            # Função anônima: define inline como função nomeada
            params = ', '.join(node.value.params)
            body = self.visit(node.value.body)
            return f"def {node.name}({params}):\n{self.indent(body)}"

        else:
            return f"{node.name} = {self.visit(node.value)}"


    def visit_Literal(self, node):
        if isinstance(node.value, str):
            return repr(node.value)  # usa aspas simples, escapando se necessário
        elif isinstance(node.value, bool):
            return "True" if node.value else "False"
        else:
            return str(node.value)

    def visit_Identifier(self, node):
        return node.name

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == '+':
            if self.is_string(node.left) and self.is_string(node.right):
                return f"{left} + {right}"
            elif self.is_string(node.left) or self.is_string(node.right):
                return f"str({left}) + str({right})"
        return f"{left} {node.op} {right}"


    def is_string(self, node):
        return isinstance(node, Literal) and isinstance(node.value, str)

    def visit_ConsoleLog(self, node):
        arg = self.visit(node.argument)
        return f"print({arg})"

    def visit_IfStatement(self, node):
        cond = self.visit(node.condition)
        then_block = self.visit(node.then_block)
        code = f"if {cond}:\n" + self._indent(then_block)
        if node.else_block:
            else_block = self.visit(node.else_block)
            code += f"\nelse:\n" + self._indent(else_block)
        return code

    def visit_WhileStatement(self, node):
        cond = self.visit(node.condition)
        body = self.visit(node.body)
        return f"while {cond}:\n" + self._indent(body)

    def visit_Block(self, node):
        return "\n".join([self.visit(s) for s in node.statements])

    def visit_FunctionDeclaration(self, node):
        params = ", ".join(node.params)
        body = self.visit(node.body)
        return f"def {node.name}({params}):\n" + self._indent(body)

    def visit_ReturnStatement(self, node):
        expr = self.visit(node.expression)
        return f"return {expr}"

    def visit_FunctionCall(self, node):
        args = ", ".join([self.visit(a) for a in node.arguments])
        return f"{node.name}({args})"

    def _indent(self, code, level=1):
        prefix = "    " * level
        return "\n".join(prefix + line for line in code.splitlines())
    
    def visit_ArrayLiteral(self, node):
        elements = [self.visit(e) for e in node.elements]
        return f"[{', '.join(elements)}]"

    def visit_ObjectLiteral(self, node):
        pairs = [f'"{k}": {self.visit(v)}' for k, v in node.pairs]
        return f"{{{', '.join(pairs)}}}"

    def visit_MemberAccess(self, node):
        obj = self.visit(node.object)
        if node.is_dot:
            key = self.visit(node.key)
            return f'{obj}[{key!r}]'
        else:
            index = self.visit(node.key)
            return f'{obj}[{index}]'

    def visit_LambdaFunction(self, node):
        params = ', '.join(node.params)
        return f"lambda {params}: {self.visit(node.expression)}"

    def visit_ForEachStatement(self, node):
        iterable_code = self.visit(node.iterable)

        if node.kind == 'in':
            loop = f"for {node.var} in {iterable_code}:"
        else:  # 'of'
            loop = f"for {node.var} in {iterable_code}:"

        body_lines = []
        for stmt in node.body.statements:
            body_lines.append("    " + self.visit(stmt))

        return loop + "\n" + "\n".join(body_lines)
