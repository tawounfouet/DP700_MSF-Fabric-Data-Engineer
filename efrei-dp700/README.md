# EFREI DP-700 - Journee Microsoft Fabric

Kit d'animation pour une journee Master 2 EFREI autour de Microsoft Fabric, orientee DP-700 et data engineering.

Objectif de la journee : donner une vue d'ensemble solide de Fabric le matin, puis faire construire l'apres-midi une mini data platform end-to-end a partir du site pedagogique [Books to Scrape](https://books.toscrape.com/) avec une architecture medaillon.

## Public

- Etudiants Master 2 avec bases SQL, Python et architecture data.
- Niveau attendu : savoir lire un script Python, comprendre une table, un pipeline et un modele analytique.
- Capacite Fabric requise pour les TP : Trial, Premium ou Fabric.

## Objectifs pedagogiques

A la fin de la journee, les etudiants doivent savoir :

- Expliquer les experiences principales de Microsoft Fabric : Data Engineering, Data Factory, Data Warehouse, Real-Time Intelligence, Power BI, OneLake.
- Distinguer Lakehouse, Warehouse, SQL analytics endpoint, notebook, pipeline et Dataflow Gen2.
- Choisir entre notebook, pipeline, Dataflow Gen2, T-SQL et Spark selon le besoin.
- Concevoir une architecture medaillon bronze, silver, gold.
- Implementer un flux end-to-end : ingestion web, stockage brut, transformation, qualite, tables gold, exposition SQL et Power BI.
- Relier ces pratiques aux domaines DP-700 : ingestion/transformation, orchestration, securite/gouvernance, monitoring/optimisation.

## Organisation du dossier

| Dossier | Contenu |
| --- | --- |
| `00-facilitateur/` | Deroule minute, checklist, conseils d'animation |
| `01-support-cours/` | Supports Markdown utilisables comme trame de slides |
| `02-tp-premiere-demi-journee/` | TP courts pour decouvrir workspace, lakehouse, SQL endpoint, pipeline et notebooks |
| `usecases/` | Deux use cases end-to-end : Books to Scrape et Microsoft Learn Sales Medallion |
| `04-evaluation/` | Quiz, grille de restitution, criteres de reussite |
| `assets/visuals/` | Schemas SVG originaux pour projeter ou integrer aux supports |
| `assets/images/mslearn/` | Captures locales selectionnees depuis les labs Microsoft Learn du depot |
| `99-sources/` | Sources locales et liens web consultes |

## Deroule recommande

| Horaire | Sequence | Format |
| --- | --- | --- |
| 09:00-09:20 | Cadrage : pourquoi Fabric, pourquoi DP-700 | Discussion guidee |
| 09:20-10:10 | Vue d'ensemble Fabric, OneLake, Lakehouse, Warehouse | Cours avec visuels |
| 10:10-10:25 | Pause |  |
| 10:25-11:20 | TP 1 : workspace, lakehouse, fichier, table, SQL endpoint | Hands-on |
| 11:20-12:15 | TP 2 : ingestion, Dataflow Gen2, pipeline, notebook | Hands-on + debrief |
| 12:15-13:30 | Pause dejeuner |  |
| 13:30-14:00 | Cadrage metier Books to Scrape et architecture cible | Atelier architecture |
| 14:00-15:15 | Bronze + Silver : scraping, raw HTML/JSONL, nettoyage Delta | Notebook guide |
| 15:15-15:30 | Pause |  |
| 15:30-16:35 | Gold + qualite + orchestration pipeline | Notebook + pipeline |
| 16:35-17:05 | SQL endpoint, modele semantique, mesures Power BI | Demo ou hands-on |
| 17:05-17:30 | Restitution, quiz, liens DP-700 | Evaluation |

## Visuels principaux

- [Vue end-to-end Fabric](assets/visuals/fabric-end-to-end.svg)
- [Architecture Books to Scrape medaillon](assets/visuals/books-medallion-architecture.svg)
- [Architecture Microsoft Learn Sales medaillon](assets/visuals/mslearn-sales-medallion-architecture.svg)
- [Workspace Fabric cible](assets/visuals/fabric-workspace-items.svg)
- [Schema etoile Books](assets/visuals/books-star-schema.svg)
- [Timeline de la journee](assets/visuals/day-timeline.svg)

## Preparation rapide

1. Verifier l'acces a [Microsoft Fabric](https://app.fabric.microsoft.com/).
2. Verifier qu'un workspace peut etre cree avec une capacite Fabric.
3. Tester l'ouverture de [Books to Scrape](https://books.toscrape.com/) depuis le reseau de l'ecole.
4. Prevoir une variante demo si les comptes etudiants n'ont pas de capacite Fabric.
5. Garder les notebooks dans `usecases/01-books-toscrape/notebooks/` ou `usecases/02-mslearn-sales-medallion/notebooks/` ouverts dans l'IDE pour copier les cellules dans Fabric.

## Use cases disponibles

- [Books to Scrape](usecases/01-books-toscrape/README.md) : source web semi-structuree, scraping, HTML brut, JSONL, qualite, gold BI.
- [Microsoft Learn Sales Medallion](usecases/02-mslearn-sales-medallion/README.md) : exemple officiel Microsoft Learn avec CSV de ventes, Delta, silver/gold et schema etoile.

## Recommandation d'animation

Le matin, ne pas essayer de couvrir tout DP-700. Il faut donner une carte mentale de Fabric et faire manipuler les objets essentiels.

L'apres-midi, faire vivre le projet comme une vraie mini plateforme : nommage, zones, audit, qualite, orchestration, exposition. C'est ce qui transforme un simple notebook de scraping en experience data engineering.
