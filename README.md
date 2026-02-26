# 📊 Data Lake ENEM: Pipeline de Engenharia de Dados com Apache Spark

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Apache Spark](https://img.shields.io/badge/apache%20spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

Este projeto implementa uma arquitetura robusta de **Data Lake local** utilizando contêineres Docker para orquestrar a extração, processamento e análise dos microdados do ENEM (Exame Nacional do Ensino Médio). 

O ambiente é 100% isolado, idempotente e reproduzível, trazendo o poder do Apache Spark (PySpark) para lidar com volumetria de Big Data (arquivos CSVs de múltiplos gigabytes) convertendo-os em formatos colunares altamente otimizados.

---

## 🏗️ Arquitetura do Projeto

A solução foi projetada em duas frentes de serviço (rodando no Ubuntu via Docker):

1. **Pipeline de Engenharia (`spark`):** Uma esteira autônoma que extrai os dados brutos e os converte em camadas estruturadas (Bronze e Prata) do Data Lake.
2. **Laboratório Analítico (`jupyter`):** Um ambiente interativo Jupyter Notebook para acesso aos dados refinados via `pandas` e `pyarrow`, sem consumir memória excessiva.

### Camadas do Data Lake (Medallion Architecture)
* **Raw (Bruto):** Arquivos `.zip` originais na pasta `dados/`.
* **Bronze:** Dados ingeridos e convertidos de formato textual (CSV) para **Parquet** (compressão Snappy), particionados por ano.
* **Prata:** Tabela higienizada pelo PySpark, filtrando colunas analíticas e aplicando regras de negócio (como preenchimento de notas ausentes).

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- [Docker](https://www.docker.com/products/docker-desktop) instalado e rodando.
- [Docker Compose](https://docs.docker.com/compose/install/) instalado.
- Arquivos `.zip` dos microdados do ENEM baixados do site do INEP e colocados na pasta raiz do projeto dentro de `dados/`.

### 1. Iniciar a Pipeline de Dados (Processamento do Data Lake)
O comando abaixo irá providenciar toda a infraestrutura (Ubuntu, Java 17, PySpark) e executará o orquestrador `run_pipeline.sh`:
```bash
docker-compose up --build spark
```
Nesta etapa de execução única (batch), os arquivos gigantes deixarão de ser `.zip` e magicamente se materializarão no seu disco como tabelas limpas na pasta local `data_lake/prata/`.

### 2. Acessar o Ambiente de Análise (Jupyter)
Para iniciar as análises de Ciência de Dados ou explorar os dados via Pandas interativamente, inicie o Laboratório:
```bash
docker-compose up jupyter
```
No terminal logado do serviço, acesse a URL que contém o `token` (ex: `http://127.0.0.1:8888/?token=...`) diretamente no seu navegador. Os dados estarão no caminho do container `/app/data_lake/prata/enem`.

---

## 📁 Estrutura de Diretórios e Código
```text
📦 enem_datalake
 ┣ 📂 dados/           # Armazena os .zips brutos baixados (Ignorado no Git para evitar limite de tamanho)
 ┣ 📂 data_lake/       # Repositório de dados processados em Parquet (Mapeado nos Volumes do Docker)
 ┃ ┣ 📂 bronze/        
 ┃ ┗ 📂 prata/         
 ┣ 📂 docs/            # Documentação rica e aprofundada voltada para o time e infraestrutura
 ┣ 📂 notebooks/       # Armazena os relatórios .ipynb criados pelo time
 ┣ 📂 src/             # Scripts primários da pipeline e de extração
 ┃ ┣ 📜 extrair_dados_spark.py
 ┃ ┣ 📜 ingestao_bronze_spark.py
 ┃ ┣ 📜 processamento_prata_spark.py
 ┃ ┗ 📜 run_pipeline.sh  # Orquestrador Mestre de bash
 ┣ 📜 .gitignore       # Blindagem do GitHub e do GitLocal (~100MB limit guard)
 ┣ 📜 docker-compose.yml 
 ┣ 📜 Dockerfile       # Receita do SO limpo, instâncias Rootlsess e isolamento de usuários
 ┗ 📜 requirements.txt # Bibliotecas padronizadas (Pandas, PyArrow, PySpark, JupyterLab)
```

## 📚 Documentação Adicional / Manuais

Abaixo estão os guias detalhados encontrados na pasta `docs/` que acompanham o repositório. Eles esclarecem as motivações sobre negócio e infraestrutura deste Data Lake:
- **[Infraestrutura e Docker](docs/infraestrutura_docker.md):** Fundamentos do uso de Volumes e escolha da imagem.
- **[Transformações - Camada Prata](docs/transformacoes_camada_prata.md):** Explicativo sobre a lógica de tratamento de dados (`NULLs`) e seleção vertical do INEP.
- **[Guia de Apresentação ao Time](docs/guia_apresentacao_time.md):** Manual focado em como reproduzir a pipeline (idempotência) para os stakeholders.
- **[Oportunidade Analítica & Insights](docs/insights_analiticos.md):** Matriz de estudos sociais, desigualdade geográfica e modelos recomendados de ML usando o Dataset Lapidado.


