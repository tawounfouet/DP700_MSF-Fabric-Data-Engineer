# 03 - Guide Fabric pas a pas

## 1. Creer le workspace

Nom :

```text
ws-efrei-dp700-books-dev-groupeXX
```

Verifier qu'il est associe a une capacite Fabric.

## 2. Creer le lakehouse

Nom :

```text
lh_books_toscrape
```

Ce lakehouse portera les zones `Files` et `Tables`.

## 3. Creer les notebooks

Creer quatre notebooks dans Fabric et coller le contenu des fichiers :

- `notebooks/nb_01_ingest_books_bronze.py`
- `notebooks/nb_02_transform_books_silver.py`
- `notebooks/nb_03_build_books_gold.py`
- `notebooks/nb_04_data_quality_checks.py`

Attacher le lakehouse `lh_books_toscrape` a chaque notebook.

Avant le notebook bronze, executer dans une cellule separee si necessaire :

```python
%pip install beautifulsoup4 requests
```

## 4. Executer en mode rapide

Dans le notebook bronze, commencer avec :

```python
MAX_CATALOG_PAGES = 5
REQUEST_SLEEP_SECONDS = 0.2
```

Cela scrape environ 100 livres et suffit pour valider le pipeline en classe.

## 5. Executer en mode complet

Pour le dataset complet :

```python
MAX_CATALOG_PAGES = 50
REQUEST_SLEEP_SECONDS = 0.1
```

Le site expose 1000 resultats, avec 20 livres par page.

## 6. Verifier les tables

Apres execution :

- Rafraichir `Tables`.
- Verifier `silver_books`.
- Verifier `gold_book_catalog`.
- Ouvrir le SQL analytics endpoint.

## 7. Creer le pipeline

Nom :

```text
pl_books_toscrape_end_to_end
```

Ajouter les activites Notebook :

1. `nb_01_ingest_books_bronze`
2. `nb_02_transform_books_silver`
3. `nb_03_build_books_gold`
4. `nb_04_data_quality_checks`

Relier chaque activite a la suivante avec `On completion`.

## 8. Explorer avec SQL

Executer les requetes du fichier :

```text
sql-powerbi/queries_books_gold.sql
```

## 9. Preparer Power BI

Creer un modele semantique sur :

- `gold_book_catalog`
- `gold_category_stats`
- `dim_category_gold`
- `dim_rating_gold`
- `fact_books_gold`

Puis utiliser les mesures DAX de :

```text
sql-powerbi/powerbi_model.md
```

