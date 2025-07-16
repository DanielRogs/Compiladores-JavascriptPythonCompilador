from parser.parser import Parser
from translator.transpiler import Transpiler
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_entrada.js>")
        return

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        code = f.read()

    try:
        parser = Parser(code)
        ast = parser.parse_program()

        transpiler = Transpiler(ast)
        python_code = transpiler.transpile()

        print("# Código Python gerado:\n")
        print(python_code)

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
