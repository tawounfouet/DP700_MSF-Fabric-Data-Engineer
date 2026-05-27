# nb_02_transform_books_silver
# Objectif : transformer le JSONL bronze en tables Delta silver propres et typees.

from pathlib import Path
from pyspark.sql import functions as F

FILES_ROOT = Path("/lakehouse/default/Files")
RAW_JSON_ROOT = FILES_ROOT / "bronze" / "books_toscrape" / "raw_json"

available_dates = sorted(
    path.name.split("=", 1)[1]
    for path in RAW_JSON_ROOT.glob("ingestion_date=*")
    if path.is_dir()
)

if not available_dates:
    raise ValueError("Aucune ingestion bronze trouvee. Executez nb_01_ingest_books_bronze d'abord.")

INGESTION_DATE = available_dates[-1]
SOURCE_PATH = f"Files/bronze/books_toscrape/raw_json/ingestion_date={INGESTION_DATE}/books.jsonl"

raw_df = spark.read.json(SOURCE_PATH)

rating_pairs = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}
rating_map = F.create_map([item for pair in rating_pairs.items() for item in (F.lit(pair[0]), F.lit(pair[1]))])

clean_df = (
    raw_df
    .withColumn("title", F.trim(F.col("title")))
    .withColumn("category", F.trim(F.col("category")))
    .withColumn("category_norm", F.lower(F.regexp_replace(F.trim(F.col("category")), r"[^A-Za-z0-9]+", "_")))
    .withColumn("price_gbp", F.regexp_extract(F.col("price_text"), r"([0-9]+(?:\.[0-9]+)?)", 1).cast("decimal(10,2)"))
    .withColumn("price_excl_tax_gbp", F.regexp_extract(F.col("price_excl_tax_text"), r"([0-9]+(?:\.[0-9]+)?)", 1).cast("decimal(10,2)"))
    .withColumn("price_incl_tax_gbp", F.regexp_extract(F.col("price_incl_tax_text"), r"([0-9]+(?:\.[0-9]+)?)", 1).cast("decimal(10,2)"))
    .withColumn("tax_gbp", F.regexp_extract(F.col("tax_text"), r"([0-9]+(?:\.[0-9]+)?)", 1).cast("decimal(10,2)"))
    .withColumn("rating_value", F.element_at(rating_map, F.col("rating_text")).cast("int"))
    .withColumn("is_available", F.lower(F.col("availability_text")).contains("in stock"))
    .withColumn("available_count", F.regexp_extract(F.col("availability_text"), r"\((\d+) available\)", 1).cast("int"))
    .withColumn("number_of_reviews", F.col("number_of_reviews_text").cast("int"))
    .withColumn("book_id", F.sha2(F.coalesce(F.col("upc"), F.col("source_url"), F.col("title")), 256))
    .withColumn("silver_processed_ts", F.current_timestamp())
)

rejected_df = (
    clean_df
    .withColumn(
        "reject_reason",
        F.concat_ws(
            "; ",
            F.when(F.col("title").isNull() | (F.length(F.col("title")) == 0), F.lit("missing_title")),
            F.when(F.col("price_gbp").isNull(), F.lit("missing_or_invalid_price")),
            F.when(F.col("rating_value").isNull(), F.lit("missing_or_invalid_rating")),
            F.when(F.col("source_url").isNull(), F.lit("missing_source_url")),
        )
    )
    .filter(F.length(F.col("reject_reason")) > 0)
)

valid_df = (
    clean_df
    .filter(F.col("title").isNotNull())
    .filter(F.col("price_gbp").isNotNull())
    .filter(F.col("rating_value").between(1, 5))
    .filter(F.col("source_url").isNotNull())
    .dropDuplicates(["source_url"])
)

silver_books = valid_df.select(
    "book_id",
    "run_id",
    "ingestion_date",
    "ingestion_ts_utc",
    "source_url",
    "catalog_page_number",
    "rank_on_page",
    "title",
    "category",
    "category_norm",
    "price_gbp",
    "price_excl_tax_gbp",
    "price_incl_tax_gbp",
    "tax_gbp",
    "rating_text",
    "rating_value",
    "availability_text",
    "is_available",
    "available_count",
    "number_of_reviews",
    "description",
    "image_url",
    "upc",
    "product_type",
    "silver_processed_ts",
)

silver_categories = (
    silver_books
    .select("category", "category_norm")
    .dropDuplicates(["category_norm"])
    .withColumn("category_id", F.sha2(F.col("category_norm"), 256))
)

silver_books.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_books")
silver_categories.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_categories")
rejected_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_books_rejected")

print(f"Ingestion date silver: {INGESTION_DATE}")
print(f"Silver books: {silver_books.count()}")
print(f"Rejected rows: {rejected_df.count()}")
display(silver_books.limit(10))
