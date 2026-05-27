# 01 - Cadrage metier

## Contexte

Books to Scrape simule un catalogue e-commerce de livres. Le site est pedagogique, statique et concu pour l'entrainement au scraping.

La direction produit veut un premier tableau de bord de catalogue pour comprendre :

- La couverture par categorie.
- La distribution des prix.
- Les livres les mieux notes.
- La disponibilite.
- Les anomalies de parsing.

## Questions analytiques

Questions a traiter en gold :

1. Combien de livres par categorie ?
2. Quel prix moyen par categorie ?
3. Combien de livres par note ?
4. Combien de livres sont disponibles ?
5. Quels livres sont les plus chers ?
6. Quelles categories ont la note moyenne la plus elevee ?

## Contraintes data engineering

- Source HTML paginee.
- Pas de contrat de schema explicite.
- Les champs prix, note et disponibilite doivent etre parses.
- La source peut changer, donc le HTML brut doit etre conserve.
- Les tables analytiques doivent etre Delta pour etre exposees via SQL endpoint et Power BI.

## Definition de reussite

Le use case est reussi si :

- Le bronze contient les pages HTML et un JSONL extrait.
- Le silver contient une table propre, typee et dedupliquee.
- Le gold contient au moins une table catalogue et une table de statistiques categorie.
- Les controles qualite detectent les prix invalides, les notes hors plage et les doublons.
- Le SQL endpoint peut repondre aux questions metier.

