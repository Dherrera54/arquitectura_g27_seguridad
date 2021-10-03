from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(128))
    contrasena = db.Column(db.String(32))
    tratamientos = db.relationship('Tratamiento', cascade='all, delete, delete-orphan')

class Tratamiento(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tratamiento = db.Column(db.String(128))
    paciente = db.Column(db.Integer, db.ForeignKey("paciente.id"))

class PacienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Paciente
        include_relationships = True
        load_instance = True

class TratamientoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tratamiento
        include_relationships = True
        load_instance = True

