import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

# Definir los tokens con expresiones regulares y sus interpretaciones
TOKENS = {
    # Palabras reservadas: palabras clave del lenguaje
    'PALABRA_RESERVADA': (r'\b(if|else|for|print|int|b|f|h|j|k)\b', "Palabras clave del lenguaje"),
    
    # Identificadores: comienzan con una letra y pueden contener hasta 15 caracteres alfanuméricos
    'IDENTIFICADOR': (r'\b[a-zA-Z][a-zA-Z0-9]{0,14}\b', "Identificadores con hasta 15 caracteres"),
    
    # Constantes enteras: números enteros del 0 al 100
    'CONSTANTE_ENTERA': (r'\b(100|[0-9]{1,2})\b', "Números enteros entre 0 y 100"),
    
    # Operadores aritméticos: suma, resta, multiplicación, división
    'OPERADOR_ARITMETICO': (r'[+\-*/]', "Operadores aritméticos"),
    
    # Operadores de asignación: :=
    'OPERADOR_ASIGNACION': (r'\:=', "Operador de asignación"),
    
    # Operadores relacionales: comparaciones
    'OPERADOR_RELACIONAL': (r'>=|<=|<>|>|<|=', "Operadores relacionales"),
    
    # Símbolos especiales: paréntesis, corchetes, llaves, punto y coma, etc.
    'SIMBOLO': (r'[{}\[\]();.,]', "Símbolos especiales"),
    
    # Cadenas: entre comillas dobles, solo permiten ciertos caracteres
    'CADENA': (r'\"[bfhjk]*\"', "Cadenas con caracteres específicos"),
}

# Expresiones regulares adicionales con ejemplos válidos e inválidos
EXPRESIONES = {
    "Expresión 1": (r'^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8}$',
                     "Debe contener al menos 2 mayúsculas, 1 carácter especial, 2 números y 3 minúsculas en 8 caracteres",
                     "Aa1!bbb2", "abc12345"),
    "Expresión 2": (r'^[a-z0-9_-]{3,16}$', "Usuario válido entre 3 y 16 caracteres alfanuméricos, guion o guion bajo", "user_12", "Us"),
    "Expresión 3": (r'^-?\d*(\.\d+)?$', "Número entero o decimal opcionalmente negativo", "-12.34", "12..34"),
    "Expresión 4": (r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$', "Solo letras y caracteres especiales en español", "José", "Jose1"),
    "Expresión 5": (r'^[0-9]+[.,]{1,1}0{2,2}$', "Número con dos decimales exactos en 0", "123.00", "123.456"),
}

# Combinar todas las expresiones regulares en una sola
regex_patterns = '|'.join(f'(?P<{name}>{pattern[0]})' for name, pattern in TOKENS.items())

def analizador_lexico(codigo_fuente):
    tokens_encontrados = []
    tabla_simbolos = {}
    tabla_errores = []
    
    # Usamos un solo contador para ambas categorías
    simbolo_id = 1
    
    # También mantendremos un registro de símbolos ya procesados para evitar duplicados
    simbolos_procesados = set()

    for match in re.finditer(regex_patterns, codigo_fuente):
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)
        
        if tipo_token:
            tokens_encontrados.append((tipo_token, valor_token))

            # Verificar si es un identificador o constante y no ha sido procesado antes
            if tipo_token == "IDENTIFICADOR" and valor_token not in simbolos_procesados:
                tabla_simbolos[valor_token] = {"ID": simbolo_id, "Tipo": "Identificador"}
                simbolo_id += 1
                simbolos_procesados.add(valor_token)
            
            elif tipo_token == "CONSTANTE_ENTERA" and valor_token not in simbolos_procesados:
                tabla_simbolos[valor_token] = {"ID": simbolo_id, "Tipo": "Constante"}
                simbolo_id += 1
                simbolos_procesados.add(valor_token)
    
    # Detectar errores para tokens que no coinciden con ninguna regla
    # (Para una implementación más completa, necesitaríamos analizar el código fuente caractér por caractér)
    
    return tokens_encontrados, tabla_simbolos, tabla_errores

# Código de prueba
codigo_prueba = "if x := 10 then print(x + 5);"
# codigo_prueba = """
# int contador := 10;
# if contador >= 5 then {
#     resultado := contador + 20;
#     print("asdfg");
# }

# identificador12345 := 50;  # Error: Identificador demasiado largo
# numero_fuera_rango := 200; # Error: Número mayor a 100

# for i := 0; i <= 100; i := i + 1 {
#     suma := suma + i;
# }
# """


# Ejecutar el analizador
tokens, tabla_simbolos, tabla_errores = analizador_lexico(codigo_prueba)

# Imprimir tokens
print("\nTokens detectados:")
for tipo, valor in tokens:
    print(f"{tipo}: {valor}")

# Imprimir la tabla de símbolos
print("\nTabla de Símbolos:")
for simbolo, info in tabla_simbolos.items():
    print(f"{info['ID']}: {simbolo} -> {info['Tipo']}")

# Imprimir tabla de errores
print("\nErrores detectados:")
if tabla_errores:
    for error in tabla_errores:
        print(f"Valor: {error[0]}, Error: {error[1]}")
else:
    print("No se encontraron errores.")

# Verificación de expresiones adicionales
print("\nVerificación de expresiones adicionales:")
for nombre, (expresion, descripcion, valido, invalido) in EXPRESIONES.items():
    print(f"\n{nombre}: {descripcion}")
    print(f"Ejemplo válido ({valido}):", "Válido" if re.fullmatch(expresion, valido) else "Inválido")
    print(f"Ejemplo inválido ({invalido}):", "Válido" if re.fullmatch(expresion, invalido) else "Inválido")