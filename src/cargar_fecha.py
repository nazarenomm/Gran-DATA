from functools import reduce
import time
import numpy as np
from extensiones import db
from models import ClubModel, PartidoModel, RendimientoModel, JugadorModel
from app import app
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

def limpiar_tabla(tabla: pd.DataFrame, nombre_tabla: str) -> pd.DataFrame:
    to_keep_as_is_dict = {
        'home_standard': ['Unnamed', 'Performance', 'Expected', 'SCA', 'Carries'],
        'away_standard': ['Unnamed', 'Performance', 'Expected', 'SCA', 'Carries'],
        'home_pass': ['Unnamed'],
        'away_pass': ['Unnamed'],
        'home_pass_types': ['Unnamed', 'Pass Types', 'Corner Kicks', 'Outcomes'],
        'away_pass_types': ['Unnamed', 'Pass Types', 'Corner Kicks', 'Outcomes'],
        'home_defense': ['Unnamed'],
        'away_defense': ['Unnamed'],
        'home_possession': ['Unnamed'],
        'away_possession': ['Unnamed'],
        'home_misc': ['Unnamed', 'Performance'],
        'away_misc': ['Unnamed', 'Performance'],
        'home_gk': ['Unnamed', 'Shot Stopping'],
        'away_gk': ['Unnamed', 'Shot Stopping'],
    }
    
    to_keep_as_is = to_keep_as_is_dict.get(nombre_tabla, [])
    tabla.columns = [
        f'{c[0]}-{c[1]}' if all(x not in c[0] for x in to_keep_as_is) else c[1]
        for c in tabla.columns
    ]
    
    drop_columns_dict = {
        'home_standard': ['Touches', 'Blocks', 'Int', 'Tkl', 'CrdY', 'CrdR', 'xAG'],
        'away_standard': ['Touches', 'Blocks', 'Int', 'Tkl', 'CrdY', 'CrdR', 'xAG'],
        'home_pass': ['Total-Cmp', 'Total-Att', 'Total-Cmp%', 'Short-Cmp%', 'Medium-Cmp%', 'Long-Cmp%'],
        'away_pass': ['Total-Cmp', 'Total-Att', 'Total-Cmp%', 'Short-Cmp%', 'Medium-Cmp%', 'Long-Cmp%'],
        'home_pass_types': ['In', 'Out', 'Str', 'Cmp', 'Off', 'Blocks'],
        'away_pass_types': ['In', 'Out', 'Str', 'Cmp', 'Off', 'Blocks'],
        'home_defense': ['Tackles-Def 3rd', 'Tackles-Mid 3rd', 'Tackles-Att 3rd', 'Challenges-Tkl%', 'Tkl+Int'],
        'away_defense': ['Tackles-Def 3rd', 'Tackles-Mid 3rd', 'Tackles-Att 3rd', 'Challenges-Tkl%', 'Tkl+Int'],
        'home_possession': ['Touches-Touches', 'Touches-Live', 'Take-Ons-Succ%', 'Take-Ons-Tkld', 'Take-Ons-Tkld%'],
        'away_possession': ['Touches-Touches', 'Touches-Live', 'Take-Ons-Succ%', 'Take-Ons-Tkld', 'Take-Ons-Tkld%'],
        'home_misc': ['Crs', 'Int', 'TklW', 'Aerial Duels-Won%'],
        'away_misc': ['Crs', 'Int', 'TklW', 'Aerial Duels-Won%'],
        'home_gk': ['Save%', 'Launched-Cmp%', 'Passes-Launch%', 'Goal Kicks-Launch%', 'Crosses-Stp%'],
        'away_gk': ['Save%', 'Launched-Cmp%', 'Passes-Launch%', 'Goal Kicks-Launch%', 'Crosses-Stp%'],
    }
    
    # Eliminar las últimas 8 columnas para ciertas tablas
    if nombre_tabla in ['home_standard', 'away_standard']:
        tabla = tabla.iloc[:, :-8]
    
    # Eliminar columnas específicas
    drop_columns = drop_columns_dict.get(nombre_tabla, [])
    tabla.drop(columns=drop_columns, inplace=True, errors='ignore')
    
    return tabla

