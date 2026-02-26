import sys
sys.path.insert(0, "/app/src")
from spark_utils import get_spark_session

spark = get_spark_session("Check")
df_bronze = spark.read.parquet("/app/data_lake/bronze/enem/ano=2024")
print("--- ALL BRONZE ---------")
for c in df_bronze.columns: print(c)
spark.stop()
