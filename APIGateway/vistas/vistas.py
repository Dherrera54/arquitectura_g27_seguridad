from flask_restful import Resource
from ..modelos import db, Paciente, PacienteSchema, Tratamiento, TratamientoSchema
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required , create_access_token

import logging


paciente_schema = PacienteSchema()
tratamiento_schema = TratamientoSchema()

class VistaPacientes(Resource):

    def get(self):
        return [paciente_schema.dump(paciente) for paciente in Paciente.query.all()]


class VistaLogIn(Resource):
    def post(self):
            logging.basicConfig(filename='log.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
            logging.info('Inicio de sesion fue exitoso')
            paciente = Paciente.query.filter(Paciente.nombre == request.json["nombre"],
                                       Paciente.contrasena == request.json["contrasena"]).first()
            db.session.commit()
            if paciente is None:
                return "El paciente no existe", 404
            else:
                token_de_acceso = create_access_token(identity=paciente.id)
                return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id_paciente":paciente.id}


class VistaSignIn(Resource):

    def post(self):
        nuevo_paciente = Paciente(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        token_de_acceso= create_access_token(identity=request.json['nombre'])
        db.session.add(nuevo_paciente)
        db.session.commit()
        return {'mensaje':f'paciente {nuevo_paciente.nombre} creado exitosamente', 'token de acceso':token_de_acceso}


class VistaPaciente(Resource):

    @jwt_required()
    def put(self, id_paciente):
        paciente = Paciente.query.get_or_404(id_paciente)
        paciente.nombre = request.json.get("nombre",paciente.nombre)
        paciente.contrasena = request.json.get("contrasena",paciente.contrasena)
        db.session.commit()
        return paciente_schema.dump(paciente)

    @jwt_required()
    def get(self,id_paciente):
        paciente = Paciente.query.get_or_404(id_paciente)
        return paciente_schema.dump(paciente)

class VistaTratamientoPaciente(Resource):

    @jwt_required()
    def post(self, id_paciente):
        nuevo_tratamiento = Tratamiento(tratamiento=request.json["tratamiento"])
        paciente = Paciente.query.get_or_404(id_paciente)
        paciente.tratamientos.append(nuevo_tratamiento)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'Nombre de tratamiento existente',409

        return tratamiento_schema.dump(nuevo_tratamiento)