# Modele Power BI propose

## Tables

Modele simple pour rapport rapide :

- `gold_book_catalog`
- `gold_category_stats`

Modele etoile pour discussion data modelling :

- `fact_books_gold`
- `dim_category_gold`
- `dim_rating_gold`

## Relations

| Depuis | Vers | Cardinalite |
| --- | --- | --- |
| `fact_books_gold[category_id]` | `dim_category_gold[category_id]` | Many-to-one |
| `fact_books_gold[rating_value]` | `dim_rating_gold[rating_value]` | Many-to-one |

Filtrage : sens unique depuis les dimensions vers la table de faits.

## Mesures DAX

```DAX
Total Books =
COUNTROWS ( fact_books_gold )
```

```DAX
Average Price GBP =
AVERAGE ( fact_books_gold[price_gbp] )
```

```DAX
Available Books =
CALCULATE (
    COUNTROWS ( fact_books_gold ),
    fact_books_gold[is_available] = TRUE ()
)
```

```DAX
Availability Rate =
DIVIDE ( [Available Books], [Total Books] )
```

```DAX
Five Star Books =
CALCULATE (
    COUNTROWS ( fact_books_gold ),
    fact_books_gold[rating_value] = 5
)
```

```DAX
Average Rating =
AVERAGE ( fact_books_gold[rating_value] )
```

```DAX
High Rated Share =
DIVIDE (
    CALCULATE (
        COUNTROWS ( fact_books_gold ),
        fact_books_gold[rating_value] >= 4
    ),
    [Total Books]
)
```

## Pages de rapport

Page 1 - Catalogue overview :

- Carte `Total Books`
- Carte `Average Price GBP`
- Carte `Availability Rate`
- Bar chart `Total Books` par categorie
- Histogramme `Total Books` par note

Page 2 - Analyse categorie :

- Table categories avec `book_count`, `avg_price_gbp`, `avg_rating`
- Scatter `avg_price_gbp` vs `avg_rating`, taille = `book_count`
- Slicer categorie

Page 3 - Qualite :

- Table `dq_results`
- Statut passed/failed
- Nombre de rejets depuis `silver_books_rejected`

