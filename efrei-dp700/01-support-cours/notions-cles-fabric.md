# Notions cles Microsoft Fabric

## Workspace

Un workspace est le conteneur de collaboration, securite et cycle de vie. Pour la journee, chaque groupe cree son propre workspace afin d'isoler les objets et de faciliter le nettoyage.

## OneLake

OneLake est la couche de stockage unifiee. L'idee cle pour les etudiants : les experiences Fabric ne partent pas chacune dans leur silo. Elles travaillent autour d'une meme fondation de donnees.

## Lakehouse

Le lakehouse est le meilleur choix pour le use case Books to Scrape :

- Le bronze contient du HTML et du JSONL.
- Le silver et le gold sont en Delta.
- Les notebooks Spark peuvent transformer.
- Le SQL endpoint peut exposer les tables aux analystes.

## Data Factory

Data Factory dans Fabric apporte deux familles d'outils :

- Pipelines pour l'orchestration.
- Dataflows Gen2 pour l'ETL low-code avec Power Query.

## Notebook

Le notebook est le bon choix pour le scraping et la transformation Spark, car il donne un controle fin sur HTTP, parsing HTML, qualite, schemas et ecriture Delta.

## Warehouse

Le warehouse est pertinent si l'equipe veut surtout du T-SQL complet, des traitements relationnels et une couche gold tres SQL. Dans cette journee, on garde le gold dans le lakehouse pour rester simple, mais on discute l'option "gold en warehouse".

## Modele semantique

Le modele semantique transforme les tables gold en vocabulaire metier : relations, mesures, hierarchies et calculs DAX. C'est la couche la plus lisible pour Power BI.

## Architecture medaillon

Dans Fabric, l'architecture medaillon peut etre implementee avec :

- Un seul lakehouse et des prefixes/tables par couche.
- Un lakehouse par couche.
- Bronze/Silver en lakehouse et Gold en warehouse.

Pour un cours d'une journee, un seul lakehouse est plus simple. En production, la separation par workspace/lakehouse peut ameliorer la gouvernance.

