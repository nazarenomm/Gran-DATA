from flask_restx import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import EquipoJugadorModel, EquipoModel, FormacionModel, JugadorModel, RolModel, UsuarioModel
from extensiones import db, equipo_ns
from services import fecha

PRESUPUESTO = 70_000_000

equipo_post_args = reqparse.RequestParser()
equipo_post_args.add_argument("usuario_id", type=int, help="Usuario ID Requerido", required=True)
equipo_post_args.add_argument("formacion", type=str, help="Formación Requerida", required=True)
equipo_post_args.add_argument("jugadores_id", type=dict, help="Jugadores Requeridos", required=True)

equipo_patch_args = reqparse.RequestParser()
equipo_patch_args.add_argument("accion", type=str, help="Accion requerida", required= True) # transferencia o cambio titular por suplente
equipo_patch_args.add_argument("jugador_entrante_id", type=int, help="Jugador Entrante ID Requerido", required= False)
equipo_patch_args.add_argument("jugador_saliente_id", type=int, help="Jugador Saliente ID Requerido", required= False)
equipo_patch_args.add_argument("jugador_capitan_id", type=int, help="Jugador Saliente ID Requerido", required= False)

equipo_fields = {
    'equipo_id': fields.Integer,
    'usuario_id': fields.Integer,
    'valor': fields.Integer,
    'formacion': fields.String,
}

