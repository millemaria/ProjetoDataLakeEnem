import pandas as pd

try:
    df_part = pd.read_csv('/app/dados/microdados_enem_2024/DADOS/PARTICIPANTES_2024.csv', sep=';', encoding='latin1', nrows=1)
    print("--- PARTICIPANTES_2024 ---")
    print(df_part.columns.tolist())
except Exception as e:
    print("Error part:", e)

try:
    df_res = pd.read_csv('/app/dados/microdados_enem_2024/DADOS/RESULTADOS_2024.csv', sep=';', encoding='latin1', nrows=1)
    print("--- RESULTADOS_2024 ---")
    print(df_res.columns.tolist())
except Exception as e:
    print("Error res:", e)
