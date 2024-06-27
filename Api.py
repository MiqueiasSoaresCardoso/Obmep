from flask import Flask, jsonify, request
from pymongo import MongoClient

# Configuração da conexão com MongoDB Atlas
uri = "mongodb+srv://miqueiassoares:pMmAke6bpsOI8u6T@cluster0.sjuug1b.mongodb.net/Obmep"
client = MongoClient(uri)
db = client['Obmep']
collection = db['Escola']

app = Flask(__name__)

#ENDPOINT - 02
#Dentro de um determinado estado,selecionando o nível e a edição da olimpíada, conseguir visualizar qual instituição mais se destacou nas premiações
@app.route('/api/buscarinstuicaoestado', methods = ['GET'])
def buscarinstuicao():
    estado = request.args.get('estado',default= 'PB',type= str)
    nivel = request.args.get('nivel', default= 3, type= int)
    edicao = request.args.get('edicao', default= 2023, type= int)

    pipeline = [
        {
            '$match': {
                'uf': estado,
                'nivel': nivel,
                'edicao': edicao
            }
        },
        {
            '$group': {
                '_id': '$escola',
                'total_premiacoes': {'$sum': 1}
            }
        },
        {
            '$sort': {
                'total_premiacoes': -1
            }
        },
        {
            '$limit': 1  # Limitando para exibir apenas a instituição com mais premiações
        }
    ]

    resultados = list(collection.aggregate(pipeline))

    if resultados:
        return jsonify({
            'estado': estado,
            'nivel': nivel,
            'edicao': edicao,
            'instituicao': resultados[0]['_id'],
            'total_premiacoes': resultados[0]['total_premiacoes'],
        }),200
    else:
        return jsonify({'message':'Nenhuma instituição encontrada para os critérios especificados'}),404

if __name__ == '__main__':
    app.run(debug=True)