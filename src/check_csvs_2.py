import pandas as pd
import json

try:
    df_part = pd.read_csv('/app/dados/microdados_enem_2024/DADOS/PARTICIPANTES_2024.csv', sep=';', encoding='latin1', nrows=0)
    df_res = pd.read_csv('/app/dados/microdados_enem_2024/DADOS/RESULTADOS_2024.csv', sep=';', encoding='latin1', nrows=0)
    
    with open('/app/src/cols.json', 'w') as f:
        json.dump({
            "part": df_part.columns.tolist(),
            "res": df_res.columns.tolist()
        }, f, indent=2)
except Exception as e:
    with open('/app/src/cols.json', 'w') as f:
        f.write(str(e))