def rendimientos_partido(url, match, score, modelo) -> pd.DataFrame:
    dfs = pd.read_html(url)
        
    # Definir los nombres de las tablas a limpiar
    nombres_tablas = [
        'home_standard', 'home_pass', 'home_pass_types', 'home_defense', 
        'home_possession', 'home_misc', 'home_gk',
        'away_standard', 'away_pass', 'away_pass_types', 'away_defense', 
        'away_possession', 'away_misc', 'away_gk'
    ]
    
    # Limpiar las tablas
    tablas_clean = []
    for tabla, nombre_tabla in zip(dfs[3:17], nombres_tablas):
        tabla_limpia = limpiar_tabla(tabla, nombre_tabla)
        # Asignar el equipo
        if 'home' in nombre_tabla:
            tabla_limpia['match'] = match
            tabla_limpia['score'] = score
            tabla_limpia['team'] = match.split(' - ')[0]
            tabla_limpia['team_goals'] = int(score.split('–')[0])
            tabla_limpia['conceded_goals'] = int(score.split('–')[1])
            tabla_limpia['win'] = int(score.split('–')[0]) > int(score.split('–')[1])
            tabla_limpia['tie'] = int(score.split('–')[0]) == int(score.split('–')[1])
        else:
            tabla_limpia['match'] = match
            tabla_limpia['score'] = score
            tabla_limpia['team'] = match.split(' - ')[1]
            tabla_limpia['team_goals'] = int(score.split('–')[1])
            tabla_limpia['conceded_goals'] = int(score.split('–')[0])
            tabla_limpia['win'] = int(score.split('–')[1]) > int(score.split('–')[0])
            tabla_limpia['tie'] = int(score.split('–')[1]) == int(score.split('–')[0])

        # Eliminar la última fila si no es GK
        if nombre_tabla not in ['home_gk', 'away_gk']:
            tabla_limpia.drop(tabla_limpia.index[-1], inplace=True)
        tablas_clean.append(tabla_limpia)

    # Función para obtener la primera posición
    def primera_posicion(pos_str):
        if pd.isna(pos_str):
            return np.nan
        return pos_str.split(',')[0]

    for df in tablas_clean:
        if 'Pos' in df.columns:
            df['Pos'] = df['Pos'].apply(primera_posicion)
    
    # Mergeamos todas las tablas
    def merge_and_concat(tablas_clean, group_size=7) -> pd.DataFrame:
        merged_dfs = []
        for i in range(0, len(tablas_clean), group_size):
            group = tablas_clean[i:i + group_size]
            df_merged = reduce(
                lambda left, right: pd.merge(left, right, how='left', on=['Player', 'Nation', 'Age', 'team'], suffixes=('', '_dup')),
                group
            )
            df_merged = df_merged.loc[:, ~df_merged.columns.str.endswith('_dup')]
            merged_dfs.append(df_merged)
        df_final = pd.concat(merged_dfs, ignore_index=True)
        return df_final

    df_merged = merge_and_concat(tablas_clean, group_size=7)

    df_merged['Pos'] = df_merged['Pos'].replace({
        'RW': 'W',
        'LW': 'W',
        'LM': 'M',
        'RM': 'M',
        'LB': 'FB',
        'RB': 'FB',
    })
    df_merged.fillna(0, inplace=True)

    X_test = df_merged.copy()
    X_test.drop(columns=['Player', '#', 'Nation', 'team', 'Age', 'match', 'score'], inplace=True, errors='ignore')
    X_test = pd.get_dummies(X_test, columns=['Pos'], dtype=int)
    
    # Asegurar que todas las columnas del entrenamiento estén presentes (esto es porque hay algunas posiciones que no aparecen en todos los partidos)
    for col in modelo.feature_names_in_:
        if col not in X_test.columns:
            X_test[col] = 0
    X_test = X_test[modelo.feature_names_in_]

    df_merged['puntaje_modelo'] = modelo.predict(X_test)

    # asignar figura del partido
    df_merged['figura'] = df_merged['puntaje_modelo'] == df_merged['puntaje_modelo'].max()

    # formatear el puntaje
    df_merged['puntaje'] = np.clip(np.round(df_merged['puntaje_modelo']), 1, 10)

    # calculamos el puntaje total (el que cuenta en el juego)
    def calcular_puntaje_total(row):
        if row['Pos'] == 'FW':
            row['puntaje'] += (row['Gls']-row['PK'])*3 + row['Ast']
        elif row['Pos'] in ['W', 'AM']:
            row['puntaje'] += (row['Gls']-row['PK'])*4 + row['Ast']
        elif row['Pos'] in ['M', 'CM']:
            row['puntaje'] += (row['Gls']-row['PK'])*5 + row['Ast']
        elif row['Pos'] == 'DM':
            row['puntaje'] += (row['Gls']-row['PK'])*6 + row['Ast']*2
            if row['conceded_goals'] == 0:
                row['puntaje'] += 1
        elif row['Pos'] in ['FB', 'WB']:
            row['puntaje'] += (row['Gls']-row['PK'])*8 + row['Ast']*2
            if row['conceded_goals'] == 0:
                row['puntaje'] += 2
        elif row['Pos'] == 'CB':
            row['puntaje'] += (row['Gls']-row['PK'])*6 + row['Ast']*3
            if row['conceded_goals'] == 0:
                row['puntaje'] += 2
        elif row['Pos'] == 'GK':
            row['puntaje'] += (row['Gls']-row['PK'])*10 + row['Ast']*4
            if row['conceded_goals'] == 0:
                row['puntaje'] += 3
        else:
            raise ValueError(f'Posición {row["Pos"]} no reconocida')
        
        row['puntaje'] -=  row['CrdR']*4 + row['OG']*2 + (row['PKatt']-row['PK'])*2 + row['CrdY']*2

        if row['figura'] == True:
            row['puntaje'] += 4

        return row
    
    df_merged = df_merged.apply(calcular_puntaje_total, axis=1)

    df_merged.drop(columns=['#', 'Nation', 'Age'], inplace=True)

    return df_merged
    
