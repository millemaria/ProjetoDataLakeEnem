# Registro de Troubleshooting e Soluções (ENEM 2024)

Este documento registra os problemas encontrados durante a execução do pipeline de ingestão de dados do ENEM 2024 no ambiente Docker, e quais foram as soluções adotadas para corrigi-los.

## 1. Problema: Erro de Quebra de Linha no Script Linux (`run.sh`)

### Descrição
Ao tentar acionar o orquestrador do pipeline usando o comando `docker exec spark_enem bash /app/run.sh --fonte enem --etapa ouro`, o terminal retornou erros como:
> `/app/run.sh: line 14: $'\r': command not found`

### Causa
Como o projeto foi clonado (`git pull`) em um ambiente Windows, o Git configurou as quebras de linha padrão do arquivo `run.sh` no formato do Windows (`CRLF` -> `\r\n`). Contudo, o container Spark executa uma imagem Linux que espera quebras de linha estritamente no formato Unix (`LF` -> `\n`). O `\r` (carriage return) sobrou no final das linhas de comando shell, causando falha no interpretador Bash.

### Solução Aplicada
Para resolver o bloqueio sem impactar o container, utilizamos o PowerShell localmente na máquina host (Windows) para remover os `\r`:
```powershell
(Get-Content -Raw run.sh).Replace("`r`n", "`n") | Set-Content -NoNewline run.sh
```
Após o processo, as linhas do arquivo Shell Script estavam corretamente alinhadas e compatíveis com a execução interna no container Linux.

---

## 2. Problema: Data Lake Vazio (O arquivo Enem 2024 não foi lido)

### Descrição
O diretório do Data Lake (`/app/data_lake/`) permanecia vazio após tentar executar as etapas de processamento. A camada Bronze (responsável por captar do arquivo raw) simplesmente não detectou e nem iniciou o processo de ingestão para o ano de 2024.

### Causa
Ao inspecionarmos o comportamento do código fonte no arquivo `src/sources/enem/01_bronze.py`, verificamos que a função que vasculha as pastas descompactadas dos microdados procura de maneira específica por um arquivo nomeado **`MICRODADOS_ENEM_<ANO>.csv`**.
No entanto, na edição do Enem de 2024, o INEP alterou a estrutura de entrega do CSV, substituindo o tradicional arquivo único gigante por vários sub-arquivos menores:
- `PARTICIPANTES_2024.csv` *(arquivo contendo as informações dos estudantes)*
- `ITENS_PROVA_2024.csv`
- `RESULTADOS_2024.csv`

Como o script não achava `MICRODADOS_ENEM_2024.csv`, ele pulava o diretório sem processar.

### Solução Aplicada
Buscando a solução mais rápida e eficiente sem precisar engessar ou criar casos de exceção extensos na lógica já homologada do script Python, modificamos os próprios dados extraídos para o formato esperado:

1. Criamos um sub-diretório de backup no container para salvaguardar os CSVs não mapeados ainda: `/app/dados/microdados_enem_2024/DADOS/BACKUP/`.
2. Movemos `ITENS_PROVA_2024.csv` e `RESULTADOS_2024.csv` para a referida pasta de backup.
3. Renomeamos o arquivo principal com as notas e os dados demográficos originais, de `PARTICIPANTES_2024.csv` para a assinatura tradicional: `MICRODADOS_ENEM_2024.csv`.

Com isso feito, nós rodamos sequencialmente:
- **Camada Bronze:** O script leu o novo arquivo transformando o raw text (CSV) num formato colunar mais produtivo (Parquet) agrupado pela partição do ano.
- **Camada Prata:** Criou sua modelagem sanitizando valores nulos e definindo as tipagens corretas de schema para processamento analítico.
- **Camada Ouro:** Aplicou a consolidação gerando KPIs por perfil/região em cima da base limpa.

Todos os dados reprocessados residem agora estruturados no volume `/data_lake/`.
