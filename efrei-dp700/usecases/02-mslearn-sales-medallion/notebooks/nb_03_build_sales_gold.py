# nb_03_build_sales_gold
# Objectif : construire un schema etoile gold depuis silver_sales_orders.

from pyspark.sql import functions as F

sales = spark.table("silver_sales_orders")

dimdate_gold = (
    sales
    .select("OrderDate")
    .dropDuplicates(["OrderDate"])
    .withColumn("DateKey", F.date_format(F.col("OrderDate"), "yyyyMMdd").cast("int"))
    .withColumn("Day", F.dayofmonth(F.col("OrderDate")))
    .withColumn("Month", F.month(F.col("OrderDate")))
    .withColumn("MonthName", F.date_format(F.col("OrderDate"), "MMM"))
    .withColumn("Year", F.year(F.col("OrderDate")))
    .withColumn("YearMonth", F.date_format(F.col("OrderDate"), "yyyy-MM"))
)

dimcustomer_gold = (
    sales
    .select("CustomerName", "Email")
    .dropDuplicates(["CustomerName", "Email"])
    .withColumn("CustomerID", F.sha2(F.concat_ws("|", "CustomerName", "Email"), 256))
    .withColumn("FirstName", F.split(F.col("CustomerName"), " ").getItem(0))
    .withColumn("LastName", F.split(F.col("CustomerName"), " ").getItem(1))
)

dimproduct_gold = (
    sales
    .select("Item")
    .dropDuplicates(["Item"])
    .withColumn("ProductID", F.sha2(F.col("Item"), 256))
    .withColumn("ProductName", F.split(F.col("Item"), ", ").getItem(0))
    .withColumn("ProductVariant", F.coalesce(F.split(F.col("Item"), ", ").getItem(1), F.lit("")))
)

factsales_gold = (
    sales.alias("s")
    .join(dimcustomer_gold.alias("c"), (F.col("s.CustomerName") == F.col("c.CustomerName")) & (F.col("s.Email") == F.col("c.Email")), "left")
    .join(dimproduct_gold.alias("p"), F.col("s.Item") == F.col("p.Item"), "left")
    .join(dimdate_gold.alias("d"), F.col("s.OrderDate") == F.col("d.OrderDate"), "left")
    .select(
        F.col("s.SalesOrderLineKey"),
        F.col("s.SalesOrderNumber"),
        F.col("s.SalesOrderLineNumber"),
        F.col("d.DateKey"),
        F.col("c.CustomerID"),
        F.col("p.ProductID"),
        F.col("s.Quantity"),
        F.col("s.UnitPrice"),
        F.col("s.Tax"),
        F.col("s.LineAmount"),
        F.col("s.SourceFile"),
        F.current_timestamp().alias("GoldProcessedTS"),
    )
)

sales_year_month_gold = (
    factsales_gold.alias("f")
    .join(dimdate_gold.alias("d"), F.col("f.DateKey") == F.col("d.DateKey"), "left")
    .groupBy("d.Year", "d.Month", "d.YearMonth")
    .agg(
        F.countDistinct("f.SalesOrderNumber").alias("order_count"),
        F.sum("f.Quantity").alias("total_quantity"),
        F.sum("f.LineAmount").cast("decimal(14,2)").alias("total_revenue"),
    )
)

dimdate_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("dimdate_gold")
dimcustomer_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("dimcustomer_gold")
dimproduct_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("dimproduct_gold")
factsales_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("factsales_gold")
sales_year_month_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("sales_year_month_gold")

print(f"Fact rows: {factsales_gold.count()}")
display(sales_year_month_gold.orderBy("Year", "Month"))

