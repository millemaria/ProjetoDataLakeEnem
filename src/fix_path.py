import json

notebook_path = '/app/notebooks/storytelling_enem.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        for i, line in enumerate(cell['source']):
            if line.strip() == 'ranking_redacao_por_uf = "/app/data_lake/ouro/enem/media_notas_por_uf_ano.parquet"\\n' or line.strip() == 'ranking_redacao_por_uf = "/app/data_lake/ouro/enem/media_notas_por_uf_ano.parquet"':
                cell['source'][i] = line.replace('media_notas_por_uf_ano.parquet', 'ranking_redacao_por_uf')

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
