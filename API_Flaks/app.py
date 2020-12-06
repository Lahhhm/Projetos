from flask import Flask, jsonify, request
import json  #Lista desenv. eh em json e arquivo recebido do body tbm

app = Flask(__name__)

desenvolvedores = [
    {
    'id':'0',
    'nome':'Bruno',
     'habilidades':['Python', 'Flask']
     },
    {
    'id':'1',
    'nome':'Vanessa',
     'habilidades':['Python', 'Docker']}
]
#devolve um desenvolvedor pelo id, tbm altera e deleta um desenvolvedor
@app.route('/dev/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def desenvolvedor(id):
    if request.method == 'GET': #Caso chamar Consulta, execute
        try:
            response = desenvolvedores[id]
        except IndexError:
            mensagem = 'Desenvolvedor de ID {} não existe'.format(id)
            response = {'status':'erro', 'mensagem':mensagem}
            print(desenvolvedor)
        except Exception:   #Erro nao previsto
            mensagem = 'Erro desconhecido. Procure o administrador da API'
            response = {'status':'erro', 'mensagem':mensagem}
        return jsonify(response)
    elif request.method == 'PUT': #Caso seja alteracao, execute
        dados = json.loads(request.data)  #Vai mandar um Json dentro do Body, esse Json substitui o valor atual, pelo novo
        desenvolvedores[id] = dados
        print(desenvolvedores[id])
        return jsonify(dados)
    elif request.method == 'DELETE':
        desenvolvedores.pop(id)
        return jsonify({'status':'sucesso', 'message':'Registro Excluído'})

#Lista todos os desenvolvedores e permite registrar um novo desenvolvedor
@app.route('/dev/', methods=['POST', 'GET'])
def lista_desenvolvedores():
    if request.method == 'POST':
        dados = json.loads(request.data) #recebendo dados json
        posicao = len(desenvolvedores) #Ler posicao na lista
        dados['id'] = posicao
        desenvolvedores.append(dados)
        print(dados)
        return jsonify(desenvolvedores[posicao])
    elif request.method == 'GET':
        return jsonify(desenvolvedores) #Retorna a lista


if __name__ == '__main__':
    app.run(debug=True, port=5004)
    