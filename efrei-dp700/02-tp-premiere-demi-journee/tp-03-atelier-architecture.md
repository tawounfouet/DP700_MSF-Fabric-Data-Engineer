# TP 03 - Atelier architecture Fabric

Durée : 25 minutes.

Objectif : choisir une architecture Fabric selon un besoin.

## Scenario

Une librairie en ligne veut analyser son catalogue :

- Nombre de livres par categorie.
- Prix moyen par categorie.
- Disponibilite en stock.
- Distribution des notes.
- Detection des pages mal parsees ou sans prix.

Source : `https://books.toscrape.com/`

Contraintes :

- Le site est pagine.
- Les donnees sont semi-structurees en HTML.
- Les prix et notes sont fictifs.
- L'equipe BI veut un rapport Power BI.
- L'equipe data veut pouvoir rejouer le parsing sans rappeler le site.

## Travail demande

En groupe, proposez :

1. Les items Fabric a creer.
2. Les zones bronze, silver, gold.
3. Les tables attendues.
4. Les controles qualite.
5. L'ordre du pipeline.

## Architecture cible attendue

Comparer votre proposition au schema :

![Architecture medaillon Books](../assets/visuals/books-medallion-architecture.svg)

## Questions bonus

- Feriez-vous un seul lakehouse ou trois lakehouses ?
- Quand utiliseriez-vous un warehouse pour la couche gold ?
- Quels objets doivent etre securises ?
- Quels elements doivent etre monitorés ?

