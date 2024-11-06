from flask_restful import Resource, reqparse, fields, marshal_with, abort
from exceptions.exceptions import JugadorNoEncontradoException
from models import EquipoModel, FormacionModel, JugadorModel
from extensiones import db

equipo_post_args = reqparse.RequestParser()
equipo_post_args.add_argument("usuario_id", type=int, help="Usuario ID Requerido", required=True)
equipo_post_args.add_argument("formacion", type=str, help="Formación Requerida", required=True)
equipo_post_args.add_argument("jugadores_id", type=dict, help="Jugadores Requeridos", required=True)

equipo_fields = {
    'equipo_id': fields.Integer,
    'usuario_id': fields.Integer,
    'valor': fields.Integer,
    'formacion': fields.String,
    'jugadores_id': fields.Raw  # Para el campo JSON de jugadores
}

class EquipoResource(Resource):
    @marshal_with(equipo_fields)
    def get(self, equipo_id):
        result = EquipoModel.query.filter_by(equipo_id=equipo_id).first()
        if not result:
            abort(404, message="Equipo no encontrado")
        return result
    
    def delete(self, equipo_id):
        equipo = EquipoModel.query.filter_by(equipo_id=equipo_id).first()
        if not equipo:
            abort(404, message="Equipo no encontrado")
        db.session.delete(equipo)
        db.session.commit()
        return {"message": "Equipo eliminado"}, 200
    
    @marshal_with(equipo_fields)
    def post(self):
        args = equipo_post_args.parse_args()
        usuario_id = args['usuario_id']
        equipo_existente = EquipoModel.query.filter_by(usuario_id=usuario_id).first() #revisar si ya tiene un equipo, en tal caso borrarlo
        if equipo_existente:
            db.session.delete(equipo_existente)
            db.session.commit()
        
        formacion = args['formacion']
        formacion_model = FormacionModel.query.filter_by(formacion=formacion).first()
        if not formacion_model:
            abort(404, message="Formación no encontrada")

        delanteros_requeridos = formacion_model.delanteros
        mediocampistas_requeridos = formacion_model.mediocampistas
        defensores_requeridos = formacion_model.defensores

        jugadores = args['jugadores_id']

        if len(jugadores['defensores']) != defensores_requeridos:
            abort(400, message=f"Se requieren {defensores_requeridos} defensores titulares")
        if len(jugadores['mediocampistas']) != mediocampistas_requeridos:
            abort(400, message=f"Se requieren {mediocampistas_requeridos} mediocampistas titulares")
        if len(jugadores['delanteros']) != delanteros_requeridos:
            abort(400, message=f"Se requieren {delanteros_requeridos} delanteros titulares")
        if not jugadores.get('arquero'):
            abort(400, message="Se requiere 1 arquero titular")

        if not jugadores.get('arquero_suplente'):
            abort(400, message="Se requiere 1 arquero suplente")
        if not jugadores.get('defensor_suplente'):
            abort(400, message="Se requiere 1 defensor suplente")
        if not jugadores.get('mediocampista_suplente'):
            abort(400, message="Se requiere 1 mediocampista suplente")
        if not jugadores.get('delantero_suplente'):
            abort(400, message="Se requiere 1 delantero suplente")

        all_jugadores_ids = (
        jugadores['defensores'] + jugadores['mediocampistas'] +
        jugadores['delanteros'] + [jugadores['arquero']] +
        [jugadores['arquero_suplente'], jugadores['defensor_suplente'],
         jugadores['mediocampista_suplente'], jugadores['delantero_suplente']]
        )

        if len(all_jugadores_ids) != len(set(all_jugadores_ids)):
            abort(400, message="No se permiten jugadores repetidos")
        
        jugadores_db = JugadorModel.query.filter(JugadorModel.jugador_id.in_(all_jugadores_ids)).all()
        jugadores_dict = {jugador.jugador_id: jugador for jugador in jugadores_db}


        #podriamos modificar la tabla directamente y nos ahorrramos este paso
        posiciones_codificadas = {
            'arquero': 'ARQ',
            'defensores': 'DEF',
            'mediocampistas': 'VOL',
            'delanteros': 'DEL'
        }

        posiciones = {
            'arquero': [jugadores['arquero']] + [jugadores['arquero_suplente']],
            'defensores': jugadores['defensores'] + [jugadores['defensor_suplente']],
            'mediocampistas': jugadores['mediocampistas'] + [jugadores['mediocampista_suplente']],
            'delanteros': jugadores['delanteros'] + [jugadores['delantero_suplente']]
        }

        for posicion, ids in posiciones.items():
            codigo_posicion = posiciones_codificadas[posicion]  
            for jugador_id in ids:
                jugador = jugadores_dict.get(jugador_id)
                if not jugador:
                    abort(404, message=f"Jugador con ID {jugador_id} no encontrado")
                if jugador.posicion != codigo_posicion:
                    abort(400, message=f"El jugador {jugador_id} no es un {posicion}")

        nuevo_equipo = EquipoModel(
            usuario_id=args['usuario_id'],
            valor=15_000_000,  # TODO: Calcular el valor del equipo
            formacion=formacion,
            jugadores_id=jugadores
        )
        db.session.add(nuevo_equipo)
        db.session.commit()

        return nuevo_equipo, 201