@equipo_ns.route('/<int:equipo_id>')
class EquipoResource(Resource):
    @equipo_ns.doc(params={'equipo_id': 'ID del equipo'}, responses={200: 'OK', 404: 'Equipo no encontrado'})
    @jwt_required()
    @marshal_with(equipo_fields)
    def get(self, equipo_id=None):  # `equipo_id` es opcional
        usuario_id = get_jwt_identity()
        # Buscar el usuario autenticado
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404

        # Si `equipo_id` está presente, buscar equipo por ID, de lo contrario buscar por usuario
        if equipo_id:
            equipo = EquipoModel.query.filter_by(equipo_id=equipo_id, usuario_id=usuario_id).first()
            if not equipo:
                return {"message": "Equipo no encontrado o no pertenece al usuario"}, 404
        else:
            equipo = EquipoModel.query.filter_by(usuario_id=usuario_id).first()
            if not equipo:
                return {"equipo": False}, 200
        # Serializar respuesta
        return {
            "equipo_id": equipo.equipo_id,
            "usuario_id": equipo.usuario_id,
            "valor": equipo.valor,
            "formacion": equipo.formacion
        }, 200
    
    @equipo_ns.doc(params={'equipo_id': 'ID del equipo'}, responses={200: 'OK', 404: 'Equipo no encontrado'})
    @jwt_required()
    def delete(self, equipo_id):
        equipo = EquipoModel.query.filter_by(equipo_id=equipo_id).first()
        if not equipo:
            abort(404, message="Equipo no encontrado")

        jugadores = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id).all()
        for jugador in jugadores:
            db.session.delete(jugador)
            
        db.session.delete(equipo)
        db.session.commit()
        return {"message": "Equipo eliminado"}, 200
    
    @equipo_ns.doc(params={'equipo_id': 'ID del equipo'}, responses={200: 'OK', 400: 'Error de validación', 404: 'Equipo no encontrado'})
    @equipo_ns.expect(equipo_patch_args)
    def patch(self, equipo_id):
        if fecha.verificar_veda():
            abort(400, message="Estamos en veda")

        args = equipo_patch_args.parse_args()

        equipo = EquipoModel.query.filter_by(equipo_id=equipo_id).first()
        if not equipo:
            abort(404, message="Equipo no encontrado")
        
        jugador_entrante_id = None
        jugador_saliente_id = None
        jugador_capitan_id = None
        
        accion = args['accion']
        if accion != 'cambio capitan':
            jugador_entrante_id = args['jugador_entrante_id']
            jugador_saliente_id = args['jugador_saliente_id']

            jugador_entrante = JugadorModel.query.filter_by(jugador_id=jugador_entrante_id).first()
            jugador_saliente = JugadorModel.query.filter_by(jugador_id=jugador_saliente_id).first()
        else:
            jugador_capitan_id = args['jugador_capitan_id']
        if accion == 'transferencia':           
        
            if not jugador_entrante:
                abort(404, message="Jugador Entrante no encontrado")
            if not jugador_saliente:
                abort(404, message="Jugador Saliente no encontrado")

            if not (jugador_entrante_id and jugador_saliente_id):
                abort(400, message="Se requieren los IDs de los jugadores")
            equipo_jugador_saliente = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, jugador_id=jugador_saliente_id).first()
            if not equipo_jugador_saliente:
                abort(404, message="Jugador Saliente no encontrado en el equipo")

            equipo_jugador_entrante = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, jugador_id=jugador_entrante_id).first()
            if equipo_jugador_entrante:
                abort(400, message="Jugador Entrante ya pertenece al equipo")

            # chequear el presupuesto
            valor_equipo = equipo.valor
            valor_jugador_entrante = jugador_entrante.precio
            valor_jugador_saliente = jugador_saliente.precio
            if valor_equipo - valor_jugador_saliente + valor_jugador_entrante > PRESUPUESTO:
                abort(400, message="El valor total del equipo supera el presupuesto")

            # chequear que el jugador entrante tenga la misma posición que el jugador saliente, si no cambiar la formacion del equipo si hay una formacion posible
            formacion = FormacionModel.query.filter_by(formacion=equipo.formacion).first()
            cantidad_defensores = formacion.defensores
            cantidad_mediocampistas = formacion.mediocampistas
            cantidad_delanteros = formacion.delanteros

            if jugador_saliente.posicion != jugador_entrante.posicion:
                if jugador_saliente.posicion == 'ARQ' or jugador_entrante.posicion == 'ARQ':
                    abort(400, message="No se puede cambiar un arquero por un jugador de campo")   

                elif jugador_saliente.posicion == 'DEF':
                    if jugador_entrante.posicion == 'VOL':
                        nueva_formacion = FormacionModel.query.filter_by(
                            defensores=cantidad_defensores-1,
                            mediocampistas=cantidad_mediocampistas+1,
                            delanteros=cantidad_delanteros
                            ).first()
                    elif jugador_entrante.posicion == 'DEL':
                        nueva_formacion = FormacionModel.query.filter_by(
                            defensores=cantidad_defensores-1,
                            mediocampistas=cantidad_mediocampistas,
                            delanteros=cantidad_delanteros+1
                            ).first()
                        
                elif jugador_saliente.posicion == 'VOL':
                    if jugador_entrante.posicion == 'DEF':
                        nueva_formacion = FormacionModel.query.filter_by(
                            defensores=cantidad_defensores+1,
                            mediocampistas=cantidad_mediocampistas-1,
                            delanteros=cantidad_delanteros
                            ).first()
                    elif jugador_entrante.posicion == 'DEL':
                        nueva_formacion = FormacionModel.query.filter_by(
                            defensores=cantidad_defensores,
                            mediocampistas=cantidad_mediocampistas-1,
                            delanteros=cantidad_delanteros+1
                            ).first()
                        
                elif jugador_saliente.posicion == 'DEL':
                    if jugador_entrante.posicion == 'DEF':
                        nueva_formacion = FormacionModel.query.filter_by(
                            defensores=cantidad_defensores+1,
                            mediocampistas=cantidad_mediocampistas,
                            delanteros=cantidad_delanteros-1
                            ).first()
                    elif jugador_entrante.posicion == 'VOL':
                        nueva_formacion = FormacionModel.query.filter_by(
                            defensores=cantidad_defensores,
                            mediocampistas=cantidad_mediocampistas+1,
                            delanteros=cantidad_delanteros-1
                            ).first()
                
                if not nueva_formacion:
                    abort(400, message="No hay formación posible para hacer la transferencia")
                
                equipo.formacion = nueva_formacion.formacion

            # se cambia el jugador saliente por el entrante en la tabla equipo_jugador, sin cambiar el rol
            equipo_jugador_saliente.jugador_id = jugador_entrante_id

        elif accion == 'cambio':
            if jugador_entrante.posicion != jugador_saliente.posicion:
                abort(400, message="Los jugadores deben tener la misma posición para hacer el cambio")

            rol_suplente_id = RolModel.query.filter_by(rol='suplente').first().rol_id
            equipo_jugador_entrante = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, jugador_id=jugador_entrante_id, rol_id=rol_suplente_id).first()
            if not equipo_jugador_entrante:
                abort(404, message="Jugador Entrante no encontrado en el equipo suplente")
            
            rol_titular_id = RolModel.query.filter_by(rol='titular').first().rol_id
            equipo_jugador_saliente = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, jugador_id=jugador_saliente_id, rol_id=rol_titular_id).first()
            if not equipo_jugador_saliente:
                rol_capitan_id = RolModel.query.filter_by(rol='capitan').first().rol_id
                equipo_jugador_saliente = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, jugador_id=jugador_saliente_id, rol_id=rol_capitan_id).first()
                if not equipo_jugador_saliente:
                    abort(404, message="Jugador Saliente no encontrado en el equipo titular")
            
            # se intercambian los roles de los jugadores, para no hardcodear los rol_id
            # si el jugador saliente es el capitán, el jugador entrante pasa a serlo
            equipo_jugador_entrante.rol_id, equipo_jugador_saliente.rol_id = equipo_jugador_saliente.rol_id, equipo_jugador_entrante.rol_id

        elif accion == 'cambio capitan':
            rol_titular_id = RolModel.query.filter_by(rol='titular').first().rol_id
            equipo_capitan_entrante = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, jugador_id=jugador_capitan_id, rol_id=rol_titular_id).first()
            print(equipo_capitan_entrante)
            if not equipo_capitan_entrante:
                abort(404, message="Jugador a capitanear no encontrado en el equipo titular o ya es capitan")	

            rol_capitan_id = RolModel.query.filter_by(rol='capitan').first().rol_id
            equipo_capitan_saliente = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, rol_id=rol_capitan_id).first()
            if not equipo_capitan_saliente:
                abort(404, message="Capitan no encontrado")

            equipo_capitan_entrante.rol_id, equipo_capitan_saliente.rol_id = equipo_capitan_saliente.rol_id, equipo_capitan_entrante.rol_id

        else:
            abort(400, message="Accion no reconocida")
        
        db.session.commit()
        return {"message": "cambio realizado"}, 200
    
