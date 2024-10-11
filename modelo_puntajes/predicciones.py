import pandas as pd
from sklearn.base import BaseEstimator
from funciones import generar_predicciones
import joblib
import time

# TODO: ignore warnings
# TODO: que considere el resultado, habria que entrenar el modelo de nuevo
# TODO: si un jugador juega menos de x minutos dejar puntaje en nan
def computar_fecha(fecha: int, modelo: BaseEstimator):
    # Tabla de todos los partidos
    df = pd.read_html('https://fbref.com/en/comps/21/horario/Resultados-y-partidos-en-Liga-Profesional-Argentina')[0]

    # Tabla de todos los partidos con links
    links = pd.read_html('https://fbref.com/en/comps/21/horario/Resultados-y-partidos-en-Liga-Profesional-Argentina', extract_links= 'body')[0]

    fbref = 'https://fbref.com'

    df_fecha = df[df['Wk'] == fecha]

    for i in range(len(df_fecha)):
        df_fecha['Match Report'].iloc[i] = fbref + links['Match Report'].iloc[i][1]

    df_fecha['match'] = df_fecha['Home'] + ' - ' + df_fecha['Away']
    df_fecha = df_fecha[['match', 'Match Report']]

    predicciones = []
    for index, row in df_fecha.iterrows():
        url = row['Match Report']
        match = row['match']
        predicciones.append(generar_predicciones(url, match, modelo))
        time.sleep(10)
    
    df_fecha_concat = pd.concat(predicciones, ignore_index=True)

    return df_fecha_concat

if __name__ == '__main__':
    modelo = joblib.load('modelo_puntajes/modelos/primer_modelo.pkl')
    df_fecha = computar_fecha(1, modelo)
    print(df_fecha)
    df_fecha.to_csv('predicciones_fecha_1.csv', index=False)
