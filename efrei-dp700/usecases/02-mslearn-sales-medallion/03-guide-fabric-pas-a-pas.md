# 03 - Guide Fabric pas a pas

## 1. Creer le workspace

Nom :

```text
ws-efrei-dp700-sales-dev-groupeXX
```

## 2. Creer le lakehouse

Nom :

```text
lh_sales_medallion
```

## 3. Charger les fichiers bronze

Dans le lakehouse, creer :

```text
Files/bronze/sales/orders/
```

Uploader les fichiers fournis dans ce dossier local :

```text
data/orders/2019.csv
data/orders/2020.csv
data/orders/2021.csv
```

## 4. Creer les notebooks

Creer quatre notebooks Fabric et coller le contenu :

- `notebooks/nb_01_load_sales_bronze.py`
- `notebooks/nb_02_transform_sales_silver.py`
- `notebooks/nb_03_build_sales_gold.py`
- `notebooks/nb_04_sales_quality_checks.py`

Attacher le lakehouse `lh_sales_medallion` a chaque notebook.

## 5. Executer

Ordre :

```text
nb_01_load_sales_bronze
nb_02_transform_sales_silver
nb_03_build_sales_gold
nb_04_sales_quality_checks
```

## 6. Creer le pipeline

Nom :

```text
pl_sales_medallion_end_to_end
```

Activites :

```text
Notebook bronze -> Notebook silver -> Notebook gold -> Notebook quality
```

## 7. Explorer avec SQL

Basculer vers le SQL analytics endpoint du lakehouse et executer :

```text
sql-powerbi/queries_sales_gold.sql
```

## 8. Creer le modele semantique

Inclure :

- `dimdate_gold`
- `dimcustomer_gold`
- `dimproduct_gold`
- `factsales_gold`

Puis suivre :

```text
sql-powerbi/powerbi_model.md
```

