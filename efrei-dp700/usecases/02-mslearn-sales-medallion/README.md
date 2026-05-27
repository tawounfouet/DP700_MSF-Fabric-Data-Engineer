# Use case end-to-end - Microsoft Learn Sales Medallion

Ce use case reprend et structure l'exemple officiel Microsoft Learn du depot local :

```text
learning/cloud/azure/ms-learn/mslearn-fabric
```

Il s'appuie principalement sur le lab :

```text
Instructions/Labs/03b-medallion-lakehouse.md
```

et sur les fichiers :

```text
Allfiles/Labs/01/orders/2019.csv
Allfiles/Labs/01/orders/2020.csv
Allfiles/Labs/01/orders/2021.csv
```

## Objectif

Construire une mini plateforme analytique Fabric pour des ventes Adventure Works :

- Ingestion de fichiers CSV annuels dans une zone bronze.
- Transformation en table Delta silver.
- Construction d'un schema etoile gold.
- Controle qualite.
- Exposition via SQL analytics endpoint et modele semantique Power BI.

## Pourquoi ce deuxieme use case

Books to Scrape montre un flux web semi-structure. Ce use case Microsoft Learn montre un flux plus classique d'entreprise : fichiers de ventes, typage, dimensions, faits et reporting.

## Items Fabric recommandes

| Item | Nom recommande | Role |
| --- | --- | --- |
| Workspace | `ws-efrei-dp700-sales-dev-groupeXX` | Conteneur projet |
| Lakehouse | `lh_sales_medallion` | Stockage Files + Tables |
| Notebook | `nb_01_load_sales_bronze` | Lecture fichiers CSV bronze |
| Notebook | `nb_02_transform_sales_silver` | Nettoyage et table Delta silver |
| Notebook | `nb_03_build_sales_gold` | Dimensions et fait gold |
| Notebook | `nb_04_sales_quality_checks` | Controle qualite |
| Pipeline | `pl_sales_medallion_end_to_end` | Orchestration |
| Semantic model | `sm_sales_analytics` | Couche Power BI |
| Report | `rpt_sales_analysis` | Analyse ventes |

## Organisation Lakehouse

```text
Files/
  bronze/sales/orders/
    2019.csv
    2020.csv
    2021.csv

Tables/
  bronze_sales_orders
  silver_sales_orders
  dimdate_gold
  dimcustomer_gold
  dimproduct_gold
  factsales_gold
  dq_sales_results
```

## Donnees incluses

Les donnees Microsoft Learn sont copiees dans :

```text
data/orders/
```

Dans Fabric, chargez les trois fichiers dans :

```text
Files/bronze/sales/orders/
```

## Ordre d'execution

1. Lire `01-cadrage-metier.md`.
2. Lire `02-architecture-cible.md`.
3. Suivre `03-guide-fabric-pas-a-pas.md`.
4. Executer les notebooks dans l'ordre.
5. Creer le pipeline.
6. Executer les requetes SQL.
7. Creer le modele semantique.

