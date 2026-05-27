# Checklist de preparation

## Une semaine avant

- Confirmer l'acces etudiant a Microsoft Fabric.
- Verifier que chaque groupe peut creer un workspace associe a une capacite Fabric Trial, Premium ou Fabric.
- Prevoir des groupes de 2 ou 3 si les capacites sont limitees.
- Envoyer les prerequis : bases SQL, Python, notion de DataFrame, notion de schema etoile.
- Tester l'acces reseau a `https://books.toscrape.com/`.
- Verifier que les fichiers Microsoft Learn sont presents dans `usecases/02-mslearn-sales-medallion/data/orders/`.

## La veille

- Ouvrir `README.md` et `01-support-cours/slides-journee.md`.
- Tester le chargement d'un CSV simple dans un lakehouse.
- Tester un notebook Spark minimal.
- Tester l'installation eventuelle des dependances Python dans Fabric :

```python
%pip install beautifulsoup4 requests
```

- Preparer une variante demo si l'installation de dependances est bloquee : executer seulement les cellules deja prêtes ou commenter le scraping et montrer les schemas.

## Nommage recommande

Workspace :

```text
ws-efrei-dp700-books-dev-groupeXX
```

Lakehouse :

```text
lh_books_toscrape
```

Notebooks :

```text
nb_00_setup
nb_01_ingest_books_bronze
nb_02_transform_books_silver
nb_03_build_books_gold
nb_04_data_quality_checks
```

Pipeline :

```text
pl_books_toscrape_end_to_end
```

Modele semantique :

```text
sm_books_analytics
```

Rapport :

```text
rpt_books_catalog_analysis
```

## Variante sans capacite Fabric

Si les comptes n'ont pas de capacite :

- Projeter les visuels et captures dans `assets/`.
- Faire lire les notebooks par groupe et demander de commenter chaque transformation.
- Utiliser le SQL et le DAX comme exercice de conception.
- Evaluer via la grille de restitution.

## Points de vigilance

- Le premier demarrage Spark peut prendre du temps.
- Le SQL analytics endpoint d'un lakehouse expose les tables Delta mais reste lecture seule pour les donnees.
- Les tables creees dans `Files` ne sont pas automatiquement visibles cote SQL endpoint. Les tables analytiques doivent etre creees dans `Tables` via Delta.
- Le scraping appelle environ 50 pages catalogue et jusqu'a 1000 pages detail en mode complet. Pour une demo rapide, limiter `MAX_CATALOG_PAGES` a 3 ou 5.
- Books to Scrape est un site de demonstration : les prix et notes sont fictifs, ce qui est parfait pour l'apprentissage mais pas pour une interpretation metier reelle.
- Le use case Microsoft Learn Sales Medallion est la variante la plus robuste si vous voulez eviter toute dependance web externe pendant l'apres-midi.
