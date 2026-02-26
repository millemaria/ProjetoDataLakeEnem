import pandas as pd

try:
    df_part = pd.read_csv('/app/dados/microdados_enem_2024/DADOS/PARTICIPANTES_2024.csv', sep=';', encoding='latin1', usecols=['NU_INSCRICAO'])
    print("Total Participantes:", len(df_part))
    
    df_res = pd.read_csv('/app/dados/microdados_enem_2024/DADOS/RESULTADOS_2024.csv', sep=';', encoding='latin1', usecols=['NU_SEQUENCIAL'])
    print("Total Resultados:", len(df_res))
except Exception as e:
    print(str(e))
