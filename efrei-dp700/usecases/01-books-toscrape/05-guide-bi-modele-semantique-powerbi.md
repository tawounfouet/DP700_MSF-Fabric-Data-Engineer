# 05 - Guide BI — Du modèle sémantique au rapport Power BI

> **Objectif** : comprendre pourquoi on crée un modèle sémantique, comment le configurer dans Fabric, puis construire un rapport Power BI à partir des tables gold du lakehouse.

---

## Prérequis

Avant de commencer ce guide :

- [x] Le pipeline `pl_books_toscrape_end_to_end` a été exécuté au moins une fois
- [x] Les tables gold existent dans `lh_books_toscrape` :
  - `gold_book_catalog`
  - `gold_category_stats`
  - `fact_books_gold`
  - `dim_category_gold`
  - `dim_rating_gold`

---

## C'est quoi un modèle sémantique ? Et pourquoi en créer un ?

### Sans modèle sémantique

Power BI peut se connecter directement aux tables brutes d'un Lakehouse. Mais alors :

- L'analyste voit des colonnes nommées `category_norm`, `price_excl_tax_gbp`, `gold_processed_ts`... ce n'est pas parlant
- Il n'y a pas de relations entre les tables — impossible de filtrer par catégorie sur la table de faits
- Chaque analyste recalcule les KPIs à sa façon → incohérence entre rapports
- Si une colonne est renommée dans la table, le rapport plante

### Avec un modèle sémantique

Le modèle sémantique est une **couche de traduction** entre la donnée technique et l'utilisateur métier.

```
Lakehouse (technique)          Modèle sémantique (métier)         Rapport Power BI
──────────────────────         ─────────────────────────────      ──────────────────
fact_books_gold        ──►     Table "Livres"                ──►   Graphiques
dim_category_gold      ──►     Table "Catégories"            ──►   Filtres
dim_rating_gold        ──►     Table "Notes"                 ──►   KPIs
                               Relations définies                   Mesures DAX
                               Mesures DAX partagées               réutilisables
                               Noms conviviaux
```

**Concrètement, le modèle sémantique permet de :**
- Définir **une seule fois** le calcul de chaque KPI (ex. taux de disponibilité) → tous les rapports utilisent la même formule
- Créer des **relations** entre tables pour les filtres croisés
- **Renommer** les colonnes en langage métier
- **Masquer** les colonnes techniques inutiles dans les rapports
- Permettre à plusieurs rapports de partager la même source de vérité

> **Analogie** : le Lakehouse est l'entrepôt avec les palettes et les cartons. Le modèle sémantique est le catalogue produits avec les noms, prix affichés, et rayons. Power BI est la vitrine du magasin.

---

## Architecture du modèle sémantique de ce projet

### Deux approches disponibles

**Approche 1 — Modèle simple (recommandé pour démarrer)**

Utilise uniquement `gold_book_catalog` et `gold_category_stats`. Pas de relations à configurer. Idéal pour un premier rapport rapide.

```
gold_book_catalog          gold_category_stats
─────────────────          ───────────────────
book_id                    category
title                      book_count
category           ◄──►    avg_price_gbp
price_gbp                  avg_rating
rating_value               available_books
is_available               availability_rate
price_bucket
```

**Approche 2 — Schéma étoile (recommandé pour comprendre le modelling)**

Utilise `fact_books_gold` + `dim_category_gold` + `dim_rating_gold`. C'est le modèle classique de data warehousing.

```
                    dim_category_gold
                    ─────────────────
                    category_id  ◄──────────────────┐
                    category                        │
                    category_norm                   │ Many-to-one
                                                    │
fact_books_gold                                     │
───────────────                                     │
book_id                                             │
category_id  ──────────────────────────────────────►│
rating_value ──────────────────────────┐
price_gbp                              │ Many-to-one
is_available                           │
available_count                        ▼
ingestion_date          dim_rating_gold
                        ──────────────
                        rating_value
                        rating_label  (One, Two, Three...)
                        rating_band   (Low, Medium, High)
```

> **Ce guide utilise les deux approches** : d'abord le modèle simple pour aller vite, puis le schéma étoile pour la partie avancée.

---

## Partie 1 — Créer le modèle sémantique dans Fabric

### Étape 1 — Accéder au SQL Analytics Endpoint

Le modèle sémantique se crée à partir du SQL Analytics Endpoint du Lakehouse — pas directement depuis les notebooks.

1. Dans le workspace, cliquer sur `lh_books_toscrape`
2. En haut à droite, un menu déroulant affiche **`Lakehouse`**
3. Cliquer sur ce menu → sélectionner **`SQL analytics endpoint`**
4. L'interface change : tu es maintenant dans un environnement SQL avec les tables listées à gauche

