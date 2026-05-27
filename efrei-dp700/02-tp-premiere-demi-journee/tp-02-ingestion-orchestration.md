# TP 02 - Ingestion, transformation et orchestration

Durée : 50 minutes.

Objectif : comprendre les rôles respectifs de Dataflow Gen2, pipeline et notebook.

## Partie A - Comparer les outils

Completez ce tableau en binome avant de manipuler :

| Besoin | Outil pressenti | Pourquoi |
| --- | --- | --- |
| Copier un fichier HTTP vers un lakehouse |  |  |
| Nettoyer des colonnes avec Power Query |  |  |
| Scraper un site web pagine |  |  |
| Lancer trois etapes dans l'ordre |  |  |
| Transformer un gros volume avec Spark |  |  |
| Exposer une table gold a Power BI |  |  |

## Partie B - Pipeline simple

Inspirez-vous du lab local `../../Instructions/Labs/04-ingest-pipeline.md`.

1. Dans le workspace, creer un pipeline :

```text
pl_intro_sales_ingestion
```

2. Ajouter une activite `Copy data`.
3. Source HTTP :

```text
https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/sales.csv
```

4. Destination : `lh_intro_fabric/Files/new_data/sales.csv`.
5. Executer le pipeline.
6. Verifier le fichier dans le lakehouse.

## Partie C - Notebook de transformation

Creer un notebook `nb_intro_load_sales` attache au lakehouse.

Coller et executer :

```python
from pyspark.sql.functions import col, month, year, split

df = spark.read.format("csv").option("header", "true").load("Files/new_data/sales.csv")

df = (
    df
    .withColumn("OrderYear", year(col("OrderDate")))
    .withColumn("OrderMonth", month(col("OrderDate")))
    .withColumn("FirstName", split(col("CustomerName"), " ").getItem(0))
    .withColumn("LastName", split(col("CustomerName"), " ").getItem(1))
)

df.write.format("delta").mode("overwrite").saveAsTable("sales_intro_clean")
```

Verifier que la table `sales_intro_clean` apparait dans le lakehouse.

## Partie D - Orchestrer

Ajouter une activite `Notebook` dans le pipeline apres `Copy data`.

Le pipeline attendu :

```text
Copy data -> Notebook transformation
```

Executer puis consulter l'historique.

## Debrief

- Le pipeline transforme-t-il les donnees lui-meme ?
- Le notebook sait-il planifier son execution tout seul ?
- Quel outil est le plus adapte pour Books to Scrape ?
- Pourquoi la combinaison pipeline + notebook ressemble-t-elle a une vraie chaine ELT ?
