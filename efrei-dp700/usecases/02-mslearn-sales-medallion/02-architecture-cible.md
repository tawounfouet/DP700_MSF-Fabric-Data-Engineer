# 02 - Architecture cible

## Flux

![Architecture Microsoft Learn Sales medaillon](../../assets/visuals/mslearn-sales-medallion-architecture.svg)

```text
CSV orders Microsoft Learn
        |
        v
Files/bronze/sales/orders
        |
        v
bronze_sales_orders
        |
        v
silver_sales_orders
        |
        v
dimdate_gold + dimcustomer_gold + dimproduct_gold + factsales_gold
        |
        v
SQL analytics endpoint + Power BI
```

## Bronze

Role : conserver les fichiers sources et charger une table technique.

Contenu :

- `Files/bronze/sales/orders/2019.csv`
- `Files/bronze/sales/orders/2020.csv`
- `Files/bronze/sales/orders/2021.csv`
- `bronze_sales_orders`

Colonnes ajoutees :

- `SourceFile`
- `BronzeLoadedTS`

## Silver

Role : nettoyer, typer, enrichir et dedoublonner.

Table :

- `silver_sales_orders`

Transformations :

- Schema explicite.
- Colonnes date `OrderYear`, `OrderMonth`.
- Nettoyage client.
- Revenu calcule : `LineAmount = Quantity * (UnitPrice + Tax)`.
- Rejet implicite des lignes sans commande, date ou produit.

## Gold

Role : construire un schema etoile.

Dimensions :

- `dimdate_gold`
- `dimcustomer_gold`
- `dimproduct_gold`

Fait :

- `factsales_gold`

## Variante production

En production, vous pouvez :

- Orchestrer le depot des fichiers avec un pipeline Copy Data.
- Ajouter une cle de run dans toutes les tables.
- Charger incrementiellement au lieu d'ecraser les tables.
- Ajouter des tests de reconciliation entre bronze, silver et gold.
