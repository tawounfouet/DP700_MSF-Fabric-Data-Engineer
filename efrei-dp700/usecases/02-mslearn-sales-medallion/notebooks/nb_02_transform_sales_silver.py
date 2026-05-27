# nb_02_transform_sales_silver
# Objectif : nettoyer, typer et enrichir les commandes bronze pour produire silver_sales_orders.

from pyspark.sql import functions as F

bronze_df = spark.table("bronze_sales_orders")

silver_df = (
    bronze_df
    .withColumn("CustomerName", F.when(F.col("CustomerName").isNull() | (F.trim(F.col("CustomerName")) == ""), F.lit("Unknown")).otherwise(F.trim(F.col("CustomerName"))))
    .withColumn("Email", F.lower(F.trim(F.col("Email"))))
    .withColumn("Item", F.trim(F.col("Item")))
    .withColumn("OrderYear", F.year(F.col("OrderDate")))
    .withColumn("OrderMonth", F.month(F.col("OrderDate")))
    .withColumn("LineAmount", (F.col("Quantity") * (F.col("UnitPrice") + F.col("Tax"))).cast("decimal(12,2)"))
    .withColumn("UnitPrice", F.col("UnitPrice").cast("decimal(10,2)"))
    .withColumn("Tax", F.col("Tax").cast("decimal(10,2)"))
    .withColumn("SalesOrderLineKey", F.sha2(F.concat_ws("|", "SalesOrderNumber", F.col("SalesOrderLineNumber").cast("string")), 256))
    .withColumn("SilverProcessedTS", F.current_timestamp())
    .filter(F.col("SalesOrderNumber").isNotNull())
    .filter(F.col("SalesOrderLineNumber").isNotNull())
    .filter(F.col("OrderDate").isNotNull())
    .filter(F.col("Item").isNotNull())
    .dropDuplicates(["SalesOrderNumber", "SalesOrderLineNumber"])
)

silver_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_sales_orders")

print(f"Silver rows: {silver_df.count()}")
display(silver_df.limit(10))