def cargar_fecha(fecha:int, modelo) -> pd.DataFrame:
    URL = 'https://fbref.com/en/comps/21/schedule/Liga-Profesional-Argentina-Scores-and-Fixtures'

    df = pd.read_html(URL)[0]
    links = pd.read_html(URL, extract_links='body')[0]
    df_fecha = df[df['Wk'] == fecha]
    links_fecha = links[links['Wk'] == (f"{fecha}", None)]

    for i in range(len(df_fecha)):
        df_fecha['Match Report'].iloc[i] = 'https://fbref.com' + links_fecha['Match Report'].iloc[i][1]

    df_fecha['match'] = df_fecha['Home'] + ' - ' + df_fecha['Away']
    df_fecha = df_fecha[['match', 'Match Report', 'Score']]

    rendimientos:list[pd.DataFrame] = []

    for _, row in df_fecha.iterrows():
        url = row['Match Report']
        match = row['match']
        score = row['Score']
        rendimientos.append(rendimientos_partido(url, match, score, modelo))
        time.sleep(10)

    df_fecha_concat = pd.concat(rendimientos, ignore_index=True)

    df_fecha_concat['fecha'] = fecha
    
    return df_fecha_concat # dataframe de rendimientos, tiene equipo y partido, CAMBIAR POR IDs






