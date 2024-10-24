from typing import Optional
import joblib
import pandas as pd
import numpy as np
from functools import reduce
from sklearn.linear_model import LinearRegression
import time
import warnings
warnings.filterwarnings("ignore")

# TODO: si un jugador juega menos de x minutos dejar puntaje en nan
# TODO: guardar la data de los rendimientos en la base de datos
# TODO: singleton ??? en lugar de cargarlo con joblib
# TODO: si un jugador no está en la base de datos, agregarlo

URL = 'https://fbref.com/en/comps/21/horario/Resultados-y-partidos-en-Liga-Profesional-Argentina'
TRAINING_DATA = 'modelo_puntajes/data/training_data.csv'

class ModeloPuntajes:
    NUM_MODELO = 1

    def __init__(self, modelo_path: Optional[str]='modelo_puntajes/modelos/primer_modelo.pkl'):
        if modelo_path:
            self.modelo = joblib.load(modelo_path)
        else:
            df = pd.read_csv(TRAINING_DATA)
            df.dropna(subset=['rating'], inplace=True)

            df['Pos'].replace({'RW': 'W',
                                'LW': 'W',
                                'LM': 'M',
                                'RM': 'M',
                                'LB': 'FB',
                                'RB': 'FB',
                                }, inplace=True)
            
            X = df.drop(['rating', 'player', '#', 'Nation', 'Age', 'team', 'match'], axis=1)
            y = df['rating']

            X.fillna(0, inplace=True)
            X = pd.get_dummies(X, columns=['Pos'], dtype=int)

            modelo = LinearRegression()

            modelo.fit(X, y)

            joblib.dump(modelo, f'modelo_puntajes/modelos/modelo_{self.NUM_MODELO}.pkl')

            self.NUM_MODELO += 1
    
    def computar_fecha(self, fecha: int) -> pd.DataFrame:
        # Tabla de todos los partidos
        df = pd.read_html(URL)[0]

        # Tabla de todos los partidos con links al reporte
        links = pd.read_html(URL, extract_links='body')[0]

        fbref = 'https://fbref.com'

        df_fecha = df[df['Wk'] == fecha]
        links_fecha = links[links['Wk'] == (f"{fecha}", None)]

        for i in range(len(df_fecha)):
            df_fecha['Match Report'].iloc[i] = fbref + links_fecha['Match Report'].iloc[i][1]

        df_fecha['match'] = df_fecha['Home'] + ' - ' + df_fecha['Away']
        df_fecha = df_fecha[['match', 'Match Report', 'Score']]

        predicciones = []
        for index, row in df_fecha.iterrows():
            url = row['Match Report']
            match = row['match']
            score = row['Score']
            predicciones.append(self._predict(url, match, score))
            time.sleep(10)
        
        df_fecha_concat = pd.concat(predicciones, ignore_index=True)

        df_fecha_concat['fecha'] = fecha

        df_fecha_concat = df_fecha_concat[['fecha', 'Player', 'team', 'Rating']]

        df_fecha_concat.rename(columns={'team': 'equipo', 'Rating': 'puntaje', 'Player': 'jugador'}, inplace=True)
        
        return df_fecha_concat

    def _limpiar_tabla(self, tabla: pd.DataFrame, nombre_tabla: str) -> pd.DataFrame:
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

    def _predict(self, url: str, match: str, score: str) -> pd.DataFrame:
        # Leer las tablas de la URL
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
            tabla_limpia = self._limpiar_tabla(tabla, nombre_tabla)
            # Asignar el equipo
            if 'home' in nombre_tabla:
                tabla_limpia['team'] = match.split(' - ')[0]
                tabla_limpia['team_goals'] = int(score.split('–')[0])
                tabla_limpia['conceded_goals'] = int(score.split('–')[1])
                tabla_limpia['win'] = int(score.split('–')[0]) > int(score.split('–')[1])
                tabla_limpia['tie'] = int(score.split('–')[0]) == int(score.split('–')[1])
            else:
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
        
        # Combinar las tablas
        def merge_and_concat(tablas_clean, group_size=7):
            merged_dfs = []
            for i in range(0, len(tablas_clean), group_size):
                group = tablas_clean[i:i + group_size]
                df_merged = reduce(
                    lambda left, right: pd.merge(left, right, how='left', on=['Player', 'Nation', 'Age', 'team'], suffixes=('', '_dup')),
                    group
                )
                # Eliminar columnas duplicadas
                df_merged = df_merged.loc[:, ~df_merged.columns.str.endswith('_dup')]
                merged_dfs.append(df_merged)
            # Concatenar todos los DataFrames
            df_final = pd.concat(merged_dfs, ignore_index=True)
            return df_final
        
        df_merged = merge_and_concat(tablas_clean, group_size=7)
        
        # Reemplazar posiciones
        df_merged['Pos'] = df_merged['Pos'].replace({
            'RW': 'W',
            'LW': 'W',
            'LM': 'M',
            'RM': 'M',
            'LB': 'FB',
            'RB': 'FB',
        })
        
        # Preparar los datos para la predicción
        X_test = df_merged.copy()
        X_test.drop(columns=['Player', '#', 'Nation', 'team', 'Age'], inplace=True, errors='ignore')
        X_test.fillna(0, inplace=True)
        X_test = pd.get_dummies(X_test, columns=['Pos'], dtype=int)
        
        # Asegurar que todas las columnas del entrenamiento estén presentes (esto es porque hay algunas posiciones que no aparecen en todos los partidos)
        for col in self.modelo.feature_names_in_:
            if col not in X_test.columns:
                X_test[col] = 0
        X_test = X_test[self.modelo.feature_names_in_]
        
        # Realizar las predicciones
        df_merged['Rating'] = self.modelo.predict(X_test)
        
        # Crear el DataFrame de predicciones
        predicciones = df_merged[['Player', 'team', 'Rating']].sort_values('Rating', ascending=False).reset_index(drop=True)
        
        return predicciones