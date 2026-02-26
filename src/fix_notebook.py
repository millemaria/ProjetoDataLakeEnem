import json
import os

path = '/app/notebooks/storytelling_enem.ipynb'
with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 0: Markdown
nb['cells'][0]['source'] = [
    '# Storytelling da Evolução das Notas do ENEM\n',
    '\n',
    'Bem-vindo à análise preditiva baseada nos dados do nosso **Data Lake (Camada Ouro)**.\n',
    'Nestas visualizações, investigamos como o desempenho (médias de notas) dos candidatos nos Estados de todo o Brasil evoluiu ao longo do tempo.'
]

# Cell 2: Load Data
nb['cells'][2]['source'] = [
    'from pyspark.sql import SparkSession\n',
    'import matplotlib.pyplot as plt\n',
    'import seaborn as sns\n',
    'import pandas as pd\n',
    '\n',
    '# Inicializa a sessão Spark no contexto do Jupyter\n',
    'spark = SparkSession.builder \\\n',
    '    .appName(\"StorytellingENEM\") \\\n',
    '    .getOrCreate()\n',
    '\n',
    '# O caminho interno mapeado no container do Jupyter para a camada Ouro\n',
    'pasta_ouro = \"/app/data_lake/ouro/enem/media_notas_por_uf_ano\"\n',
    '\n',
    '# Lendo os dados já otimizados e agregados por UF e Ano do Parquet\n',
    'try:\n',
    '    df_ouro = spark.read.parquet(pasta_ouro)\n',
    '    # Convertendo para Pandas para plotagem\n',
    '    df_pd = df_ouro.toPandas()\n',
    '    df_pd[\"ano\"] = pd.to_numeric(df_pd[\"ano\"])\n',
    '    df_pd = df_pd.sort_values(by=[\"ano\", \"SG_UF_PROVA\"])\n',
    '    print(\"✅ Dados da Camada Ouro (Média de Notas por UF) carregados com sucesso!\")\n',
    '    display(df_pd.head())\n',
    'except Exception as e:\n',
    '    print(\"⚠️ Não foi possível carregar. Rode o pipeline Ouro antes.\\n\", e)\n',
    '    df_pd = pd.DataFrame()'
]

# Cell 4: Chart Redação
nb['cells'][4]['source'] = [
    'if not df_pd.empty and \"MEDIA_REDACAO\" in df_pd.columns:\n',
    '    plt.figure(figsize=(15, 6))\n',
    '    # Filtramos apenas as UFs do Sudeste para não poluir o gráfico\n',
    '    ufs_destaque = [\"SP\", \"RJ\", \"MG\", \"ES\"]\n',
    '    df_plot = df_pd[df_pd[\"SG_UF_PROVA\"].isin(ufs_destaque)]\n',
    '\n',
    '    sns.lineplot(\n',
    '        data=df_plot,\n',
    '        x=\"ano\",\n',
    '        y=\"MEDIA_REDACAO\",\n',
    '        hue=\"SG_UF_PROVA\",\n',
    '        marker=\"o\",\n',
    '        linewidth=2\n',
    '    )\n',
    '    plt.title(\"Evolução das Médias em Redação no Sudeste\", fontsize=15)\n',
    '    plt.xlabel(\"Ano do Exame\", fontsize=12)\n',
    '    plt.ylabel(\"Nota Média (Redação)\", fontsize=12)\n',
    '    plt.xticks(df_plot[\"ano\"].unique())\n',
    '    plt.grid(True, linestyle=\"--\", alpha=0.5)\n',
    '    plt.legend(title=\"UF\", bbox_to_anchor=(1.05, 1), loc=\"upper left\")\n',
    '    plt.tight_layout()\n',
    '    plt.show()'
]

# Cell 6: Chart Matemática
nb['cells'][6]['source'] = [
    'if not df_pd.empty and \"MEDIA_MT\" in df_pd.columns:\n',
    '    plt.figure(figsize=(15, 6))\n',
    '    ufs_destaque = [\"SP\", \"RJ\", \"MG\", \"ES\"]\n',
    '    df_plot = df_pd[df_pd[\"SG_UF_PROVA\"].isin(ufs_destaque)]\n',
    '\n',
    '    sns.barplot(\n',
    '        data=df_plot,\n',
    '        x=\"ano\",\n',
    '        y=\"MEDIA_MT\",\n',
    '        hue=\"SG_UF_PROVA\",\n',
    '        palette=\"viridis\"\n',
    '    )\n',
    '    plt.title(\"Comparações das Médias de Matemática por Ano (Sudeste)\", fontsize=15)\n',
    '    plt.xlabel(\"Ano do Exame\", fontsize=12)\n',
    '    plt.ylabel(\"Nota Média (Matemática)\", fontsize=12)\n',
    '    plt.legend(title=\"UF\", bbox_to_anchor=(1.05, 1), loc=\"upper left\")\n',
    '    plt.grid(axis=\"y\", linestyle=\"--\", alpha=0.5)\n',
    '    plt.tight_layout()\n',
    '    plt.show()'
]

# Read from distribution per mask
nb['cells'][8]['source'] = [
    '# Lendo base de Rankings da Camada Ouro para ver os Participantes por Ano\n',
    'pasta_ranking = \"/app/data_lake/ouro/enem/ranking_redacao_por_uf\"\n',
    'try:\n',
    '    df_rk = spark.read.parquet(pasta_ranking).toPandas()\n',
    '    df_rk[\"ano\"] = pd.to_numeric(df_rk[\"ano\"])\n',
    '    df_total_ano = df_rk.groupby(\"ano\")[\"TOTAL_PARTICIPANTES\"].sum().reset_index()\n',
    '    \n',
    '    plt.figure(figsize=(10, 5))\n',
    '    plt.fill_between(df_total_ano[\"ano\"], df_total_ano[\"TOTAL_PARTICIPANTES\"], color=\"#4C72B0\", alpha=0.3)\n',
    '    plt.plot(df_total_ano[\"ano\"], df_total_ano[\"TOTAL_PARTICIPANTES\"], color=\"#4C72B0\", marker=\"D\", linewidth=2.5)\n',
    '    \n',
    '    plt.title(\"Retomada: Total de Participantes no ENEM Brasil\", fontsize=15)\n',
    '    plt.xlabel(\"Ano\", fontsize=12)\n',
    '    plt.ylabel(\"Participantes com Redação > 0\", fontsize=12)\n',
    '    plt.xticks(df_total_ano[\"ano\"].unique())\n',
    '    plt.grid(True, linestyle=\"-.\", alpha=0.5)\n',
    '    plt.tight_layout()\n',
    '    plt.show()\n',
    'except Exception as e:\n',
    '    print(\"Falha ao carregar ranking da camada Ouro:\", e)'
]

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print('Notebook atualizado.')
