import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
from lark import Lark, Transformer, UnexpectedInput

# Tokens definidos con expresiones regulares
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

# Unión de expresiones regulares
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS.items())

# Análisis léxico
def analizador_lexico(codigo_fuente):
    tokens_encontrados = []
    tabla_simbolos = {}
    errores_lexicos = []
    identificador_id = 1
    constante_id = 1

    for match in re.finditer(token_regex, codigo_fuente):
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

    # Identificar errores léxicos (caracteres no coincidentes)
    posiciones_validas = {m.start() for m in re.finditer(token_regex, codigo_fuente)}
    for i, c in enumerate(codigo_fuente):
        if not c.isspace() and i not in posiciones_validas:
            errores_lexicos.append((c, i))

    return tokens_encontrados, tabla_simbolos, errores_lexicos

# Gramática BNF para Lark
bnf_grammar = r"""
start: stmt+

stmt: asignacion ";"
    | imprimir ";"

asignacion: IDENTIFICADOR OPERADOR_ASIGNACION expr

imprimir: "print" "(" expr ")"

expr: expr OPERADOR_ARITMETICO expr   -> operacion
    | IDENTIFICADOR
    | CONSTANTE_ENTERA

%import common.CNAME -> IDENTIFICADOR
%import common.INT -> CONSTANTE_ENTERA
%import common.WS
%ignore WS

OPERADOR_ASIGNACION: ":="
OPERADOR_ARITMETICO: /\+|-|\*|\//
"""

# Analizador sintáctico con árbol
parser = Lark(bnf_grammar, start='start', parser='lalr')

# Transformador para imprimir árboles si se desea
class TreePrinter(Transformer):
    def operacion(self, items):
        return f"({items[0]} op {items[2]})"

# Código fuente de prueba con error
#codigo_prueba = "if x := 10 then print(x + 5); y := 3a;"
#Código fuente correcto
codigo_prueba = "x := 10; print(x + 5);"

# Ejecutar análisis léxico
tokens, tabla_simbolos, errores_lexicos = analizador_lexico(codigo_prueba)

# Mostrar tokens
print("\n Tokens detectados:")
for tipo, valor in tokens:
    print(f"{tipo:<20}: {valor}")

# Mostrar tabla de símbolos
print("\n Tabla de Símbolos:")
for simbolo, info in tabla_simbolos.items():
    print(f"{info['ID']}: {simbolo} -> {info['Tipo']}")

# Mostrar errores léxicos
if errores_lexicos:
    print("\n Errores Léxicos:")
    for caracter, posicion in errores_lexicos:
        print(f"Carácter inesperado '{caracter}' en posición {posicion}")
else:
    print("\n No se encontraron errores léxicos.")

# Análisis sintáctico
print("\n Análisis Sintáctico:")
try:
    tree = parser.parse(codigo_prueba)
    print(" Análisis sintáctico exitoso. Árbol de derivación:")
    print(tree.pretty())
except UnexpectedInput as e:
    print(" Error sintáctico detectado:")
    print(f"Descripción: {e}")
    print(f"Línea {e.line}, columna {e.column}")
    print(e.get_context(codigo_prueba))

