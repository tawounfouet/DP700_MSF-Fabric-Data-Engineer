# 01 - Cadrage metier

## Contexte

Une equipe commerciale veut analyser ses commandes Adventure Works sur trois annees. Les donnees arrivent sous forme de fichiers CSV annuels.

Le besoin est volontairement proche des labs Microsoft Learn pour que les etudiants puissent relier le TP a DP-700 et DP-601.

## Questions analytiques

1. Quel chiffre d'affaires par an et par mois ?
2. Quels produits generent le plus de revenu ?
3. Quels clients achetent le plus ?
4. Quelle quantite vendue par produit ?
5. Quelle tendance de revenu observe-t-on entre 2019 et 2021 ?

## Contraintes data engineering

- Les fichiers bronze sont sans en-tete.
- Le schema doit etre impose explicitement.
- Les dates, quantites et montants doivent etre types.
- Les donnees doivent etre preparees pour un modele dimensionnel.
- Les tables gold doivent etre consommables en SQL et Power BI.

## Definition de reussite

Le use case est reussi si :

- Les CSV sont conserves dans `Files/bronze/sales/orders`.
- `bronze_sales_orders` trace les lignes source.
- `silver_sales_orders` est propre, typee et dedupliquee.
- `dimdate_gold`, `dimcustomer_gold`, `dimproduct_gold` et `factsales_gold` sont crees.
- Les controles qualite sont stockes dans `dq_sales_results`.
- Les requetes SQL repondent aux questions metier.