> Le SQL analytics endpoint est une vue **read-only** des tables Delta du Lakehouse, exposée via T-SQL. On ne peut pas écrire de données ici, seulement lire.

### Étape 2 — Vérifier que les tables sont bien là

Dans le panneau gauche, sous **Tables**, vérifier la présence de :

- `gold_book_catalog`
- `gold_category_stats`
- `fact_books_gold`
- `dim_category_gold`
- `dim_rating_gold`
- `dq_results`

Si une table manque → retourner dans le Lakehouse, onglet Tables, cliquer **Refresh**.

### Étape 3 — Ouvrir le Model view

1. Dans la barre de navigation en haut, cliquer sur **`Model`** (ou **`Reporting`** selon la version)
2. Tu arrives dans une vue canvas avec les tables représentées sous forme de boîtes

C'est ici que se configure le modèle sémantique : relations, colonnes visibles, mesures DAX.

### Étape 4 — Créer le modèle sémantique (item séparé)

Pour partager le modèle sémantique avec plusieurs rapports, il faut le créer comme un item indépendant.

1. Retourner dans le workspace
2. Cliquer sur **`+ New item`** → **`Semantic model`**
3. Une fenêtre s'ouvre pour choisir la source de données
4. Sélectionner **`lh_books_toscrape`** (le SQL analytics endpoint)
5. Cocher les tables à inclure :
   - [x] `gold_book_catalog`
   - [x] `gold_category_stats`
   - [x] `fact_books_gold`
   - [x] `dim_category_gold`
   - [x] `dim_rating_gold`
   - [x] `dq_results`
6. Cliquer **Confirm**
7. Nommer le modèle :

```text
sm_books_toscrape
```

8. Cliquer **Create**

---

## Partie 2 — Configurer les relations (schéma étoile)

### Pourquoi les relations sont importantes

Sans relation, si l'utilisateur filtre par catégorie "Mystery", Power BI ne sait pas que ça doit filtrer aussi la table `fact_books_gold`. Les relations définissent ces **filtres croisés automatiques**.

### Créer la relation fact → dim_category

1. Dans le Model view du modèle sémantique, repérer les deux tables `fact_books_gold` et `dim_category_gold`
2. **Cliquer-glisser** la colonne `category_id` de `fact_books_gold` vers la colonne `category_id` de `dim_category_gold`
3. Une fenêtre de configuration apparaît :

| Paramètre | Valeur à choisir |
|---|---|
| **From table** | `fact_books_gold` |
| **From column** | `category_id` |
| **To table** | `dim_category_gold` |
| **To column** | `category_id` |
| **Cardinality** | `Many to one (*)` |
| **Cross filter direction** | `Single` (de dim vers fact) |

4. Cliquer **OK / Confirm**

> **Cardinalité Many-to-one** : plusieurs livres (`fact_books_gold`) peuvent appartenir à la même catégorie (`dim_category_gold`), mais une catégorie est unique dans la dimension. C'est la règle de base du schéma étoile.

### Créer la relation fact → dim_rating

Répéter la même opération :

1. Glisser `rating_value` de `fact_books_gold` vers `rating_value` de `dim_rating_gold`
2. Configuration :

| Paramètre | Valeur |
|---|---|
| **Cardinality** | `Many to one (*)` |
| **Cross filter direction** | `Single` |

3. Cliquer **OK**

### Résultat attendu

Le canvas doit montrer :

```
dim_category_gold ──────────────── fact_books_gold ──────────────── dim_rating_gold
  [category_id]   1            *   [category_id]   *            1   [rating_value]
                                   [rating_value]
```

Les chiffres `1` et `*` sur les lignes de relation indiquent la cardinalité.

---

## Partie 3 — Créer les mesures DAX

### C'est quoi une mesure DAX ?

Une **mesure DAX** est un calcul nommé et réutilisable. Au lieu que chaque rapport recalcule "le nombre de livres disponibles" à sa manière, on le définit une seule fois dans le modèle.

**DAX** (Data Analysis Expressions) est le langage de calcul de Power BI / Fabric.

### Où créer les mesures

Dans le Model view du modèle sémantique :
1. Cliquer sur la table `fact_books_gold` pour la sélectionner
2. Dans la barre d'outils, cliquer **`New measure`**
3. Une barre de formule s'ouvre en haut du canvas

### Mesure 1 — Total Books

```DAX
Total Books =
COUNTROWS ( fact_books_gold )
```

> Compte simplement le nombre total de lignes dans la table de faits = nombre de livres.

### Mesure 2 — Average Price GBP

```DAX
Average Price GBP =
AVERAGE ( fact_books_gold[price_gbp] )
```

### Mesure 3 — Available Books

```DAX
Available Books =
CALCULATE (
    COUNTROWS ( fact_books_gold ),
    fact_books_gold[is_available] = TRUE ()
)
```

