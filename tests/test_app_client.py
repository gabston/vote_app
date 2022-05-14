from flask import Flask
import json
import random



def quantidade_votos(id: int):
    return random.randint(0, 10)


class Query():

    def filter_by(*args, **kwargs):
        return 1

    def count(*args, **kwargs):
        return random.randint(0, 10)

    def all(obj):
        return obj

class DummyVotacao:
    id = 2
    num_candidato1 = 3
    num_candidato2 = 4
    cargo = 1

    query = Query()
        
def find_all():

  return [DummyVotacao]

def find_by_id(id: int):

    return [1]

class DummyVotos():

    """
    Votos.query.filter_by(id_votacao=id).count()
    """

    query = Query()

    def quantidade_votos(id: int):
        return random.randint(0, 10)

    # def count(*args, **kwargs):
    #     return random.randint(0, 10)

def test_index_page(app, mocker):
    client = app.test_client()
    url = '/'
    # Mocker 
    mocker.patch(
        "models.Votacao.find_all",
        find_all,
    )
    mocker.patch(
        "models.Votos.quantidade_votos",
        DummyVotos.quantidade_votos
    )
    # --- Mocker
    response = client.get(url)
    assert response.status_code == 200

def test_list_votacoes_endpoint(app, mocker):
    client = app.test_client()
    url = '/list/votacoes'
    mocker.patch(
        "models.Votacao.find_by_id",
        find_by_id
    )
    mocker.patch(
        "models.Votacao.find_all",
        find_all
    )
    response_by_id = client.get(url, query_string=json.dumps(dict(id=2)))
    response = client.get(url)
    assert response.status_code == 200
    assert response_by_id == 200