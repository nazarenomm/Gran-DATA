from extensiones import db
from models import ClubModel, EstadoModel, FormacionModel, JugadorModel, PartidoModel, RolModel, RolesUsuarioModel
from app import app
import pandas as pd

URL = 'https://fbref.com/en/comps/21/schedule/Liga-Profesional-Argentina-Scores-and-Fixtures'

def cargar_club(club):
    if not ClubModel.query.filter_by(nombre=club).first():
        club_model = ClubModel(nombre=club, puntos=0,
                               partidos_jugados=0, partidos_ganados=0,
                               partidos_empatados=0, partidos_perdidos=0,
                               goles_favor=0, goles_contra=0)
        db.session.add(club_model)
    db.session.commit()

def cargar_estados():
    estados = [
        'Posible Titular',
        'Habilitado',
        'Lesionado',
        'Suspendido',
        'Duda',
        'No Juega'
    ]
    for estado in estados:
        if not EstadoModel.query.filter_by(estado=estado).first():
            estado_model = EstadoModel(estado=estado)
            db.session.add(estado_model)
    db.session.commit()

def cargar_partidos():
    df = pd.read_html(URL)[0]
    df = df.dropna(subset=['Home', 'Away'])
    
    for index, row in df.iterrows():
        try:
            local_id = db.session.query(ClubModel.club_id).filter_by(nombre=row['Home']).first()[0]
            visitante_id = db.session.query(ClubModel.club_id).filter_by(nombre=row['Away']).first()[0]

            partido = PartidoModel(local_id=local_id, visitante_id=visitante_id, fecha=row['Wk'])
            db.session.add(partido)
        except Exception as e:
            print(f"Error al procesar la fila: {index}. Error: {e}")

    db.session.commit()

def agregar_formacion(formacion: str) -> None:
    lista_formacion = formacion.split('-')
    if not len(lista_formacion) == 3:
        raise ValueError('La formación debe tener 3 números separados por guiones')
    if not FormacionModel.query.filter_by(formacion=formacion).first():
        formacion_model = FormacionModel(formacion=formacion, defensores=int(lista_formacion[0]),
                                   mediocampistas=int(lista_formacion[1]), delanteros=int(lista_formacion[2]))
        db.session.add(formacion_model)
    db.session.commit()

def cargar_jugador(jugador):
    club = ClubModel.query.filter_by(nombre=jugador['Equipo']).first()
    club_id = club.club_id if club else None
    if not JugadorModel.query.filter_by(nombre=jugador['Jugador'], club_id=club_id).first():
        jugador_model = JugadorModel(club_id=club_id, nombre=jugador['Jugador'],
                                     precio=jugador['Precio'], posicion=jugador['Pos'], estado=jugador['Estado'],)
        db.session.add(jugador_model)
    db.session.commit()

def cargar_roles():
    roles = ['titular', 'suplente', 'capitan']
    for rol in roles:
        if not RolModel.query.filter_by(rol=rol).first():
            rol_model = RolModel(rol=rol)
            db.session.add(rol_model)
    db.session.commit()

def cargar_usuario_roles_iniciales():
    if not RolesUsuarioModel.query.first():
        roles = [RolesUsuarioModel(nombre="Usuario"), RolesUsuarioModel(nombre="Admin")]
        db.session.bulk_save_objects(roles)
        db.session.commit()



if __name__ == '__main__':
    jugadores = pd.read_csv('services/modelo_puntajes/data/jugadores.csv')
    #jugadores = pd.read_csv('modelo_puntajes/data/jugadores.csv')
    clubes = jugadores['Equipo'].unique()
    formaciones = ['4-4-2', '4-3-3', '3-4-3', '4-5-1', '3-5-2', '5-3-2', '3-3-4', '4-2-4', '5-2-3']

    with app.app_context():
        db.create_all()
        
        for club in clubes:
            cargar_club(club)

        cargar_estados()
        cargar_partidos()

        for formacion in formaciones:
            agregar_formacion(formacion)

        for index, jugador in jugadores.iterrows():
            cargar_jugador(jugador)
        
        cargar_roles()

        cargar_usuario_roles_iniciales()
