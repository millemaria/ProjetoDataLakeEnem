import csv
import os

path_part = '/app/dados/microdados_enem_2024/DADOS/PARTICIPANTES_2024.csv'
path_res = '/app/dados/microdados_enem_2024/DADOS/RESULTADOS_2024.csv'
path_out = '/app/dados/microdados_enem_2024/DADOS/MICRODADOS_ENEM_2024.csv'

print(f"Juntando {path_part} e {path_res} para {path_out}...")

try:
    with open(path_part, 'r', encoding='latin1') as f_part, \
         open(path_res, 'r', encoding='latin1') as f_res, \
         open(path_out, 'w', encoding='latin1', newline='') as f_out:
         
        reader_part = csv.reader(f_part, delimiter=';')
        reader_res = csv.reader(f_res, delimiter=';')
        writer = csv.writer(f_out, delimiter=';')
        
        # Read headers
        header_part = next(reader_part)
        header_res = next(reader_res)
        
        # Find columns in res that are not in part to avoid duplication
        # Or just select columns we want to keep from res
        # Actually, let's keep all from part, and only new ones from res
        res_indices_to_keep = []
        for i, col in enumerate(header_res):
            if col not in header_part:
                res_indices_to_keep.append(i)
                
        new_header = header_part + [header_res[i] for i in res_indices_to_keep]
        writer.writerow(new_header)
        
        count = 0
        for row_part in reader_part:
            row_res = next(reader_res)
            new_row = row_part + [row_res[i] for i in res_indices_to_keep]
            writer.writerow(new_row)
            count += 1
            if count % 500000 == 0:
                print(f"  {count} linhas processadas...")
                
    print(f"Sucesso! {count} linhas unidas.")
except Exception as e:
    print("Erro durante a junção:", e)
