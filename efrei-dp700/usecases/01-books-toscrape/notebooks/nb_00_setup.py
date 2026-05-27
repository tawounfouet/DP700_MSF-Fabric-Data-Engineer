# nb_00_setup
# Parametres communs pour le use case Books to Scrape.
#
# Dans Fabric, creez un notebook separe ou copiez cette cellule en haut des autres notebooks.
# Si besoin, executez d'abord dans une cellule Fabric :
# %pip install beautifulsoup4 requests

from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://books.toscrape.com/"

# Mode classe : 5 pages catalogue = environ 100 livres.
# Mode complet : 50 pages catalogue = 1000 livres.
MAX_CATALOG_PAGES = 5

# Rester raisonnable avec le site sandbox.
REQUEST_SLEEP_SECONDS = 0.2
USER_AGENT = "EFREI-DP700-Fabric-Teaching/1.0"

INGESTION_TS = datetime.now(timezone.utc)
INGESTION_DATE = INGESTION_TS.date().isoformat()

FILES_ROOT = Path("/lakehouse/default/Files")
PROJECT_ROOT = FILES_ROOT / "bronze" / "books_toscrape"

print(f"BASE_URL={BASE_URL}")
print(f"MAX_CATALOG_PAGES={MAX_CATALOG_PAGES}")
print(f"INGESTION_DATE={INGESTION_DATE}")
print(f"FILES_ROOT={FILES_ROOT}")

