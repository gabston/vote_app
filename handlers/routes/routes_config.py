from crud import (
    get_candidato_by_id,
    get_all_candidatos,
    register_candidato
)
from database import db
from flask import request, render_template, Response
from models import (
    Candidato,
    Votacao,
    Votos
)
import json

NoneType=type(None)

def get_response(content, message=False, error=False):
    """
    Make a response to an endpoint
    """
    body = dict()
    body['content'] = content
    if error:
        body['content'] = dict(message=message, error=True)
        return Response(json.dumps(body), mimetype='application/json')
    if message:
        body['message'] = message
    return Response(json.dumps(body), mimetype='application/json')

""" class IndexRoute():
    def __init__(self, app: object):
        app.route('/', methods=['GET'])(self.pagina_votar)

    def pagina_votar(self):
        lista = [item for item in Votacao.query.all()]
        votos_objeto = []
        for item in lista:
            votos_objeto.append(Votos.quantidade_votos(id=item.id))
        print(votos_objeto)
        return render_template('form.html', lista=lista, votos=votos_objeto) """

def api_routes(app):

    @app.route('/vote', methods=['POST',])
    def registra_voto():
        payload = dict(request.form)
        if Votacao.query.filter_by(id=payload['id_votacao']).first():
            candidatos = Votacao.query.filter_by(id=payload['id_votacao'],num_candidato1=payload['num']).first() or Votacao.query.filter_by(id=payload['id_votacao'],num_candidato2=payload['num']).first()
            if candidatos:
                voto = Votos(id_votacao=payload['id_votacao'], num_candidato=payload['num'], votos=" ")
                db.session.add(voto)
                db.session.commit()
                return 'Voto registrado com sucesso, obrigado!'
            else:
                return f"Candidato {payload['num']} não encontrado na votação!"
        else:
            return 'a'

    @app.route('/', methods=['GET'])
    def pagina_votar():
        lista = [item for item in Votacao.find_all()]
        votos_objeto = []
        for item in lista:
            votos_objeto.append(Votos.quantidade_votos(id=item.id))
        return render_template('form.html', lista=lista, votos=votos_objeto)

    @app.route('/ksjdaksjd', methods=['GET'])
    def votos():
        lista = [item for item in Votacao.query.all()]
        for item in lista:
            votos = [Votacao.query.filter_by(id=item.id).count()]
        return render_template('index.html', lista=lista, votos=votos)

    # Listar Candidatos
    @app.route('/list/candidatos', methods=['GET',])
    def listar_candidatos():
        if request.args.get("id"):
            id = request.args.get("id")
            content = get_candidato_by_id(id=id)
            return get_response(content=content)
        content = get_all_candidatos()
        return get_response(content=content)

    # Cadastrar Candidato
    @app.route('/register/candidato', methods=['POST', ])
    def cadastro_candidato():
        try:
            json_query = request.get_json()
            register_candidato(
                num=json_query['num_candidato'],
                nome=json_query['nome'],
                idade=json_query['idade'],
                partido=json_query['partido'],
                cargo=json_query['cargo']
            )
            return get_response(content=json_query, message='Usuário criado com sucesso')
        except KeyError as e:
            return get_response(content=json_query, error=True, message=f'Faltam argumentos: {e}')
        except Exception as e:
            return get_response(content=json_query, error=True, message=f'{e}')

    # Deletar Candidato
    @app.route('/delete/candidato/<num>', methods=['DELETE',])
    def deleta_candidato(num):
        try:
            candidato_objeto = Candidato.query.filter_by(num_candidato=num).first()
            db.session.delete(candidato_objeto)
            db.session.commit()
            return get_response(content=candidato_objeto.nome, message='Usuario deletado com sucesso!')
        except Exception:
            return get_response(content={}, error=True, message=f'Erro ao deletar o Candidato {num}')

    # Atualizar candidato
    @app.route('/update/candidato/<id>', methods=['PUT',])
    def atualiza_candidato(id):
        try:
            candidato_objeto = Candidato.query.filter_by(num_candidato=id).first()
            request_json = request.get_json()

            if 'nome' in request_json:
                candidato_objeto.nome = request_json['nome']
            if 'idade' in request_json:
                candidato_objeto.idade = request_json['idade']
            if 'partido' in request_json:
                candidato_objeto.partido = request_json['partido']
            if 'cargo' in request_json:
                candidato_objeto.cargo = request_json['cargo']
            if 'num_candidato' in request_json:
                candidato_objeto.num_candidato = request_json['num_candidato']
            
            db.session.add(candidato_objeto)
            db.session.commit()

            return get_response(content=request_json, message='Candidato atualizado!')

        except Exception as e:
            return get_response(content=request_json, error=True, message=f'{e}')

    # Listar votações
    @app.route('/list/votacoes', methods=['GET',])
    def listar_votacoes():
        if request.args.get("id"):
            id = request.args.get("id")
            votacao = Votacao.find_by_id(id=id)
            if isinstance(votacao,NoneType):
                return get_response(content={}, error=True, message='Votação inexistente no banco de dados!')
            return get_response(content=votacao)
        votacao_objeto = Votacao.find_all()
        votacoes = list()
        for objeto in votacao_objeto:
            votacao = {
                "id": objeto.id,
                "num_candidato1": objeto.num_candidato1,
                "num_candidato2": objeto.num_candidato2,
                "cargo": objeto.cargo
            }
            votacoes.append(votacao)
        return get_response(content=votacoes)

    # Criar votação
    @app.route('/register/votacao', methods=['POST', ])
    def cadastro_votacao():
        try:
            json_query = request.get_json()
            votacao = Votacao(
                    num_candidato1=json_query['num_candidato1'], 
                    num_candidato2=json_query['num_candidato2'],  
                    cargo=json_query['cargo']
            )
            candidato1_objeto = Candidato.query.filter_by(num_candidato=votacao.num_candidato1).first()
            candidato2_objeto = Candidato.query.filter_by(num_candidato=votacao.num_candidato2).first()
            if not candidato1_objeto or not candidato2_objeto:
                return get_response(content={}, error=True, message='O número de uns dos candidatos não foram encontrados')
            db.session.add(votacao)
            db.session.commit()
            return get_response(content=json_query, message='Votaçao criada com sucesso')
        except KeyError as e:
            return get_response(content=json_query, error=True, message=f'Faltam argumentos: {e}')
        except Exception as e:
            return get_response(content=json_query, error=True, message=f'{e}')

    # Deletar votação
    @app.route('/delete/votacao/<id>', methods=['DELETE',])
    def deleta_votacao(id):
        try:
            votacao_objeto = Votacao.query.filter_by(id=id).first()
            id1 = votacao_objeto.num_candidato1
            id2 = votacao_objeto.num_candidato2
            candidato1 = Candidato.query.filter_by(num_candidato=id1).first()
            candidato2 = Candidato.query.filter_by(num_candidato=id2).first()

            db.session.delete(votacao_objeto)
            db.session.commit()
            return get_response(content={"candidato1": {"nome": candidato1.nome, "num": candidato1.num_candidato}, "candidato2": {"nome": candidato2.nome, "num": candidato2.num_candidato}}, message='Votação deletada com sucesso!')
        except Exception as e :
            return get_response(content={e}, error=True, message=f'Erro ao deletar votação {id}')

    # Atualizar votação
    @app.route('/update/votacao/<id>', methods=['PUT',])
    def update_votacao(id):
        try:
            votacao_objeto = Votacao.query.filter_by(id=id).first()
            request_json = request.get_json()

            if 'cargo' in request_json:
                votacao_objeto.cargo = request_json['cargo']
            if 'num_candidato1' in request_json:
                votacao_objeto.num_candidato1 = request_json['num_candidato1']
            if 'num_candidato2' in request_json:
                votacao_objeto.num_candidato2 = request_json['num_candidato2']
            
            db.session.add(votacao_objeto)
            db.session.commit()

            return get_response(content=request_json, message='Candidato atualizado!')

        except Exception as e:
            return get_response(content=request_json, error=True, message=f'{e}')

    # Listar voto
    @app.route('/list/votos', methods=['GET',])
    def listar_votos():
        if request.args.get("id"):
            id = request.args.get("id")
            voto_objeto = Votos.query.filter_by(id=id).first()
            if isinstance(voto_objeto,NoneType):
                return get_response(content={}, error=True, message='Votação inexistente no banco de dados!')
            voto_dict = {
                "id": voto_objeto.id,
                "num_candidato": voto_objeto.num_candidato,
                "cargo": voto_objeto.cargo
            }
            return get_response(content=voto_dict)
        votos_objetos = Votos.query.all()
        votos = list()
        for objeto in votos_objetos:
            voto_dict = {
                "id": objeto.id,
                "num_candidato": objeto.num_candidato,
                "id_votacao": objeto.id_votacao
            }
            votos.append(voto_dict)
        return get_response(content=votos)

    # Deletar voto
    @app.route('/delete/voto/<id>', methods=['DELETE',])
    def deletar_voto(id):
        if id == 'all':
            if request.args.get('candidato'):
                num = request.args.get('candidato')
                if Votacao.query.filter_by(num_candidato1=num).first() or Votacao.query.filter_by(num_candidato2=num).first():
                    if request.args.get('votacao'):
                        id_votacao = request.args.get('votacao')
                        if Votacao.query.filter_by(id=id_votacao).first():
                            voto_candidato = Votos.query.filter_by(id_votacao=id_votacao, num_candidato=num)
                            for voto in voto_candidato:
                                db.session.delete(voto)
                            db.session.commit()
                    votos_objeto = Votos.query.filter_by(num_candidato=num)
                    for voto in votos_objeto:
                        db.session.delete(voto)
                    db.session.commit()
                    return get_response(content={}, message='Votos deletados!')
                else:
                    return get_response(content={}, error=True, message='Candidato inexistente')
            else:
                return get_response(content={}, error=True, message='Candidato não informado!')
        else:
            return get_response(content={}, error=True, message='Parâmetro inexistente!')

    # Criar voto
    @app.route('/register/voto', methods=['POST',])
    def criar_voto():
        try:
            json = request.get_json()
            if not Candidato.query.filter_by(num_candidato=json['num_candidato']).first() or not Votacao.query.filter_by(id=json['id_votacao']).first():
                return get_response(content={}, error=True, message='Candidato ou votação não existe no banco.')
            voto = Votos(
                num_candidato=json['num_candidato'],
                id_votacao=json['id_votacao'],
                votos=json['votos']
            )
            db.session.add(voto)
            db.session.commit()
            return get_response(content=json, message=f'Voto adicionado ao candidato {voto.num_candidato}!')
        except KeyError:
            return get_response(content={}, error=True, message='Algum campo não foi informado corretamente!')
        except Exception as e:
            return get_response(content={}, error='True', message=e)

    # Atualizar voto
    @app.route('/update/voto/<id>', methods=['PUT',])
    def atualizar_voto(id):
        try:
            request_json = request.get_json()
            voto_objeto = Votos.quer.filter_by(id=id)
            if 'num_candidato' in request_json:
                voto_objeto.num_candidato = request_json['num_candidato']
            if 'id_votacao' in request_json:
                voto_objeto.id_votacao = request_json['id_votacao']
        except KeyError:
            return get_response(content={}, error=True, message='Algum campo não foi informado corretamente!')
        except Exception as e:
            return get_response(content={}, error='True', message=e)
    
    @app.route('/seila')
    def seila():
        return 'Hello World !'