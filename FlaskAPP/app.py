from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/flaskdb'
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(255))
    anonimo = db.Column(db.Bit)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    cep = db.Column(db.String)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    bairro = db.Column(db.String)
    descricaoLocal = db.Column(db.String)

    def __repr__(self):
        return f"Report: {self.titulo}"

    def __init__(self, titulo):
        self.titulo = titulo

def format_report(report):
    return {
        "id": report.id,
        "titulo": report.titulo,
        "descricao": report.descricao,
        "anonimo": report.anonimo,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "cep": report.cep,
        "cidade": report.cidade,
        "estado": report.estado,
        "bairro": report.bairro,
        "descricaoLocal": report.descricaoLocal
    }

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/reports', methods = ['POST'])
def create_event():
    report = Report(titulo = request.json['titulo'])
    report.descricao = request.json['descricao']
    report.anonimo = request.json['anonimo']
    report.latitude = request.json['latitude']
    report.longitude = request.json['longitude']
    report.cep = request.json['cep']
    report.cidade = request.json['cidade']
    report.estado = request.json['estado']
    report.bairro = request.json['bairro']
    report.descricaoLocal = request.json['descricaoLocal']
    db.session.add(report)
    db.session.commit()
    return format_report(report)

# conseguir todos os reports
@app.route('/reports', methods =['GET'])
def get_reports():
    reports = Report.query.order_by(Report.id.asc()).all()
    report_list = []
    for report in reports:
        report_list.append(format_report(report))
    return {'reports': report_list}

# conseguir apenas 1 report
@app.route('/reports/<id>', methods = ['GET'])
def get_report(id):
    report = Report.query.filter_by(id=id).one()
    formatted_report = format_report(report)
    return {'report': formatted_report}

# deletar um report
@app.route('/reports/<id>', methods = ['DELETE'])
def delete_report(id):
   report = Report.query.filter_by(id=id).one()
   db.session.delete(report)
   db.session.commit()
   return f'Report (id: {id}) deleted!'

if __name__ == '__main__':
    app.run()
