import kaggle
import io
from contextlib import redirect_stdout
import os
import json
import hashlib

from flask import Flask, request, Response
from flask_cors import CORS

raiz = os.path.dirname(os.path.abspath(__file__))
FILE = "/data.json"
hash_competicao = ""

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def atualizar_file(data):
    with open(raiz + FILE, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)

def carregar_file():
    if(os.path.exists(raiz + FILE)):
        return json.load(open(raiz + FILE, 'r'))

def checa_hash_comp():
    global hash_competicao
    hasher = hashlib.md5()
    with open(raiz + FILE, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    if hasher.hexdigest() != hash_competicao:
        hash_competicao = hasher.hexdigest()
        return True
    return False

@app.route('/', methods=['GET'])
def ver_competicao():
    f = io.StringIO()
    with redirect_stdout(f):
        kaggle.api.competition_leaderboard_cli("kddbr-2018", view=True, csv_display=True, quiet=True)
    read_data = f.getvalue()
    read_data = read_data.split('\n')[1:-2]

    headers = (read_data[0]).split(",")
    headers.insert(0, "position")
    data = {"data": []}

    for k,v in enumerate(read_data[1:], 1):
        values = v.split(",")
        values.insert(0, k)
        valor = dict(zip(headers, values))
        data['data'].append(valor)

    atualizar_file(data)
    news = checa_hash_comp()
    if news == True:
        return json.dumps({"news": news, "data": carregar_file()}), 200
    return json.dumps({"news": news}), 200

if __name__ == '__main__':
    app.run(debug=True)