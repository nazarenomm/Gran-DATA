from app import app, db
from Puntaje.modelo_puntajes import ModeloPuntajes

class Puntaje(db.Model):
    __tablename__ = 'puntajes'
    id = db.Column(db.Integer, primary_key=True)
    jugador = db.Column(db.String(100), nullable=False)
    equipo = db.Column(db.String(30), nullable=False)
    puntaje = db.Column(db.Float)
    fecha = db.Column(db.Integer, nullable=False)

if __name__ == '__main__':
    modelo = ModeloPuntajes()
    # df_fecha = modelo.computar_fecha(1)
    
    import pandas as pd
    df_fecha = pd.read_csv('modelo_puntajes/data/predicciones/predicciones_fecha_1.csv')

    with app.app_context():
        db.create_all()
        for index, row in df_fecha.iterrows():
            nuevo_puntaje = Puntaje(jugador=row['jugador'], equipo=row['equipo'], puntaje=row['puntaje'], fecha=row['fecha'])
            db.session.add(nuevo_puntaje) 
        db.session.commit()