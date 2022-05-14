from models import (
    Candidato
)
from database import db

NoneType = type(None)

def get_candidato_by_id(id):
    candidato = Candidato.query.filter_by(num_candidato=id).first()
    if isinstance(candidato,NoneType):
            return dict(error=True, message='Candidato inexistente no banco de dados!')
    candidato_dict = {
            "num_candidato": candidato.num_candidato,
            "nome": candidato.nome,
            "idade": candidato.idade,
            "partido": candidato.partido,
            "cargo": candidato.cargo
        }
    return candidato_dict

def get_all_candidatos():
    candidatos_objetos = Candidato.query.all()
    candidatos = list()
    for objeto in candidatos_objetos:
        candidato = {
            "num": objeto.num_candidato,
            "nome": objeto.nome,
            "idade": objeto.idade,
            "partido": objeto.partido,
            "cargo": objeto.cargo
        }
        candidatos.append(candidato)
    return candidatos

def register_candidato(num: int, nome: str, idade: int, partido: str, cargo: str):
    if get_candidato_by_id(id=num):
        return dict(error=True, message='Candidato já cadastrado!')
    candidato = Candidato(
                num_candidato=num,
                nome=nome,
                idade=idade,
                partido=partido,
                cargo=cargo
            )
    with db.engine.connect():
        db.session.add(candidato)
        db.session.commit()