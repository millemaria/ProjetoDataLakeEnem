import json

notebook_path = '/app/notebooks/storytelling_enem.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the index of the spark.stop() cell and remove empty cells at the end
cells_to_keep = []
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and len(cell['source']) > 0 and 'spark.stop()' in ''.join(cell['source']):
        continue # remove spark stop for now
    if cell['cell_type'] == 'code' and len(cell['source']) == 0:
        continue # remove empty codes
    cells_to_keep.append(cell)

nb['cells'] = cells_to_keep

new_cells = [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Insight Visual 4: O Top 10 Estados na Redação (Excelência Acadêmica)\n",
    "\n",
    "A tabela `ranking_redacao_por_uf` da Camada Ouro permite visualizar facilmente o ranking de excelência entre os estados. Vamos observar o Top 10 de maior média em redação do ano mais recente presente no Data Lake."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "try:\n",
    "    # Utilizando o df_rk já carregado ou recarregando\n",
    "    if 'df_rk' not in locals():\n",
    "        df_rk = spark.read.parquet(pasta_ranking).toPandas()\n",
    "        df_rk[\"ano\"] = pd.to_numeric(df_rk[\"ano\"])\n",
    "    \n",
    "    ultimo_ano = df_rk[\"ano\"].max()\n",
    "    df_top10 = df_rk[df_rk[\"ano\"] == ultimo_ano].sort_values(by=\"MEDIA_REDACAO\", ascending=False).head(10)\n",
    "    \n",
    "    plt.figure(figsize=(12, 6))\n",
    "    sns.barplot(data=df_top10, x=\"MEDIA_REDACAO\", y=\"SG_UF_PROVA\", palette=\"mako\")\n",
    "    \n",
    "    plt.title(f\"Top 10 UFs com Maior Média de Redação em {ultimo_ano}\", fontsize=15)\n",
    "    plt.xlabel(\"Média de Redação\", fontsize=12)\n",
    "    plt.ylabel(\"UF\", fontsize=12)\n",
    "    for index, value in enumerate(df_top10['MEDIA_REDACAO']):\n",
    "        plt.text(value, index, f\" {value:.1f}\", va='center')\n",
    "    \n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "except Exception as e:\n",
    "    print(\"Falha ao plotar ranking Top 10:\", e)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Insight Visual 5: Inclusão e Diversidade – O Perfil Sociodemográfico\n",
    "\n",
    "A análise de representatividade é crucial para políticas públicas educacionais. Utilizando a tabela `distribuicao_perfil`, visualizamos como a diversidade de autodeclaração de Cor/Raça evoluiu no período."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "pasta_perfil = \"/app/data_lake/ouro/enem/distribuicao_perfil\"\n",
    "try:\n",
    "    df_pf = spark.read.parquet(pasta_perfil).toPandas()\n",
    "    df_pf[\"ano\"] = pd.to_numeric(df_pf[\"ano\"])\n",
    "    \n",
    "    # Mapeamento do Dicionário de Microdados do INEP\n",
    "    mapa_raca = {0: \"Não declarado\", 1: \"Branca\", 2: \"Preta\", 3: \"Parda\", 4: \"Amarela\", 5: \"Indígena\", 6: \"Não disp.\"}\n",
    "    df_pf[\"RACA_DESC\"] = df_pf[\"TP_COR_RACA\"].map(mapa_raca)\n",
    "    \n",
    "    df_raca = df_pf.groupby([\"ano\", \"RACA_DESC\"])[\"TOTAL_CANDIDATOS\"].sum().reset_index()\n",
    "    \n",
    "    plt.figure(figsize=(14, 7))\n",
    "    sns.lineplot(data=df_raca, x=\"ano\", y=\"TOTAL_CANDIDATOS\", hue=\"RACA_DESC\", marker=\"o\", linewidth=2.5)\n",
    "    \n",
    "    plt.title(\"Evolução da Participação por Autodeclaração de Cor/Raça\", fontsize=15)\n",
    "    plt.xlabel(\"Ano do Exame\", fontsize=12)\n",
    "    plt.ylabel(\"Total de Candidatos\", fontsize=12)\n",
    "    plt.xticks(df_raca[\"ano\"].unique())\n",
    "    plt.grid(True, linestyle=\"--\", alpha=0.3)\n",
    "    plt.legend(title=\"Cor / Raça\", bbox_to_anchor=(1.05, 1), loc=\"upper left\")\n",
    "    \n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "except Exception as e:\n",
    "    print(\"Falha ao carregar distribuição de perfil:\", e)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Encerramos a sessão Spark de forma segura ao final da análise no Jupyter.\n",
    "spark.stop()\n"
   ]
  }
]

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook atualizado com sucesso!")
