# nb_04_sales_quality_checks
# Objectif : tracer des controles qualite sur le pipeline sales medallion.

from datetime import datetime, timezone
from pyspark.sql import functions as F

RUN_TS = datetime.now(timezone.utc).isoformat()
FAIL_ON_CRITICAL = False

bronze = spark.table("bronze_sales_orders")
silver = spark.table("silver_sales_orders")
facts = spark.table("factsales_gold")

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


bronze_count = bronze.count()
silver_count = silver.count()
fact_count = facts.count()

add_check("bronze_has_rows", "critical", bronze_count > 0, bronze_count, "bronze_sales_orders doit contenir des lignes")
add_check("silver_has_rows", "critical", silver_count > 0, silver_count, "silver_sales_orders doit contenir des lignes")
add_check("fact_matches_silver_count", "critical", fact_count == silver_count, f"{fact_count}/{silver_count}", "factsales_gold doit avoir autant de lignes que silver")

invalid_quantity = silver.filter(F.col("Quantity").isNull() | (F.col("Quantity") <= 0)).count()
invalid_amount = silver.filter(F.col("LineAmount").isNull() | (F.col("LineAmount") <= 0)).count()
missing_customer = silver.filter(F.col("CustomerName").isNull() | (F.length(F.col("CustomerName")) == 0)).count()
missing_product = silver.filter(F.col("Item").isNull() | (F.length(F.col("Item")) == 0)).count()
duplicate_lines = silver.groupBy("SalesOrderNumber", "SalesOrderLineNumber").count().filter(F.col("count") > 1).count()

add_check("quantity_positive", "critical", invalid_quantity == 0, invalid_quantity, "Les quantites doivent etre strictement positives")
add_check("line_amount_positive", "critical", invalid_amount == 0, invalid_amount, "Le montant de ligne doit etre positif")
add_check("customer_not_empty", "major", missing_customer == 0, missing_customer, "Chaque ligne doit avoir un client")
add_check("product_not_empty", "major", missing_product == 0, missing_product, "Chaque ligne doit avoir un produit")
add_check("sales_line_unique", "critical", duplicate_lines == 0, duplicate_lines, "Une ligne de commande doit etre unique")

dq_df = spark.createDataFrame(checks)
dq_df.write.format("delta").mode("append").saveAsTable("dq_sales_results")

display(dq_df.orderBy("severity", "check_name"))

critical_failed = [check for check in checks if check["severity"] == "critical" and not check["passed"]]
if FAIL_ON_CRITICAL and critical_failed:
    failed_names = ", ".join(check["check_name"] for check in critical_failed)
    raise ValueError(f"Critical data quality checks failed: {failed_names}")

print(f"Sales data quality checks written at {RUN_TS}")

