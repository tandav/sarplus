
import os
import sys
# sys.path.append('/usr/local/lib/python3.6/site-packages')
# sys.path.append('usr/local/lib/python3.6/site-packages/pyspark/lib/py4j-0.10.9-src.zip')
sys.path.append('/usr/local/lib/python3.7/site-packages')
sys.path.append('usr/local/lib/python3.7/site-packages/pyspark/lib/py4j-0.10.9-src.zip')
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-1.8.0-openjdk/'
os.environ['PYSPARK_PYTHON'] = "./sar_env/bin/python"
os.environ['PYSPARK_DRIVER_PYTHON'] = "./sar_env/bin/python"

from pyspark.sql import SparkSession


spark = (
    SparkSession
    .builder
    .master("local[*]")
    .config("spark.jars", 'sarplus_2.11-0.2.6.jar')
    .config("spark.driver.memory", '1G')
    .config("spark.sql.shuffle.partitions", "1")
    .config("spark.default.parallelism", "1")
    .config("spark.sql.crossJoin.enabled", True)
    .config("spark.ui.enabled", False)
    .config("spark.archives", "sar_env.tar.zip") # 'spark.yarn.dist.archives' in YARN.
    .getOrCreate()
)


# x = spark.sparkContext.range(3).collect()
def mapper(it):
    from pysarplus import SARPlus, SARModel
    
    yield type(SARPlus), 'success'


x = spark.sparkContext.range(3, numSlices=3).mapPartitions(mapper).collect()
print(x)
from pysarplus import SARPlus, SARModel

# spark dataframe with user/item/rating/optional timestamp tuples
train_df = spark.createDataFrame([
    (1, 1, 1), 
    (1, 2, 1), 
    (2, 1, 1), 
    (3, 1, 1), 
    (3, 3, 1)], 
    ['user_id', 'item_id', 'rating'])

# spark dataframe with user/item tuples
test_df = spark.createDataFrame([
    (1, 1, 1), 
    (3, 3, 1)], 
    ['user_id', 'item_id', 'rating'])



model = SARPlus(
    spark, 
    col_user='user_id', 
    col_item='item_id', 
    col_rating='rating', 
    similarity_type='jaccard',
)
model.fit(train_df)


model.recommend_k_items(test_df, 'sarplus_cache', top_k=3).show()
