from database import db

class Candidato(db.Model):
    num_candidato = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nome = db.Column(db.String(40))
    idade = db.Column(db.Integer)
    partido = db.Column(db.String(40))
    cargo = db.Column(db.String(20))

class Votacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_candidato1 = db.Column(db.Integer, db.ForeignKey('candidato.num_candidato'))
    num_candidato2 = db.Column(db.Integer, db.ForeignKey('candidato.num_candidato'))
    cargo = db.Column(db.String(20))

class Votos(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_votacao = db.Column(db.Integer, db.ForeignKey('votacao.id'), nullable=False)
    num_candidato = db.Column(db.Integer, db.ForeignKey('candidato.num_candidato'), nullable=False)
    votos = db.Column(db.Integer, nullable=False)

    def quantidade_votos(id_votacao, num_candidato=None):
        queries = [Votos.id_votacao == id_votacao, ]
        if num_candidato:
            queries.append(Votos.num_candidato == num_candidato)
        return Votos.query.filter(*queries).count()