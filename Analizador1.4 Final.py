import re
from lark import Lark, UnexpectedInput
from lark.tree import pydot__tree_to_png

# -------------------- Definición de Tokens --------------------
TOKENS = {
    'PALABRA_RESERVADA': r'\b(if|else|for|print|int|b|f|h|j|k)\b',
    'IDENTIFICADOR': r'\b[a-zA-Z][a-zA-Z0-9]{0,14}\b',
    'CONSTANTE_ENTERA': r'\b(100|[0-9]{1,2})\b',
    'OPERADOR_ARITMETICO': r'[+\-*/]',
    'OPERADOR_ASIGNACION': r'\:=',
    'OPERADOR_RELACIONAL': r'>=|<=|<>|>|<|=',
    'SIMBOLO': r'[{}\[\]();.,]',
    'CADENA': r'\"[bfhjk]*\"',
}

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS.items())

# -------------------- Analizador Léxico --------------------
def analizador_lexico(codigo_fuente):
    tokens_encontrados = []
    tabla_simbolos = {}
    errores_lexicos = []

    identificador_id = 1
    constante_id = 1

    pos = 0
    while pos < len(codigo_fuente):
        match = re.match(token_regex, codigo_fuente[pos:])
        if match:
            tipo_token = match.lastgroup
            valor_token = match.group(tipo_token)
            tokens_encontrados.append((tipo_token, valor_token))

            if tipo_token == "IDENTIFICADOR":
                if valor_token not in tabla_simbolos:
                    tabla_simbolos[valor_token] = {"ID": identificador_id, "Tipo": "Identificador"}
                    identificador_id += 1
            elif tipo_token == "CONSTANTE_ENTERA":
                if valor_token not in tabla_simbolos:
                    tabla_simbolos[valor_token] = {"ID": constante_id, "Tipo": "Constante"}
                    constante_id += 1

            pos += len(valor_token)
        else:
            error_char = codigo_fuente[pos]
            errores_lexicos.append((error_char, pos))
            pos += 1

    return tokens_encontrados, tabla_simbolos, errores_lexicos

# -------------------- Gramática BNF --------------------
bnf_grammar = r"""
    start: stmt+

    stmt: "if" expr "then" stmt
        | "for" IDENTIFICADOR ":=" expr ";" stmt
        | "print" "(" expr ")" ";"
        | IDENTIFICADOR ":=" expr ";"
        | "{" stmt+ "}"

    expr: term (("+"|"-") term)*
    term: factor (("*"|"/") factor)*
    factor: CONSTANTE_ENTERA | IDENTIFICADOR | "(" expr ")"

    %import common.WS
    %ignore WS

    CONSTANTE_ENTERA: /\b(100|[0-9]{1,2})\b/
    IDENTIFICADOR: /\b[a-zA-Z][a-zA-Z0-9]{0,14}\b/
"""

parser = Lark(bnf_grammar, start='start')

# -------------------- Código de prueba --------------------
codigo_prueba = 'if x := 10 then print(x + 5); y := 3a;'  # contiene error léxico ("3a")

# -------------------- Ejecución del Análisis --------------------
tokens, tabla_simbolos, errores_lexicos = analizador_lexico(codigo_prueba)

# Mostrar tokens
print("\n Tokens detectados:")
for tipo, valor in tokens:
    print(f"{tipo:20}: {valor}")

# Mostrar tabla de símbolos
print("\n Tabla de Símbolos:")
for simbolo, info in tabla_simbolos.items():
    print(f"{info['ID']}: {simbolo} -> {info['Tipo']}")

# Mostrar errores léxicos
if errores_lexicos:
    print("\n Errores Léxicos:")
    for char, pos in errores_lexicos:
        print(f"Carácter inesperado '{char}' en posición {pos}")
else:
    print("\n Sin errores léxicos.")

# Análisis sintáctico y árbol de derivación
try:
    tree = parser.parse(codigo_prueba)
    print("\n Análisis sintáctico exitoso.")
    # Guardar imagen del árbol (opcional)
    pydot__tree_to_png(tree, "arbol_derivacion.png")
    print(" Árbol de derivación guardado como 'arbol_derivacion.png'")
except UnexpectedInput as e:
    print("\n Error sintáctico detectado:")
    print(f"Descripción: {str(e)}")
    print(f"Línea {e.line}, columna {e.column}")
