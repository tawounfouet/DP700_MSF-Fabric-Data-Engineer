# nb_01_load_sales_bronze
# Objectif : charger les CSV Microsoft Learn depuis Files/bronze/sales/orders vers une table Delta bronze.

from pyspark.sql import functions as F
from pyspark.sql.types import DateType, FloatType, IntegerType, StringType, StructField, StructType

SOURCE_PATH = "Files/bronze/sales/orders/*.csv"

order_schema = StructType([
    StructField("SalesOrderNumber", StringType()),
    StructField("SalesOrderLineNumber", IntegerType()),
    StructField("OrderDate", DateType()),
    StructField("CustomerName", StringType()),
    StructField("Email", StringType()),
    StructField("Item", StringType()),
    StructField("Quantity", IntegerType()),
    StructField("UnitPrice", FloatType()),
    StructField("Tax", FloatType()),
])

bronze_df = (
    spark.read
    .format("csv")
    .option("header", "false")
    .schema(order_schema)
    .load(SOURCE_PATH)
    .withColumn("SourceFile", F.input_file_name())
    .withColumn("BronzeLoadedTS", F.current_timestamp())
)

bronze_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("bronze_sales_orders")

print(f"Bronze rows: {bronze_df.count()}")
display(bronze_df.limit(10))

