import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

df = pd.read_csv('modelo_puntajes/data/training_data.csv')
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

lr = LinearRegression()

lr.fit(X, y)

joblib.dump(lr, 'modelo_puntajes/modelos/primer_modelo.pkl')