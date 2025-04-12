import re

# Definir los tokens con expresiones regulares
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

# Combinar todas las expresiones regulares en una sola
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS.items())

def analizador_lexico(codigo_fuente):
    tokens_encontrados = []
    tabla_simbolos = {}  # Diccionario para la tabla de símbolos
    identificador_id = 1  # ID autoincremental para identificadores
    constante_id = 1  # ID autoincremental para constantes

    for match in re.finditer(token_regex, codigo_fuente):
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)
        
        tokens_encontrados.append((tipo_token, valor_token))

        # Guardar identificadores en la tabla de símbolos
        if tipo_token == "IDENTIFICADOR":
            if valor_token not in tabla_simbolos:
                tabla_simbolos[valor_token] = {"ID": identificador_id, "Tipo": "Identificador"}
                identificador_id += 1

        # Guardar constantes en la tabla de símbolos
        elif tipo_token == "CONSTANTE_ENTERA":
            if valor_token not in tabla_simbolos:
                tabla_simbolos[valor_token] = {"ID": constante_id, "Tipo": "Constante"}
                constante_id += 1

    return tokens_encontrados, tabla_simbolos

# Código de prueba
codigo_prueba = "if x := 10 then print(x + 5);"

# Ejecutar el analizador
tokens, tabla_simbolos = analizador_lexico(codigo_prueba)

# Imprimir los tokens encontrados
print("\nTokens detectados:")
for tipo, valor in tokens:
    print(f"{tipo}: {valor}")

# Imprimir la tabla de símbolos
print("\nTabla de Simbolos:")
for simbolo, info in tabla_simbolos.items():
    print(f"{info['ID']}: {simbolo} -> {info['Tipo']}")
