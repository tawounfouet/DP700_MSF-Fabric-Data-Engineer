# Modele Power BI propose - Sales Medallion

## Tables

- `factsales_gold`
- `dimdate_gold`
- `dimcustomer_gold`
- `dimproduct_gold`

## Relations

| Depuis | Vers | Cardinalite |
| --- | --- | --- |
| `factsales_gold[DateKey]` | `dimdate_gold[DateKey]` | Many-to-one |
| `factsales_gold[CustomerID]` | `dimcustomer_gold[CustomerID]` | Many-to-one |
| `factsales_gold[ProductID]` | `dimproduct_gold[ProductID]` | Many-to-one |

Filtrage recommande : sens unique depuis les dimensions vers le fait.

## Mesures DAX

```DAX
Total Revenue =
SUM ( factsales_gold[LineAmount] )
```

```DAX
Total Quantity =
SUM ( factsales_gold[Quantity] )
```

```DAX
Order Count =
DISTINCTCOUNT ( factsales_gold[SalesOrderNumber] )
```

```DAX
Average Order Line Amount =
AVERAGE ( factsales_gold[LineAmount] )
```

```DAX
Revenue YTD =
TOTALYTD (
    [Total Revenue],
    dimdate_gold[OrderDate]
)
```

## Pages de rapport

Page 1 - Executive overview :

- Carte `Total Revenue`
- Carte `Order Count`
- Carte `Total Quantity`
- Courbe `Total Revenue` par `YearMonth`

Page 2 - Produits :

- Bar chart `Total Revenue` par `ProductName`
- Table `ProductName`, `ProductVariant`, `Total Revenue`, `Total Quantity`

Page 3 - Clients :

- Top clients par revenu
- Table clients avec commandes et revenu

Page 4 - Qualite :

- Table `dq_sales_results`
- Volumes bronze/silver/gold

