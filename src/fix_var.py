import json

notebook_path = '/app/notebooks/storytelling_enem.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        for i, line in enumerate(cell['source']):
            if line.strip() == 'try:' and 'df_rk' in ''.join(cell['source']):
                if not any('pasta_ranking =' in l for l in cell['source']):
                    cell['source'].insert(i, 'pasta_ranking = "/app/data_lake/ouro/enem/ranking_redacao_por_uf"\\n')
                break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
