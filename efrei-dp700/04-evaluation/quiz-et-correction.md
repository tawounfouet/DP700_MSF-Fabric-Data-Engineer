# Quiz et correction

## Questions

1. Quel est le role principal de OneLake dans Fabric ?
2. Quelle difference principale entre `Files` et `Tables` dans un lakehouse ?
3. Pourquoi le bronze doit-il conserver les donnees brutes ?
4. Pourquoi utiliser Delta en silver et gold ?
5. Quand choisir un notebook plutot qu'un Dataflow Gen2 ?
6. Quel est le role d'un pipeline Fabric ?
7. Le SQL analytics endpoint d'un lakehouse permet-il d'inserer des lignes dans une table Delta ?
8. Dans Books to Scrape, pourquoi les prix ne doivent-ils pas etre interpretes comme des donnees metier reelles ?
9. Donnez deux controles qualite utiles sur `silver_books`.
10. Quelle table gold utiliseriez-vous en priorite pour un rapport Power BI rapide ?

## Correction attendue

1. OneLake fournit une couche de stockage logique unifiee pour les charges de travail Fabric.
2. `Files` stocke des fichiers, `Tables` expose des tables Delta gerees et interrogeables.
3. Pour rejouer, auditer et corriger le parsing sans rappeler la source.
4. Delta apporte transactions, schema, integration Fabric et exposition SQL/Power BI.
5. Quand il faut du code, Spark, des bibliotheques, du scraping ou une logique custom.
6. Orchestrer, parametrer, planifier et monitorer des activites.
7. Non, il est en lecture seule pour modifier les donnees lakehouse.
8. Le site precise que les prix et notes sont fictifs.
9. Exemples : prix non nul et positif, note entre 1 et 5, titre non vide, doublons par URL/UPC.
10. `gold_book_catalog` pour une exploration rapide, ou `gold_category_stats` pour une vue agregée.

