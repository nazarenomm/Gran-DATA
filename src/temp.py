import pandas as pd
import numpy as np

df = pd.DataFrame({'a': [1.2, 2.0, 3.6], 'b': ['cambiar', 'no cambiar', 'cambiar']})
df['a_1'] = np.clip(np.round(df['a']), 2, 3)

def sumar(row):
    if row['b'] == 'cambiar':
        row['a_1'] += 4
    return row

df = df.apply(sumar, axis=1)
print(df)