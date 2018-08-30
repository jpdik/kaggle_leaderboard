import os
raiz = os.path.dirname(os.path.abspath(__file__))
FILE = "/data.json"

def atualizar_file(data):
    with open(raiz + FILE, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)

headers = (read_data.split('\n')[0]).split(",")
headers.insert(0, "position")
data = []

for k,v in enumerate(read_data.split('\n')[:-2]):
    values = v.split(",")
    valor = dict(zip(headers, values))
    data.append(valor)