from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType

# Tạo Spark Session
spark = SparkSession.builder \
    .appName("CryptoPriceStream") \
    .getOrCreate()

# Schema cho dữ liệu JSON từ Kafka
schema = StructType() \
    .add("iso", StringType()) \
    .add("name", StringType()) \
    .add("date_time", StringType()) \
    .add("current_price", StringType()) \
    .add("open", StringType()) \
    .add("high", StringType()) \
    .add("low", StringType()) \
    .add("close", StringType())

# Đọc từ Kafka topic
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "crypto-prices") \
  .load()

# Giải mã giá trị từ Kafka (chuỗi byte -> string)
df = df.selectExpr("CAST(value AS STRING)")

# Parse dữ liệu JSON
df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# In dữ liệu ra console
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
