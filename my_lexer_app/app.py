from flask import Flask, render_template, request, jsonify
from lexer import lexer

app = Flask(__name__)

def match_token(token_type, column):
    mapping = {
        'PROGRAMA': 'PR', 'FIN': 'PR', 'LEER': 'PR', 'IMPRIMIR': 'PR', 'ENTERO': 'PR', 'LA': 'PR', 'ES': 'PR',
        'IDENTIFICADOR': 'ID', 'PARENIZQ': 'PI', 'PARENDER': 'PD', 'LLAVEIZQ': 'LI',
        'LLAVEDER': 'LD', 'PUNTOCOMA': 'PC', 'COMA': 'CO', 'ASIGNACION': 'OP',
        'VAR': 'VAR', 'SUM': 'SUM', 'ER': 'ERR'
    }
    return mapping.get(token_type, '') == column

def analyze_code(code):
    lexer.lineno = 1
    lexer.input(code)
    tokens = []
    token_counts = {col: 0 for col in ['PR', 'ID', 'PI', 'PD', 'LI', 'LD', 'PC', 'VAR', 'SUM', 'CO', 'ER']}

    for tok in lexer:
        if not tok:
            continue
        if tok.type == 'CADENA':
            for sub_token in tok.value:
                token_dict = {
                    "line": tok.lineno,
                    "token": sub_token[1],
                    "types": [match_token(sub_token[0], col) for col in token_counts]
                }
                tokens.append(token_dict)
                for i, col in enumerate(token_counts):
                    if token_dict["types"][i]:
                        token_counts[col] += 1
        else:
            token_dict = {
                "line": tok.lineno,
                "token": tok.value,
                "types": [match_token(tok.type, col) for col in token_counts]
            }
            tokens.append(token_dict)
            for i, col in enumerate(token_counts):
                if token_dict["types"][i]:
                    token_counts[col] += 1
    
    return tokens, token_counts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form['code']
    tokens, token_counts = analyze_code(code)
    return jsonify({'tokens': tokens, 'token_counts': token_counts})

if __name__ == "__main__":
    app.run(debug=True)
