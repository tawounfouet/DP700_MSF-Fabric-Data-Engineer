# TP 01 - Lakehouse, OneLake et SQL endpoint

Durée : 45 minutes.

Objectif : creer un premier lakehouse, charger un fichier, produire une table Delta et l'interroger via SQL.

## Prerequis

- Acces a `https://app.fabric.microsoft.com/`.
- Workspace Fabric avec capacite Trial, Premium ou Fabric.

## Etapes

### 1. Creer le workspace

1. Aller dans Microsoft Fabric.
2. Creer un workspace nomme :

```text
ws-efrei-dp700-intro-groupeXX
```

3. Selectionner une licence/capacite compatible Fabric.

### 2. Creer le lakehouse

1. Dans le workspace, creer un item `Lakehouse`.
2. Nommer le lakehouse :

```text
lh_intro_fabric
```

3. Observer les deux zones :

- `Files`
- `Tables`

### 3. Charger un fichier exemple

Utiliser le fichier Microsoft Learn :

```text
https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/sales.csv
```

1. Dans `Files`, creer un dossier `data`.
2. Charger `sales.csv`.
3. Ouvrir l'aperçu du fichier.

### 4. Creer une table

1. Sur le fichier `sales.csv`, choisir `Load to Tables`.
2. Creer une nouvelle table :

```text
sales
```

3. Verifier que la table apparait dans `Tables`.

### 5. Interroger avec SQL endpoint

Basculer le lakehouse vers `SQL analytics endpoint`.

Executer :

```sql
SELECT
    Item,
    SUM(Quantity * UnitPrice) AS Revenue
FROM sales
GROUP BY Item
ORDER BY Revenue DESC;
```

Puis :

```sql
SELECT
    YEAR(OrderDate) AS OrderYear,
    COUNT(*) AS LineCount,
    SUM(Quantity) AS Quantity
FROM sales
GROUP BY YEAR(OrderDate)
ORDER BY OrderYear;
```

## Questions de debrief

- Quelle difference voyez-vous entre `Files` et `Tables` ?
- Pourquoi la table peut-elle etre interrogee en SQL ?
- Que se passerait-il si le fichier restait uniquement dans `Files` ?
- Dans quel cas utiliseriez-vous un warehouse plutot qu'un lakehouse ?

## Ressources locales utiles

- `../assets/images/mslearn/new-lakehouse.png`
- `../assets/images/mslearn/switch-sql-endpoint.png`
- Lab source : `../../Instructions/Labs/01-lakehouse.md`