> `CALCULATE` applique un filtre avant de calculer. Ici : compter les lignes **où** `is_available` est `TRUE`.

### Mesure 4 — Availability Rate

```DAX
Availability Rate =
DIVIDE ( [Available Books], [Total Books] )
```

> `DIVIDE` au lieu de `/` pour éviter une erreur de division par zéro. Retourne 0 si le dénominateur est 0.

### Mesure 5 — Five Star Books

```DAX
Five Star Books =
CALCULATE (
    COUNTROWS ( fact_books_gold ),
    fact_books_gold[rating_value] = 5
)
```

### Mesure 6 — Average Rating

```DAX
Average Rating =
AVERAGE ( fact_books_gold[rating_value] )
```

### Mesure 7 — High Rated Share

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

> Part des livres notés 4 ou 5 étoiles sur le total.

### Après avoir saisi chaque mesure

- Appuyer sur **Entrée** ou cliquer la coche ✓ pour valider
- La mesure apparaît dans la liste des colonnes de la table avec une icône **∑** (calculatrice)

---

## Partie 4 — Créer le rapport Power BI

### Étape 1 — Créer un nouveau rapport depuis le modèle sémantique

1. Dans le workspace, retrouver l'item `sm_books_toscrape`
2. Cliquer sur les **trois points `...`** à droite de l'item
3. Sélectionner **`Create report`** (ou **`Auto-create report`** pour un premier brouillon automatique)
4. Power BI s'ouvre avec un canvas vide à gauche et le panneau **Fields** à droite (toutes les tables et colonnes du modèle)

> **Alternative** : cliquer sur `sm_books_toscrape` → bouton **`Create report`** dans la barre d'outils.

### Étape 2 — Nommer et sauvegarder le rapport

Avant de commencer, sauvegarder :
1. **Fichier** → **Save**
2. Nom :

```text
rpt_books_toscrape_catalogue
```

---

## Partie 5 — Construire les 3 pages du rapport

### PAGE 1 — Vue d'ensemble du catalogue

**But** : donner une vision globale du dataset en quelques chiffres clés et graphiques.

#### Renommer la page

Double-cliquer sur l'onglet `Page 1` en bas → taper `Catalogue Overview`

#### Visuel 1 — Carte "Total Books"

1. Cliquer sur une zone vide du canvas
2. Dans le panneau **Visualizations** (droite), cliquer l'icône **Card** (rectangle avec un chiffre)
3. Dans le panneau **Fields**, glisser la mesure **`Total Books`** dans le champ **Fields** de la carte
4. Redimensionner et placer en haut à gauche

#### Visuel 2 — Carte "Average Price GBP"

Même procédure avec la mesure **`Average Price GBP`**. Placer à côté de la première carte.

#### Visuel 3 — Carte "Availability Rate"

Même procédure avec **`Availability Rate`**.

> **Astuce formatage** : cliquer sur la carte → onglet **Format** dans Visualizations → **Data label** → changer le format en **Percentage** pour `Availability Rate`.

#### Visuel 4 — Bar chart "Livres par catégorie"

1. Cliquer sur une zone vide
2. Choisir **Clustered bar chart** dans Visualizations
3. Glisser les champs :
   - **Y-axis** : `dim_category_gold[category]`
   - **X-axis** : mesure `Total Books`
4. Dans **Format** → trier par `Total Books` décroissant

#### Visuel 5 — Histogramme "Distribution des notes"

1. Choisir **Clustered column chart**
2. Glisser :
   - **X-axis** : `dim_rating_gold[rating_label]`
   - **Y-axis** : mesure `Total Books`
   - **Legend** : `dim_rating_gold[rating_band]` (pour colorier Low/Medium/High)

---

### PAGE 2 — Analyse par catégorie

**But** : permettre l'exploration des catégories avec des filtres.

#### Créer la page

Cliquer sur **`+`** en bas à côté de `Catalogue Overview` → renommer `Analyse Catégorie`

#### Visuel 1 — Slicer catégorie

1. Choisir **Slicer** dans Visualizations
2. Glisser `dim_category_gold[category]` dans **Field**
3. Placer à gauche en colonne verticale

> Le slicer permet de filtrer **tous les autres visuels** de la page par catégorie sélectionnée.

#### Visuel 2 — Table des catégories

1. Choisir **Table**
2. Glisser les colonnes :
   - `gold_category_stats[category]`
   - `gold_category_stats[book_count]`
   - `gold_category_stats[avg_price_gbp]`
   - `gold_category_stats[avg_rating]`
   - `gold_category_stats[availability_rate]`
3. Trier par `book_count` décroissant

#### Visuel 3 — Scatter plot prix vs note

1. Choisir **Scatter chart**
2. Glisser :
   - **X-axis** : `gold_category_stats[avg_price_gbp]`
   - **Y-axis** : `gold_category_stats[avg_rating]`
   - **Size** : `gold_category_stats[book_count]`
   - **Details** : `gold_category_stats[category]`

