import ply.lex as lex

# Lista de tokens
tokens = [
    'PROGRAMA', 'FIN', 'LEER', 'IMPRIMIR', 'ENTERO', 'IDENTIFICADOR',
    'NUMERO', 'PARENIZQ', 'PARENDER', 'LLAVEIZQ', 'LLAVEDER',
    'PUNTOCOMA', 'COMA', 'ASIGNACION', 'MAS', 'LA', 'ES', 'VAR', 'CADENA'
]

# Palabras reservadas
reserved = {
    'programa': 'PROGRAMA', 'end': 'FIN', 'read': 'LEER', 'printf': 'IMPRIMIR',
    'int': 'ENTERO', 'la': 'LA', 'es': 'ES'
}

# Lista de identificadores específicos
identificadores_especificos = ['suma', 'resta', 'multiplicación', 'división']

t_ignore = ' \t'
t_PARENIZQ = r'\('
t_PARENDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PUNTOCOMA = r';'
t_COMA = r','
t_ASIGNACION = r'='
t_MAS = r'\+'

def t_CADENA(t):
    r'\"([^\\"]|\\.)*\"'
    cadena = t.value[1:-1]  # remove the double quotes
    palabras = cadena.split()
    new_tokens = []
    for palabra in palabras:
        if palabra in reserved:
            new_tokens.append((reserved[palabra], palabra))
        elif palabra in identificadores_especificos:
            new_tokens.append(('IDENTIFICADOR', palabra))
        else:
            new_tokens.append(('CADENA', palabra))
    t.value = new_tokens
    t.type = 'CADENA'
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in identificadores_especificos:
        t.type = 'IDENTIFICADOR'
    else:
        t.type = 'VAR'
    return t

def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()
