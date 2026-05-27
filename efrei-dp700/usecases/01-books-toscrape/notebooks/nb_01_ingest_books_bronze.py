# nb_01_ingest_books_bronze
# Objectif : scraper Books to Scrape, conserver le HTML brut et produire un JSONL bronze.

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import json
import re
import time
import uuid

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
MAX_CATALOG_PAGES = 5
REQUEST_SLEEP_SECONDS = 0.2
USER_AGENT = "EFREI-DP700-Fabric-Teaching/1.0"

RUN_ID = str(uuid.uuid4())
INGESTION_TS = datetime.now(timezone.utc)
INGESTION_DATE = INGESTION_TS.date().isoformat()

FILES_ROOT = Path("/lakehouse/default/Files")
BRONZE_ROOT = FILES_ROOT / "bronze" / "books_toscrape"
RAW_HTML_DIR = BRONZE_ROOT / "raw_html" / f"ingestion_date={INGESTION_DATE}"
RAW_JSON_DIR = BRONZE_ROOT / "raw_json" / f"ingestion_date={INGESTION_DATE}"
LOG_DIR = FILES_ROOT / "logs" / "books_toscrape"

for folder in [RAW_HTML_DIR, RAW_JSON_DIR, LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


def safe_name(value: str, fallback: str = "page") -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", value or fallback).strip("_")
    return (cleaned or fallback)[:120]


def normalize_table_key(value: str) -> str:
    key = (value or "").lower().strip()
    key = key.replace("(incl. tax)", "incl_tax")
    key = key.replace("(excl. tax)", "excl_tax")
    key = key.replace("number of reviews", "number_of_reviews")
    key = key.replace(" ", "_")
    key = safe_name(key, fallback="unknown")
    return re.sub(r"_+", "_", key)


def fetch_html(session: requests.Session, url: str) -> str:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding
    time.sleep(REQUEST_SLEEP_SECONDS)
    return response.text


def save_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def parse_product_table(soup: BeautifulSoup) -> dict:
    values = {}
    for row in soup.select("table.table.table-striped tr"):
        key = row.select_one("th")
        value = row.select_one("td")
        if key and value:
            normalized_key = normalize_table_key(key.get_text(strip=True))
            values[normalized_key] = value.get_text(strip=True)
    return values


def parse_product_detail(html: str, url: str, page_number: int, rank_on_page: int) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    table_values = parse_product_table(soup)

    title = soup.select_one("div.product_main h1")
    price = soup.select_one("p.price_color")
    availability = soup.select_one("p.instock.availability")
    rating = soup.select_one("p.star-rating")
    description_title = soup.select_one("#product_description")
    image = soup.select_one("div.item.active img") or soup.select_one("img.thumbnail")

    breadcrumbs = [a.get_text(strip=True) for a in soup.select("ul.breadcrumb li a")]
    category = breadcrumbs[-1] if len(breadcrumbs) >= 3 else None

    rating_text = None
    if rating:
        rating_classes = [item for item in rating.get("class", []) if item != "star-rating"]
        rating_text = rating_classes[0] if rating_classes else None

    description = None
    if description_title:
        desc_paragraph = description_title.find_next("p")
        description = desc_paragraph.get_text(" ", strip=True) if desc_paragraph else None

    return {
        "run_id": RUN_ID,
        "ingestion_ts_utc": INGESTION_TS.isoformat(),
        "ingestion_date": INGESTION_DATE,
        "source_url": url,
        "catalog_page_number": page_number,
        "rank_on_page": rank_on_page,
        "title": title.get_text(" ", strip=True) if title else None,
        "category": category,
        "price_text": price.get_text(strip=True) if price else table_values.get("price_incl_tax"),
        "rating_text": rating_text,
        "availability_text": availability.get_text(" ", strip=True) if availability else table_values.get("availability"),
        "description": description,
        "image_url": urljoin(url, image.get("src")) if image and image.get("src") else None,
        "upc": table_values.get("upc"),
        "product_type": table_values.get("product_type"),
        "price_excl_tax_text": table_values.get("price_excl_tax"),
        "price_incl_tax_text": table_values.get("price_incl_tax"),
        "tax_text": table_values.get("tax"),
        "number_of_reviews_text": table_values.get("number_of_reviews"),
    }


session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

records = []
catalogue_url = BASE_URL
page_number = 1

while catalogue_url and page_number <= MAX_CATALOG_PAGES:
    catalogue_html = fetch_html(session, catalogue_url)
    catalogue_file = RAW_HTML_DIR / f"catalog_page_{page_number:03d}.html"
    save_text(catalogue_file, catalogue_html)

    catalogue_soup = BeautifulSoup(catalogue_html, "html.parser")
    cards = catalogue_soup.select("article.product_pod")

    for rank_on_page, card in enumerate(cards, start=1):
        link = card.select_one("h3 a")
        if not link or not link.get("href"):
            continue

        detail_url = urljoin(catalogue_url, link["href"])
        detail_html = fetch_html(session, detail_url)

        product_slug = safe_name(detail_url.rstrip("/").split("/")[-2] if "/" in detail_url else link.get_text(strip=True))
        detail_file = RAW_HTML_DIR / f"product_p{page_number:03d}_{rank_on_page:02d}_{product_slug}.html"
        save_text(detail_file, detail_html)

        records.append(parse_product_detail(detail_html, detail_url, page_number, rank_on_page))

    next_link = catalogue_soup.select_one("li.next a")
    catalogue_url = urljoin(catalogue_url, next_link["href"]) if next_link and next_link.get("href") else None
    page_number += 1

jsonl_path = RAW_JSON_DIR / "books.jsonl"
with jsonl_path.open("w", encoding="utf-8") as handle:
    for record in records:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

audit = [{
    "run_id": RUN_ID,
    "ingestion_ts_utc": INGESTION_TS.isoformat(),
    "ingestion_date": INGESTION_DATE,
    "base_url": BASE_URL,
    "max_catalog_pages": MAX_CATALOG_PAGES,
    "book_records": len(records),
    "raw_json_path": f"Files/bronze/books_toscrape/raw_json/ingestion_date={INGESTION_DATE}/books.jsonl",
    "raw_html_path": f"Files/bronze/books_toscrape/raw_html/ingestion_date={INGESTION_DATE}/",
}]

spark.createDataFrame(audit).write.format("delta").mode("append").saveAsTable("audit_ingestion_runs")

bronze_df = spark.read.json(f"Files/bronze/books_toscrape/raw_json/ingestion_date={INGESTION_DATE}/books.jsonl")
print(f"Run {RUN_ID} - {len(records)} books written to {jsonl_path}")
display(bronze_df.limit(10))
