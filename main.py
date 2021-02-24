import os
os.environ["PYSPARK_SUBMIT_ARGS"] = "--packages eisber:sarplus:0.2.6 pyspark-shell"

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("sample")
    .master("local[*]")
    .config("memory", "1G")
    .config("spark.sql.shuffle.partitions", "1")
    .config("spark.sql.crossJoin.enabled", True)
    .config("spark.ui.enabled", False)
    .getOrCreate()
)

print(spark.sparkContext.range(256).collect())