# nb_04_data_quality_checks
# Objectif : controler les tables silver/gold et tracer les resultats.

from datetime import datetime, timezone
from pyspark.sql import functions as F

FAIL_ON_CRITICAL = False
RUN_TS = datetime.now(timezone.utc).isoformat()

silver_books = spark.table("silver_books")
gold_book_catalog = spark.table("gold_book_catalog")
gold_category_stats = spark.table("gold_category_stats")

checks = []


def add_check(name: str, severity: str, passed: bool, metric_value, details: str) -> None:
    checks.append({
        "run_ts_utc": RUN_TS,
        "check_name": name,
        "severity": severity,
        "passed": bool(passed),
        "metric_value": str(metric_value),
        "details": details,
    })


silver_count = silver_books.count()
gold_count = gold_book_catalog.count()
category_count = gold_category_stats.count()

add_check("silver_has_rows", "critical", silver_count > 0, silver_count, "silver_books doit contenir au moins une ligne")
add_check("gold_has_same_count_as_silver", "critical", gold_count == silver_count, f"{gold_count}/{silver_count}", "gold_book_catalog doit avoir le meme nombre de livres que silver_books")
add_check("gold_has_categories", "major", category_count > 0, category_count, "gold_category_stats doit contenir des categories")

invalid_price_count = silver_books.filter(F.col("price_gbp").isNull() | (F.col("price_gbp") <= 0)).count()
invalid_rating_count = silver_books.filter(~F.col("rating_value").between(1, 5)).count()
empty_title_count = silver_books.filter(F.col("title").isNull() | (F.length(F.col("title")) == 0)).count()
empty_category_count = silver_books.filter(F.col("category").isNull() | (F.length(F.col("category")) == 0)).count()
duplicate_source_count = (
    silver_books
    .groupBy("source_url")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

add_check("price_positive", "critical", invalid_price_count == 0, invalid_price_count, "Aucun prix ne doit etre nul ou negatif")
add_check("rating_between_1_and_5", "critical", invalid_rating_count == 0, invalid_rating_count, "Les notes doivent etre comprises entre 1 et 5")
add_check("title_not_empty", "critical", empty_title_count == 0, empty_title_count, "Chaque livre doit avoir un titre")
add_check("category_not_empty", "major", empty_category_count == 0, empty_category_count, "Chaque livre doit avoir une categorie")
add_check("source_url_unique", "major", duplicate_source_count == 0, duplicate_source_count, "Une URL source ne doit pas produire plusieurs livres")

dq_df = spark.createDataFrame(checks)
dq_df.write.format("delta").mode("append").saveAsTable("dq_results")

display(dq_df.orderBy("severity", "check_name"))

critical_failed = [check for check in checks if check["severity"] == "critical" and not check["passed"]]
if FAIL_ON_CRITICAL and critical_failed:
    failed_names = ", ".join(check["check_name"] for check in critical_failed)
    raise ValueError(f"Critical data quality checks failed: {failed_names}")

print(f"Data quality checks written at {RUN_TS}")

