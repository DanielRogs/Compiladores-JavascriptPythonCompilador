import re

TOKEN_SPEC = [
    ('COMMENT', r'//.*'),  # Ignorar comentários
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'(["\'])(?:\\.|[^\\])*?\1'),
    ('VAR', r'\bvar\b'),
    ('FUNCTION', r'\bfunction\b'),
    ('ARROW', r'=>'),
    ('FOR', r'for'),
    ('IN', r'in'),
    ('OF', r'of'),
    ('RETURN', r'\breturn\b'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'),
    ('CONSOLE', r'console'),
    ('LOG', r'log'),
    ('TRUE', r'\btrue\b'),
    ('FALSE', r'\bfalse\b'),
    ('IDENTIFIER', r'[a-zA-Z_\u00C0-\u017F][a-zA-Z0-9_\u00C0-\u017F]*'),  # Suporte a acentos
    ('OP_INCREMENT', r'\+\+'),
    ('OP_DECREMENT', r'--'),
    ('OP_PLUSEQ', r'\+='),
    ('OP_MINUSEQ', r'-='),
    ('EQ_STRICT', r'==='),
    ('NEQ_STRICT', r'!=='),
    ('EQ', r'=='),
    ('NEQ', r'!='),
    ('OP_ASSIGN', r'='),
    ('OP_PLUS', r'\+'),
    ('OP_MINUS', r'-'),
    ('OP_MUL', r'\*'),
    ('OP_DIV', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('GTE', r'>='),
    ('LTE', r'<='),
    ('GT', r'>'),
    ('LT', r'<'),
    ('COLON', r':'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('DOT', r'\.'),
    ('WHITESPACE', r'\s+'),
]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_name, token_regex in TOKEN_SPEC:
            pattern = re.compile(token_regex)
            match = pattern.match(code, pos)
            if match:
                if token_name not in ['WHITESPACE']:  # Agora vamos capturar comentários
                    tokens.append(Token(token_name, match.group(0)))
                pos = match.end(0)
                break
        if not match:
            raise SyntaxError(f"Caractere desconhecido em posição {pos}")
    return tokens
