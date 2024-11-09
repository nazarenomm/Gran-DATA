import pandas as pd
from extensiones import db
from models import ClubModel, PartidoModel
from app import app

URL = 'https://fbref.com/en/comps/21/schedule/Liga-Profesional-Argentina-Scores-and-Fixtures'

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

if __name__ == '__main__':
    with app.app_context():
        cargar_partidos()
