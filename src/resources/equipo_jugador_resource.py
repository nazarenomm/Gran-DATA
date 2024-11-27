from flask_restx import Resource, fields, marshal_with
from models import EquipoJugadorModel, JugadorModel, EquipoModel
from flask_jwt_extended import jwt_required, get_jwt_identity

equipo_jugador_fields = {
    'equipo_id': fields.Integer,
    'usuario_id': fields.Integer,
    'precio': fields.Integer,  # Cambié de 'valor' a 'precio'
    'formacion': fields.String,
    'jugadores': fields.List(fields.Nested({
        'jugador_id': fields.Integer,
        'nombre': fields.String,
        'posicion': fields.String,
        'precio': fields.Integer,
        'estado': fields.String,
        'rol': fields.Integer
    }))
}
class EquipoJugadorResource(Resource):
    @jwt_required()
    @marshal_with(equipo_jugador_fields)
    def get(self):
        usuario_id = get_jwt_identity()  # Obtén el ID del usuario autenticado

        # Buscar el equipo asociado al usuario
        equipo = EquipoModel.query.filter_by(usuario_id=usuario_id).first()
        if not equipo:
            return {"message": "No se encontró un equipo para este usuario."}, 404

        # Obtener jugadores del equipo
        equipo_jugadores = EquipoJugadorModel.query.filter_by(equipo_id=equipo.equipo_id).all()
        jugadores = []
        valor_equipo = 0
        for ej in equipo_jugadores:
            jugador = JugadorModel.query.get(ej.jugador_id)
            valor_equipo += jugador.precio
            jugadores.append({
                "jugador_id": jugador.jugador_id,
                "nombre": jugador.nombre,
                "posicion": jugador.posicion,
                "precio": jugador.precio,
                "estado": jugador.estado,
                "rol": ej.rol_id  # Titular, suplente, o capitán
            })


        return {
            "equipo_id": equipo.equipo_id,
            "usuario_id": equipo.usuario_id,
            "precio": valor_equipo, 
            "formacion": equipo.formacion,
            "jugadores": jugadores
        }, 200

