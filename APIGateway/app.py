from APIGateway import create_app
from .modelos import db, Paciente
from flask_restful import Api
from .vistas import VistaPacientes, VistaSignIn, VistaLogIn, VistaPaciente, VistaTratamientoPaciente
from flask_jwt_extended import JWTManager

app =  create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaPacientes, '/pacientes')
api.add_resource(VistaPaciente, '/paciente/<int:id_paciente>')
api.add_resource(VistaTratamientoPaciente, '/paciente/<int:id_paciente>/tratamiento')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')

jwt = JWTManager(app)