import zipfile
with zipfile.ZipFile('/app/dados/microdados_enem_2024.zip', 'r') as zip_ref:
    for name in zip_ref.namelist():
        if name.endswith('.csv') or name.endswith('.CSV'):
            print(name)