@equipo_ns.route('/')
class EquipoPostResource(Resource):
    @equipo_ns.doc(params={'equipo_id': 'ID del equipo'}, responses={201: 'Creado', 400: 'Error de validación'})
    @equipo_ns.expect(equipo_post_args)
    @marshal_with(equipo_fields)
    @jwt_required()
    def post(self):
        if fecha.verificar_veda():
            abort(400, message="Estamos en veda")
            
        args = equipo_post_args.parse_args()
        usuario_id = get_jwt_identity()
        
        equipo_existente = EquipoModel.query.filter_by(usuario_id=usuario_id).first()
        if equipo_existente:
            abort(400, message="Ya existe un equipo para este usuario")

        # Validar la formación
        formacion = args['formacion']
        formacion_model = FormacionModel.query.filter_by(formacion=formacion).first()
        if not formacion_model:
            abort(404, message="Formación no encontrada")

        delanteros_requeridos = formacion_model.delanteros
        mediocampistas_requeridos = formacion_model.mediocampistas
        defensores_requeridos = formacion_model.defensores

        jugadores = args['jugadores_id']

        # Validaciones de la cantidad de jugadores
        titulares = JugadorModel.query.filter(JugadorModel.jugador_id.in_(jugadores['titulares'])).all()
        suplentes = JugadorModel.query.filter(JugadorModel.jugador_id.in_(jugadores['suplentes'])).all()

        arqueros = [jugador for jugador in titulares if jugador.posicion == 'ARQ']
        defensores = [jugador for jugador in titulares if jugador.posicion == 'DEF']
        mediocampistas = [jugador for jugador in titulares if jugador.posicion == 'VOL']
        delanteros = [jugador for jugador in titulares if jugador.posicion == 'DEL']

        arqueros_suplentes = [jugador for jugador in suplentes if jugador.posicion == 'ARQ']
        defensores_suplentes = [jugador for jugador in suplentes if jugador.posicion == 'DEF']
        mediocampistas_suplentes = [jugador for jugador in suplentes if jugador.posicion == 'VOL']
        delanteros_suplentes = [jugador for jugador in suplentes if jugador.posicion == 'DEL']

        if len(titulares) != 11:
            abort(400, message="Se requieren 11 jugadores titulares")
        elif len(suplentes) != 4:
            abort(400, message="Cantidad de jugadores suplentes incorrecta")
        elif jugadores.get('capitan') is None:
            abort(400, message="Se requiere un capitán")
        elif jugadores['capitan'] not in jugadores['titulares']:
            abort(400, message="El capitán debe ser un jugador titular")
        elif len(defensores) != defensores_requeridos:
            abort(400, message=f"Se requieren {defensores_requeridos} defensores titulares")
        elif len(mediocampistas) != mediocampistas_requeridos:
            abort(400, message=f"Se requieren {mediocampistas_requeridos} mediocampistas titulares")
        elif len(delanteros) != delanteros_requeridos:
            abort(400, message=f"Se requieren {delanteros_requeridos} delanteros titulares")
        elif len(arqueros) != 1:
            abort(400, message="Se requiere 1 arquero titular")
        elif len(arqueros_suplentes) != 1:
            abort(400, message="Se requiere 1 arquero suplente")
        elif len(defensores_suplentes) != 1:
            abort(400, message="Se requiere 1 defensor suplente")
        elif len(mediocampistas_suplentes) != 1:
            abort(400, message="Se requiere 1 mediocampista suplente")
        elif len(delanteros_suplentes) != 1:
            abort(400, message="Se requiere 1 delantero suplente")
    
        # Validar jugadores duplicados
        all_jugadores_ids = jugadores['titulares'] + jugadores['suplentes']

        if len(all_jugadores_ids) != len(set(all_jugadores_ids)):
            abort(400, message="No se permiten jugadores repetidos")

        # Verificar que todos los jugadores existen en la base de datos
        jugadores_db = JugadorModel.query.filter(JugadorModel.jugador_id.in_(all_jugadores_ids)).all()
        if len(jugadores_db) != len(all_jugadores_ids):
            abort(404, message="Uno o más jugadores no encontrados") # TODO: Mostrar los jugadores no encontrados
        
        # Calcular el valor total del equipo
        valor_total = sum(jugador.precio for jugador in jugadores_db)
        if valor_total > PRESUPUESTO:
            abort(400, message="El valor total del equipo supera el presupuesto")

        # Crear el nuevo equipo
        nuevo_equipo = EquipoModel(
            usuario_id=usuario_id,
            valor=valor_total,
            formacion=formacion
        )
        db.session.add(nuevo_equipo)

        # Agregar jugadores a la tabla equipo_jugador
        for rol, jugadores_ids in [('titular', jugadores['titulares']), ('suplente', jugadores['suplentes'])]:
            for jugador_id in jugadores_ids:
                if jugador_id == jugadores['capitan']:
                    rol_id = RolModel.query.filter_by(rol='capitan').first().rol_id
                else:
                    rol_id = RolModel.query.filter_by(rol=rol).first().rol_id
                equipo_jugador = EquipoJugadorModel(
                    equipo_id=nuevo_equipo.equipo_id,
                    jugador_id=jugador_id,
                    rol_id=rol_id
                )
                db.session.add(equipo_jugador)

        db.session.commit()
        return nuevo_equipo, 201
    