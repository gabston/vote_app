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

    def find_all():
        return Votacao.query.all()
    
    def find_by_id(id):
        votacao =  Votacao.query.filter_by(id=id).first()
        votacao_dict = {
                "id": votacao.id,
                "num_candidato1": votacao.num_candidato1,
                "num_candidato2": votacao.num_candidato2,
                "cargo": votacao.cargo
            }
        return votacao_dict

class Votos(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_votacao = db.Column(db.Integer, db.ForeignKey('votacao.id'), nullable=False)
    num_candidato = db.Column(db.Integer, db.ForeignKey('candidato.num_candidato'), nullable=False)
    votos = db.Column(db.Integer, nullable=False)

    def quantidade_votos(id):
        return Votos.query.filter_by(id_votacao=id).count()