> Ce graphique révèle si les livres chers sont mieux notés. Chaque bulle = une catégorie, la taille = le nombre de livres.

---

### PAGE 3 — Qualité des données

**But** : vérifier la santé du pipeline grâce aux résultats de `nb_04_data_quality_checks`.

#### Créer la page

Cliquer sur **`+`** → renommer `Qualité Données`

#### Visuel 1 — Carte nombre de checks critiques échoués

1. **Card**
2. Créer une mesure rapide :

```DAX
Critical Failures =
CALCULATE (
    COUNTROWS ( dq_results ),
    dq_results[severity] = "critical",
    dq_results[passed] = FALSE ()
)
```

3. Glisser cette mesure dans la carte
4. **Format** → colorer en rouge si valeur > 0 (via **Conditional formatting**)

#### Visuel 2 — Table des checks qualité

1. **Table**
2. Colonnes :
   - `dq_results[check_name]`
   - `dq_results[severity]`
   - `dq_results[passed]`
   - `dq_results[metric_value]`
   - `dq_results[details]`
3. **Format** → **Conditional formatting** sur `passed` : vert si TRUE, rouge si FALSE

#### Visuel 3 — Carte nombre de livres rejetés

Si la table `silver_books_rejected` est dans le modèle :

```DAX
Rejected Books =
COUNTROWS ( silver_books_rejected )
```

---

## Partie 6 — Publier et partager

### Sauvegarder le rapport final

`Ctrl+S` → le rapport est sauvegardé dans le workspace Fabric.

### Partager le rapport

1. Dans le workspace, retrouver `rpt_books_toscrape_catalogue`
2. Cliquer **`Share`** → saisir les emails des destinataires
3. Choisir les permissions : **Can view** (lecture seule) ou **Can edit**

### Configurer le rafraîchissement automatique

Le modèle sémantique peut se rafraîchir automatiquement après chaque run du pipeline :

1. Dans le workspace, cliquer sur les **`...`** de `sm_books_toscrape`
2. **Settings** → **Scheduled refresh**
3. Activer et configurer la fréquence (ex. quotidien à 07:00)

> **Bonne pratique** : planifier le pipeline à 06:00, le refresh du modèle à 06:45. Le rapport est toujours à jour quand les analystes arrivent le matin.

---

## Résumé de la chaîne complète

```
[HTTP : books.toscrape.com]
           │
           ▼
    nb_01 (Bronze)
    ── HTML brut + JSON Lines ──► lh_books_toscrape/Files/bronze/
    ── tables bronze            ──► lh_books_toscrape/Tables/
           │
           ▼
    nb_02 (Silver)
    ── nettoyage / typage ──► silver_books, silver_categories, silver_books_rejected
           │
           ▼
    nb_03 (Gold)
    ── agrégation / star schema ──► gold_book_catalog, gold_category_stats
                                    fact_books_gold, dim_category_gold, dim_rating_gold
           │
           ▼
    nb_04 (Data Quality)
    ── contrôles ──► dq_results
           │
           ▼
    SQL Analytics Endpoint (auto-généré par Fabric)
           │
           ▼
    Modèle sémantique : sm_books_toscrape
    ── relations définies ──► fact ↔ dim_category, fact ↔ dim_rating
    ── mesures DAX        ──► Total Books, Avg Price, Availability Rate...
           │
           ▼
    Rapport Power BI : rpt_books_toscrape_catalogue
    ── Page 1 : Catalogue Overview (KPIs, bar chart, histogramme)
    ── Page 2 : Analyse Catégorie (scatter, table, slicer)
    ── Page 3 : Qualité Données   (checks DQ, rejets)
```

---

## Erreurs fréquentes et solutions

| Erreur | Cause | Solution |
|---|---|---|
| Tables absentes dans le modèle sémantique | Tables pas encore créées dans le Lakehouse | Exécuter le pipeline complet d'abord |
| Relation impossible à créer | Colonne de jointure de type différent dans les deux tables | Vérifier que `category_id` est bien du même type dans `fact_books_gold` et `dim_category_gold` |
| Les filtres du slicer n'affectent pas les autres visuels | Relations manquantes ou sens de filtre incorrect | Vérifier dans Model view que `Cross filter direction` est bien configuré |
| Mesure DAX retourne BLANK | Filtre trop restrictif ou table vide | Vérifier que les données existent : `COUNTROWS(table)` dans une carte |
| Le rapport ne se rafraîchit pas | Scheduled refresh désactivé ou pipeline non planifié | Vérifier les settings du modèle sémantique ET du pipeline |
| `Availability Rate` affiche un nombre et pas un % | Format de la mesure non configuré | Cliquer sur la mesure → Format → Percentage |
