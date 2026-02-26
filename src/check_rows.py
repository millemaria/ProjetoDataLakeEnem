import pandas as pd

try:
    df_part = pd.read_csv('/app/dados/microdados_enem_2024/DADOS/PARTICIPANTES_2024.csv', sep=';', encoding='latin1', nrows=5)
    df_res = pd.read_csv('/app/dados/microdados_enem_2024/DADOS/RESULTADOS_2024.csv', sep=';', encoding='latin1', nrows=5)
    
    print("--- PARTICIPANTES ---")
    print(df_part[['NU_INSCRICAO']].head())
    
    print("--- RESULTADOS ---")
    print(df_res[['NU_SEQUENCIAL']].head())
except Exception as e:
    print(str(e))