if __name__ == '__main__':

    modelo = joblib.load('modelo_puntajes/modelos/primer_modelo.pkl')
    fecha = 2
    with app.app_context():
        try:
            rendimientos = pd.read_csv(f'modelo_puntajes/data/predicciones/rendimientos_fecha_{fecha}.csv')
        except FileNotFoundError:
            rendimientos = cargar_fecha(fecha, modelo)
            rendimientos.to_csv(f'modelo_puntajes/data/predicciones/rendimientos_fecha_{fecha}.csv', index=False)

        for _, row in rendimientos.iterrows():
            # cargamos partido
            local = row['match'].split(' - ')[0]
            visitante = row['match'].split(' - ')[1]

            partido = PartidoModel.query.filter_by(
                local_id=ClubModel.query.filter_by(nombre=local).first().club_id,
                visitante_id=ClubModel.query.filter_by(nombre=visitante).first().club_id,
                fecha=fecha
                ).first()
            
            partido.goles_local = row['score'].split('–')[0]
            partido.goles_visitante = row['score'].split('–')[1]
            
            partido_id = partido.partido_id
            
            # cargamos club
            club_id = ClubModel.query.filter_by(nombre=row['team']).first().club_id

            # cargamos jugador, si no esta en la db lo agregamos
            jugador = JugadorModel.query.filter_by(nombre=row['Player'], club_id=club_id).first()
            if not jugador:
                if row['Pos'] in ['FW', 'W']:
                    posicion = 'DEL'
                elif row['Pos'] in ['AM', 'M', 'CM', 'DM']:
                    posicion = 'VOL'
                elif row['Pos'] in ['FB', 'WB', 'CB']:
                    posicion = 'DEF'
                elif row['Pos'] == 'GK':
                    posicion = 'ARQ'
                nuevo_jugador = JugadorModel(nombre=row['Player'], club_id=club_id, precio=300_000, posicion=posicion)
                db.session.add(nuevo_jugador)
                db.session.commit()
                jugador = JugadorModel.query.filter_by(nombre=row['Player'], club_id=club_id).first()
            jugador_id = jugador.jugador_id
            
            nuevo_rendimiento = RendimientoModel(
                jugador_id=jugador_id,
                partido_id=partido_id,
                minutos_jugados=row['Min'],
                goles=row['Gls'],
                asistencias=row['Ast'],
                goles_penal=row['PK'],
                penales_ejecutados=row['PKatt'],
                remates=row['Sh'],
                remates_arco=row['SoT'],
                xG=row['xG'],
                npxG=row['npxG'],
                ocaciones_creadas=row['SCA'],
                goles_creados=row['GCA'],
                pases_cortos_completados=row['Short-Cmp'],
                pases_cortos_intentados=row['Short-Att'],
                pases_medios_completados=row['Medium-Cmp'],
                pases_medios_intentados=row['Medium-Att'],
                pases_largos_completados=row['Long-Cmp'],
                pases_largos_intentados=row['Long-Att'],
                xAG = row['xAG'],
                xA = row['xA'],
                pases_clave=row['KP'],
                pases_progresivos=row['PrgP'],
                pases_intentados=row['Att'],
                pases_filtrados=row['TB'],
                centros=row['Crs'],
                corners_ejecutados=row['CK'],
                entradas=row['Tackles-Tkl'],
                entradas_ganadas=row['Tackles-TklW'],
                bloqueos=row['Blocks-Blocks'],
                remates_bloqueados=row['Blocks-Sh'],
                pases_bloqueados=row['Blocks-Pass'],
                intercepciones=row['Int'],
                despejes=row['Clr'],
                errores_graves=row['Err'],
                gambetas_intentadas=row['Take-Ons-Att'],
                gambetas_completadas=row['Take-Ons-Succ'],
                traslados=row['Carries-Carries'],
                traslados_progresivos=row['Carries-PrgC'],
                tarjetas_amarillas=row['CrdY'],
                tarjetas_rojas=row['CrdR'],
                doble_amarilla=row['2CrdY'],
                faltas=row['Fls'],
                faltas_ganadas=row['Fld'],
                penales_ganados=row['PKwon'],
                penales_concedidos=row['PKcon'],
                goles_en_contra=row['OG'],
                recuperaciones=row['Recov'],
                duelos_aereos_ganados=row['Aerial Duels-Won'],
                duelos_aereos_perdidos=row['Aerial Duels-Lost'],
                remates_arco_recibidos=row['SoTA'],
                goles_recibidos=row['GA'],
                atajadas=row['Saves'],
                PSxG=row['PSxG'],
                centros_enfrentados=row['Crosses-Opp'],
                centros_atajados=row['Crosses-Stp'],
                puntaje=row['puntaje_modelo'],
                puntaje_total=row['puntaje']
                )
            db.session.add(nuevo_rendimiento)
            db.session.commit()