# Deroule d'animation

## Intention

La journee doit alterner carte mentale, manipulation et prise de recul. Les etudiants doivent comprendre que Fabric n'est pas seulement "Power BI plus notebooks", mais une plateforme SaaS unifiee pour ingerer, stocker, transformer, gouverner et exposer des donnees.

## Fil rouge

Question a poser au debut :

> Vous devez construire rapidement une plateforme analytique pour une librairie en ligne. Qu'est-ce que vous creez dans Fabric, dans quel ordre, et pourquoi ?

Cette question revient a chaque etape :

- Ou mettre les donnees brutes ?
- Quand nettoyer ?
- Quand modeliser ?
- Qui consomme ?
- Comment rejouer ?
- Comment monitorer ?

## Matinee

### 09:00-09:20 - Cadrage

- Presenter DP-700 comme une certification d'ingenierie data Fabric.
- Faire emerger les experiences deja connues : SQL, Spark, Power BI, pipelines, data lake.
- Poser la difference entre outil et plateforme.

Message cle : Fabric assemble plusieurs experiences autour de OneLake et d'un modele SaaS commun.

### 09:20-10:10 - Vue d'ensemble

Support : `01-support-cours/slides-journee.md`

Visuels :

- `assets/visuals/fabric-end-to-end.svg`
- `assets/visuals/fabric-workspace-items.svg`
- `assets/images/mslearn/onelake-architecture.png`

Points a faire passer :

- Workspace = conteneur de travail, securite et cycle de vie.
- OneLake = stockage logique unifie du tenant.
- Lakehouse = fichiers + tables Delta, Spark + SQL endpoint.
- Warehouse = SQL analytique complet.
- Pipeline = orchestration.
- Dataflow Gen2 = Power Query cloud pour ETL low-code.
- Notebook = transformation code-first et traitements Spark.
- Semantic model = couche metier pour Power BI.

### 10:25-11:20 - TP 1

TP : `02-tp-premiere-demi-journee/tp-01-lakehouse-onelake-sql.md`

Objectif : creer un workspace, un lakehouse, charger un CSV, creer une table Delta, interroger via SQL endpoint.

Debrief :

- Pourquoi la table apparait-elle cote SQL ?
- Pourquoi le SQL endpoint est-il lecture seule pour les donnees lakehouse ?
- Quelle difference entre Files et Tables ?

### 11:20-12:15 - TP 2

TP : `02-tp-premiere-demi-journee/tp-02-ingestion-orchestration.md`

Objectif : comparer pipeline, Dataflow Gen2 et notebook.

Debrief rapide :

- Dataflow Gen2 quand le besoin est visuel/Power Query.
- Notebook quand il faut du controle code, bibliotheques ou Spark.
- Pipeline quand il faut orchestrer, parametrer, planifier, monitorer.

## Apres-midi

### 13:30-14:00 - Cadrage metier

Support : `usecases/01-books-toscrape/01-cadrage-metier.md`

Demander aux groupes de proposer :

- 3 questions metier.
- Les tables gold attendues.
- Les controles qualite minimaux.

### 14:00-15:15 - Bronze et Silver

Guides :

- `usecases/01-books-toscrape/03-guide-fabric-pas-a-pas.md`
- `usecases/01-books-toscrape/notebooks/nb_01_ingest_books_bronze.py`
- `usecases/01-books-toscrape/notebooks/nb_02_transform_books_silver.py`

Message cle : garder du HTML brut permet de rejouer le parsing sans rappeler le site.

### 15:30-16:35 - Gold, qualite, pipeline

Guides :

- `nb_03_build_books_gold.py`
- `nb_04_data_quality_checks.py`

Faire construire ou montrer le pipeline `pl_books_toscrape_end_to_end` :

1. Notebook bronze.
2. Notebook silver.
3. Notebook gold.
4. Notebook qualite.

### 16:35-17:05 - Exposition

Fichiers :

- `usecases/01-books-toscrape/sql-powerbi/queries_books_gold.sql`
- `usecases/01-books-toscrape/sql-powerbi/powerbi_model.md`

### Variante officielle Microsoft Learn

Si le reseau bloque le scraping ou si vous voulez rester strictement sur les labs officiels, utilisez :

- `usecases/02-mslearn-sales-medallion/README.md`
- `usecases/02-mslearn-sales-medallion/03-guide-fabric-pas-a-pas.md`
- `usecases/02-mslearn-sales-medallion/notebooks/`

Montrer :

- SQL analytics endpoint sur tables gold.
- Modele semantique simple.
- Mesures DAX de base.

### 17:05-17:30 - Restitution

Evaluation :

- `04-evaluation/quiz-et-correction.md`
- `04-evaluation/grille-restitution.md`

Faire restituer en 2 minutes par groupe :

- Architecture retenue.
- Tables creees.
- Controle qualite le plus important.
- Amelioration possible si le projet passait en production.
