import re
from lark import Lark, Transformer, Tree

# -----------------------
# ANALIZADOR LÉXICO
# -----------------------

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

def analizador_lexico(codigo_fuente):
    tokens_encontrados = []
    tabla_simbolos = {}
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

    return tokens_encontrados, tabla_simbolos

# -----------------------
# GRAMÁTICA BNF CORREGIDA PARA LARK
# -----------------------

bnf_grammar = """
    start: instruccion+

    instruccion: condicional
               | asignacion
               | impresion

    condicional: "if" expresion "then" instruccion ("else" instruccion)?
    asignacion: IDENTIFICADOR ":=" expresion ";"
    impresion: "print" "(" expresion ")" ";"

    expresion: termino ((OP_ARIT) termino)*
    termino: IDENTIFICADOR | CONSTANTE_ENTERA

    expresion: lista
                | termino ((OP_ARIT) termino)*

    lista: "[" [expresion ("," expresion)*] "]"


    IDENTIFICADOR: /[a-zA-Z][a-zA-Z0-9]{0,14}/
    CONSTANTE_ENTERA: /(100|[0-9]{1,2})/
    OP_ARIT: /[+\\-*/]/

    %import common.WS
    %ignore WS

"""

# -----------------------
# PARSER CON LARK
# -----------------------

parser = Lark(bnf_grammar, start='start')

class ArbolTransformer(Transformer):
    def instruccion(self, items):
        return Tree("instruccion", items)
    def asignacion(self, items):
        return Tree("asignacion", items)
    def impresion(self, items):
        return Tree("impresion", items)
    def condicional(self, items):
        return Tree("condicional", items)

# -----------------------
# PRUEBA
# -----------------------

codigo_prueba = "if x := 10 then print(x + 5);"

tokens, tabla_simbolos = analizador_lexico(codigo_prueba)

print("\nTokens detectados:")
for tipo, valor in tokens:
    print(f"{tipo}: {valor}")

print("\nTabla de Símbolos:")
for simbolo, info in tabla_simbolos.items():
    print(f"{info['ID']}: {simbolo} -> {info['Tipo']}")

print("\nÁrbol de derivación:")
try:
    arbol = parser.parse(codigo_prueba)
    arbol.transform(ArbolTransformer())
    print(arbol.pretty())
except Exception as e:
    print("Error en el análisis sintáctico:", e)
