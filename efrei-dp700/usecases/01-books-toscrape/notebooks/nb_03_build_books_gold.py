# nb_03_build_books_gold
# Objectif : construire les tables gold metier et un schema etoile simple.

from pyspark.sql import functions as F

silver_books = spark.table("silver_books")
silver_categories = spark.table("silver_categories")

dim_category_gold = (
    silver_categories
    .select("category_id", "category", "category_norm")
    .withColumn("gold_processed_ts", F.current_timestamp())
)

dim_rating_gold = spark.createDataFrame(
    [
        (1, "One", "Low"),
        (2, "Two", "Low"),
        (3, "Three", "Medium"),
        (4, "Four", "High"),
        (5, "Five", "High"),
    ],
    ["rating_value", "rating_label", "rating_band"]
)

fact_books_gold = (
    silver_books.alias("b")
    .join(dim_category_gold.alias("c"), F.col("b.category_norm") == F.col("c.category_norm"), "left")
    .select(
        F.col("b.book_id"),
        F.col("c.category_id"),
        F.col("b.rating_value"),
        F.col("b.price_gbp"),
        F.col("b.price_excl_tax_gbp"),
        F.col("b.price_incl_tax_gbp"),
        F.col("b.tax_gbp"),
        F.col("b.is_available"),
        F.coalesce(F.col("b.available_count"), F.lit(0)).alias("available_count"),
        F.col("b.number_of_reviews"),
        F.col("b.ingestion_date"),
        F.current_timestamp().alias("gold_processed_ts"),
    )
)

gold_book_catalog = (
    silver_books
    .select(
        "book_id",
        "title",
        "category",
        "category_norm",
        "price_gbp",
        "rating_value",
        "rating_text",
        "is_available",
        "available_count",
        "source_url",
        "image_url",
        "description",
        "ingestion_date",
    )
    .withColumn("price_bucket",
        F.when(F.col("price_gbp") < 15, F.lit("0-15"))
         .when(F.col("price_gbp") < 30, F.lit("15-30"))
         .when(F.col("price_gbp") < 45, F.lit("30-45"))
         .otherwise(F.lit("45+"))
    )
    .withColumn("gold_processed_ts", F.current_timestamp())
)

gold_category_stats = (
    gold_book_catalog
    .groupBy("category", "category_norm")
    .agg(
        F.count("*").alias("book_count"),
        F.avg("price_gbp").cast("decimal(10,2)").alias("avg_price_gbp"),
        F.min("price_gbp").alias("min_price_gbp"),
        F.max("price_gbp").alias("max_price_gbp"),
        F.avg("rating_value").cast("decimal(10,2)").alias("avg_rating"),
        F.sum(F.when(F.col("is_available"), F.lit(1)).otherwise(F.lit(0))).alias("available_books"),
        F.sum(F.when(F.col("rating_value") == 5, F.lit(1)).otherwise(F.lit(0))).alias("five_star_books"),
    )
    .withColumn("availability_rate", (F.col("available_books") / F.col("book_count")).cast("decimal(10,4)"))
    .withColumn("gold_processed_ts", F.current_timestamp())
)

dim_category_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("dim_category_gold")
dim_rating_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("dim_rating_gold")
fact_books_gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("fact_books_gold")
gold_book_catalog.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_book_catalog")
gold_category_stats.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_category_stats")

print(f"Gold catalog rows: {gold_book_catalog.count()}")
print(f"Gold categories: {gold_category_stats.count()}")
display(gold_category_stats.orderBy(F.desc("book_count")).limit(10))

