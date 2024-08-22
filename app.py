from flask_openapi3 import OpenAPI, Info , Tag
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

info = Info(title="Api do bloco de notas", version="1.0")
app = OpenAPI(__name__, info=info)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nota.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)

"""Criação do banco de dados"""
@app.before_first_request
def create_table():
    db.create_all()
    app.run(debug=True)

"""Classe de definição do banco de dados e os métodos de manipulação dele,
 a classe Nota vai herdar o db.Model do SQLAlchemy"""
class Nota(db.Model):
    __tablename__ = "nota"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    texto = db.Column(db.String(100))
    
    def __init__(self, titulo, texto):
        """Função inicia o banco de dados"""
        self.titulo = titulo
        self.texto = texto

    def json(self):
        """Função define o id, titulo e texto como json"""
        return {'id': self.id, 'titulo': self.titulo, 
                'texto': self.texto}    

# definindo as tags
# api_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tudo_tag = Tag(name="Obter notas", description="Obter todas as nota")
adicao_tag = Tag(name="Adicao de nota", description="Adicao de nota no bloco")
atualizacao_tag = Tag(name="Atualizacao de nota", description="Atualizacao de nota no bloco")
deletar_tag = Tag(name="Deletar nota", description="Apagar de nota no bloco")

# @app.get('/api', tags=[api_tag])
# def api():
    # """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    # return redirect('/openapi')

@app.get('/', methods=['GET'] , tags=[tudo_tag])
def obter_todas_notas():
    """Função que obtem todas as notas no banco de dados"""
    return jsonify({'Notas': [nota.json() for nota in Nota.query.all()]}) # Retorna a busca te todas as notas
    
@app.post('/', methods=['POST'] , tags=[adicao_tag])
def adicao_nota():
    """Função para adicionar nota no banco de dados usando titulo e texto como parametros"""
    requisicao = request.get_json() # Requisição da nota
    nova_nota = Nota(titulo=requisicao["titulo"], texto=requisicao["texto"]) # Criação da instancia da nossa Nota como um construtor
    db.session.add(nova_nota) # Adiciona nova nota na seção do banco de dados
    db.session.commit() # Fazer o commit das mudanças no banco de dados
    return jsonify(nova_nota.json()) # Retorna a nova nota

@app.put('/', methods=['PUT'] , tags=[atualizacao_tag])
def edicao_nota():
    """Função para atualizar os detalhes da nota usando o id, titulo e descrição como parametros"""
    requisicao = request.get_json() # Requisição da nota
    nota_a_atualizar = Nota.query.get(requisicao['id']) # Procura a a nota no banco de dados pelo id
    if nota_a_atualizar:
        nota_a_atualizar.titulo = requisicao['titulo'] # Atualiza no banco de dados o novo titulo
        nota_a_atualizar.texto = requisicao['texto'] # Atualiza no banco de dados o novo texto
        db.session.commit() # Faz o commit das mudanças no banco de dados
        return jsonify(nota_a_atualizar.json())

@app.delete('/', methods=['DELETE'] , tags=[deletar_tag])
def deletar_nota():
    """Função para deletar a nota do banco de dados usando o id da nota como o parametro"""
    requisicao = request.get_json() # Requisição da nota
    nota_a_deletar = Nota.query.get(requisicao['id']) # Procurar a a nota no banco de dados pelo id
    if nota_a_deletar:
        db.session.delete(nota_a_deletar) # Deleta a nota no banco de dados
        db.session.commit() # Fazer o commit da nova mudança no banco de dados
        return jsonify({"message": "Nota deletada"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)