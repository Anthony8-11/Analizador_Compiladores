import re

# Definición de tokens
TOKENS = {
    'PALABRA_RESERVADA': r'\b(if|else|for|print|int|b|f|h|j|k)\b',
    'IDENTIFICADOR': r'\b[a-zA-Z][a-zA-Z0-9]{0,14}\b',  # Máximo 15 caracteres
    'CONSTANTE_ENTERA': r'\b(100|[0-9]{1,2})\b',  # Entre 0 y 100
    'OPERADOR_ARITMETICO': r'[+\-*/]',
    'OPERADOR_ASIGNACION': r'\:=',
    'OPERADOR_RELACIONAL': r'>=|<=|<>|>|<|=',
    'SIMBOLO': r'[{}\[\]();.,]',
    'CADENA': r'"[bfhjk]*"',  # Cadenas con solo bfhjk
}

# Expresión regular combinada para reconocer todos los tokens
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS.items())

def analizador_lexico(codigo_fuente):
    tokens_encontrados = []
    for match in re.finditer(token_regex, codigo_fuente):
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)
        tokens_encontrados.append((tipo_token, valor_token))
    return tokens_encontrados

# Ejemplo de código fuente para analizar
codigo_prueba = "if x := 10 then print(x + 5);"

tokens = analizador_lexico(codigo_prueba)

# Imprimir tokens detectados
for tipo, valor in tokens:
    print(f"{tipo}: {valor}")
