# 06 - Guide d'exécution des notebooks — Prérequis, erreurs à éviter, debugging

> **À lire avant de toucher quoi que ce soit.** Ce guide couvre les prérequis à vérifier avant chaque notebook, les erreurs classiques, les points d'attention extraits du code réel, et les méthodes de debugging.

---

## Règle d'or : l'ordre d'exécution est absolu

Les notebooks ont des **dépendances strictes**. Chaque notebook lit ce que le précédent a écrit.

```
nb_01  →  nb_02  →  nb_03  →  nb_04
```

**Ne jamais sauter une étape.** Si nb_02 plante, corriger le problème et le relancer — pas passer à nb_03.

---

## Checklist globale — avant de commencer quoi que ce soit

Avant de lancer le premier notebook, vérifier une fois pour toutes :

- [ ] Le workspace est bien associé à une capacité Fabric (pas Trial expiré)
- [ ] Le lakehouse `lh_books_toscrape` existe dans le workspace
- [ ] Chaque notebook a bien `lh_books_toscrape` comme **lakehouse par défaut** (Explorer → icône lakehouse → pastille verte)
- [ ] On est sur une connexion avec accès Internet (les notebooks Fabric peuvent appeler des URLs externes)

---

## nb_01 — Ingestion Bronze (scraping)

### Prérequis avant d'exécuter

| Prérequis | Comment vérifier |
|---|---|
| Lakehouse attaché | Explorer gauche → `lh_books_toscrape` visible avec pastille verte |
| Librairies installées | Voir étape ci-dessous |
| Site accessible | Tester `https://books.toscrape.com/` dans un navigateur |

### ⚠️ Installer les librairies EN PREMIER — cellule séparée

Le notebook utilise `requests` et `beautifulsoup4`, qui ne sont pas dans l'environnement Spark par défaut. **Avant d'exécuter le reste**, ajouter et exécuter cette cellule en tout premier :

```python
%pip install beautifulsoup4 requests
```

> **Pourquoi une cellule séparée ?** Le `%pip install` redémarre le kernel Python après installation. Si tu le mets dans la même cellule que le reste du code, le reste s'exécute avant que les librairies soient disponibles → `ModuleNotFoundError`.

### Points d'attention dans le code

**1. `MAX_CATALOG_PAGES` — commencer petit**

```python
MAX_CATALOG_PAGES = 5   # ← mode classe : ~100 livres, ~2 min
# MAX_CATALOG_PAGES = 50  # mode complet : ~1000 livres, ~15 min
```

Ne pas lancer avec `50` la première fois. Valider d'abord que le pipeline fonctionne avec `5`.

**2. `RUN_ID` — chaque exécution est unique**

```python
RUN_ID = str(uuid.uuid4())
```

Chaque run du notebook génère un identifiant unique. Cela signifie que si tu relances le notebook deux fois dans la même journée, tu as **deux partitions** dans le bronze :

```
Files/bronze/books_toscrape/raw_json/ingestion_date=2024-01-15/books.jsonl  ← premier run
Files/bronze/books_toscrape/raw_json/ingestion_date=2024-01-15/books.jsonl  ← même fichier écrasé
```

Le fichier JSONL est **écrasé** à chaque run (même date = même chemin). La table `audit_ingestion_runs` elle est en **append** — elle accumule les runs.

**3. `INGESTION_DATE` — calculé au moment du run**

```python
INGESTION_TS = datetime.now(timezone.utc)
INGESTION_DATE = INGESTION_TS.date().isoformat()
```

Si tu lances le notebook à 23h59 et qu'il tourne jusqu'à 00h01, le fichier sera daté d'aujourd'hui mais certains enregistrements auront un timestamp de demain. Pas un problème en TP, à noter en prod.

**4. La table `audit_ingestion_runs` s'accumule**

```python
spark.createDataFrame(audit).write.format("delta").mode("append").saveAsTable("audit_ingestion_runs")
```

Mode `append` : chaque exécution ajoute une ligne. Si tu lances 10 fois le notebook, tu auras 10 lignes. C'est voulu (traçabilité), mais cela peut surprendre.

### ✅ Vérification avant de passer à nb_02

Exécuter ces contrôles dans une nouvelle cellule après le run :

```python
# Vérification 1 — Le fichier JSONL existe
import os
jsonl_path = f"/lakehouse/default/Files/bronze/books_toscrape/raw_json/ingestion_date={INGESTION_DATE}/books.jsonl"
assert os.path.exists(jsonl_path), f"ERREUR : fichier introuvable → {jsonl_path}"
print(f"✅ Fichier JSONL trouvé : {jsonl_path}")

# Vérification 2 — Il contient des données
line_count = sum(1 for _ in open(jsonl_path, encoding="utf-8"))
assert line_count > 0, "ERREUR : fichier JSONL vide"
print(f"✅ {line_count} lignes dans le JSONL")

# Vérification 3 — La table audit existe
audit_count = spark.table("audit_ingestion_runs").count()
print(f"✅ audit_ingestion_runs : {audit_count} run(s) enregistré(s)")
```

**Résultat attendu avec `MAX_CATALOG_PAGES = 5` :**

```
✅ Fichier JSONL trouvé : ...
✅ 100 lignes dans le JSONL   (environ, 20 livres × 5 pages)
✅ audit_ingestion_runs : 1 run(s) enregistré(s)
```

### 🔴 Erreurs fréquentes et solutions

| Message d'erreur | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'bs4'` | `%pip install` non exécuté | Exécuter la cellule `%pip install beautifulsoup4 requests` **seule**, puis relancer |
| `ModuleNotFoundError: No module named 'requests'` | Même cause | Même solution |
| `FileNotFoundError: /lakehouse/default/Files` | Lakehouse non attaché | Ouvrir l'Explorer → attacher `lh_books_toscrape` comme default lakehouse |
| `ConnectionError` ou `requests.exceptions.ConnectionError` | Site inaccessible ou pas d'Internet | Vérifier la connexion ; le site sandbox peut être temporairement down |
| `HTTPError: 429 Too Many Requests` | Trop de requêtes trop vite | Augmenter `REQUEST_SLEEP_SECONDS` à `0.5` ou `1.0` |
| `0 books written` | `MAX_CATALOG_PAGES = 0` ou site vide | Vérifier la valeur de `MAX_CATALOG_PAGES` |
| `AnalysisException: Table audit_ingestion_runs not found` | N'arrive pas sur nb_01, mais sur nb_04 si nb_01 n'a pas tourné | Relancer nb_01 |

### 🔍 Méthode de debug nb_01

**Tester le scraping sur une seule page avant tout :**

```python
# Debug : tester que le scraping fonctionne sur 1 page
import requests
from bs4 import BeautifulSoup

test_session = requests.Session()
test_session.headers.update({"User-Agent": "EFREI-DP700-Fabric-Teaching/1.0"})

resp = test_session.get("https://books.toscrape.com/", timeout=30)
print(f"Status: {resp.status_code}")  # doit afficher 200

soup = BeautifulSoup(resp.text, "html.parser")
cards = soup.select("article.product_pod")
print(f"Livres sur la page 1 : {len(cards)}")  # doit afficher 20
```

**Inspecter le JSONL brut :**

```python
import json
with open(jsonl_path, encoding="utf-8") as f:
    first_record = json.loads(f.readline())
print(json.dumps(first_record, indent=2, ensure_ascii=False))
```

---

## nb_02 — Transformation Silver

### Prérequis avant d'exécuter

| Prérequis | Comment vérifier |
|---|---|
| nb_01 exécuté avec succès | Fichier JSONL présent dans `Files/bronze/books_toscrape/raw_json/` |
| Lakehouse attaché | Idem nb_01 |

```python
# Vérifier que le bronze existe avant de lancer nb_02
from pathlib import Path
bronze_root = Path("/lakehouse/default/Files/bronze/books_toscrape/raw_json")
dates = list(bronze_root.glob("ingestion_date=*"))
print(f"Partitions bronze disponibles : {[d.name for d in dates]}")
# Attendu : ['ingestion_date=2024-01-15'] (au moins une)
```

### Points d'attention dans le code

**1. Le notebook prend automatiquement la dernière date**

```python
available_dates = sorted(...)
INGESTION_DATE = available_dates[-1]   # ← toujours la plus récente
```

Si tu as exécuté nb_01 plusieurs jours de suite, nb_02 prendra toujours le dernier jour. C'est voulu — mais si tu veux rejouer une date spécifique, il faut forcer :

```python
INGESTION_DATE = "2024-01-10"   # forcer une date précise si besoin
```

**2. Trois tables écrites en mode overwrite**

```python
silver_books.write.format("delta").mode("overwrite").saveAsTable("silver_books")
silver_categories.write.format("delta").mode("overwrite").saveAsTable("silver_categories")
rejected_df.write.format("delta").mode("overwrite").saveAsTable("silver_books_rejected")
```

`overwrite` : chaque relance **remplace** le contenu. Pas d'accumulation ici, contrairement à nb_01.

**3. Le `rating_map` — les valeurs inattendues deviennent NULL**

```python
rating_pairs = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
```

Si le site renvoie une valeur différente de ces 5 mots exacts (ex. `"one"` en minuscule ou `""` vide), `rating_value` sera `NULL` et le livre sera **rejeté**. Vérifier `silver_books_rejected` si la conversion silver est faible.

**4. Déduplication sur `source_url`**

```python
.dropDuplicates(["source_url"])
```

Si nb_01 a été lancé deux fois le même jour (fichier JSONL écrasé), les livres ne sont pas dupliqués dans silver. Mais si deux runs produisent des JSONLs distincts et que nb_02 les lit tous → doublons possibles. Ne pas fusionner manuellement des JSONLs de dates différentes.

### ✅ Vérification avant de passer à nb_03

```python
# Vérification après nb_02
silver_count = spark.table("silver_books").count()
rejected_count = spark.table("silver_books_rejected").count()
categories_count = spark.table("silver_categories").count()

print(f"✅ silver_books       : {silver_count} lignes")
print(f"⚠️  silver_books_rejected : {rejected_count} lignes rejetées")
print(f"✅ silver_categories  : {categories_count} catégories")

# Seuil d'alerte : si plus de 10% de rejet, quelque chose cloche
if silver_count > 0:
    reject_rate = rejected_count / (silver_count + rejected_count)
    if reject_rate > 0.10:
        print(f"🔴 ATTENTION : taux de rejet élevé ({reject_rate:.1%}) — inspecter silver_books_rejected")
    else:
        print(f"✅ Taux de rejet acceptable : {reject_rate:.1%}")
```

**Résultat attendu avec `MAX_CATALOG_PAGES = 5` :**

```
✅ silver_books       : ~100 lignes
⚠️  silver_books_rejected : 0 lignes rejetées
✅ silver_categories  : entre 10 et 20 catégories
✅ Taux de rejet acceptable : 0.0%
```

### 🔴 Erreurs fréquentes et solutions

| Message d'erreur | Cause | Solution |
|---|---|---|
| `ValueError: Aucune ingestion bronze trouvee` | nb_01 n'a pas tourné ou le chemin est différent | Vérifier que `Files/bronze/books_toscrape/raw_json/` contient au moins un dossier `ingestion_date=*` |
| `AnalysisException: Path does not exist: Files/bronze/...` | Lakehouse non attaché ou chemin incorrect | Vérifier l'attachement du lakehouse |
| `silver_books` contient 0 lignes | Tous les livres rejetés | Inspecter `silver_books_rejected` pour la `reject_reason` |
| `silver_books` contient beaucoup moins que prévu | Déduplication agressive ou données incomplètes | Inspecter le JSONL brut, vérifier que nb_01 a bien écrit tous les livres |
| `rating_value` est NULL pour tous les livres | Valeurs de `rating_text` inattendues | Inspecter : `spark.table("silver_books_rejected").select("rating_text", "reject_reason").show()` |

### 🔍 Méthode de debug nb_02

**Inspecter les livres rejetés :**

```python
display(
    spark.table("silver_books_rejected")
    .select("title", "rating_text", "price_text", "reject_reason")
    .limit(20)
)
```

**Vérifier les valeurs brutes du JSONL avant transformation :**

```python
raw_df = spark.read.json(SOURCE_PATH)
print(f"Colonnes disponibles : {raw_df.columns}")
raw_df.select("rating_text", "price_text", "availability_text").distinct().show(20)
```

**Vérifier que les prix ont bien été parsés :**

```python
spark.table("silver_books") \
    .select("title", "price_gbp", "price_text") \
    .filter(F.col("price_gbp").isNull()) \
    .show(10)
# Si des lignes apparaissent → le regex n'a pas matché le format du prix
```

---

## nb_03 — Construction Gold

### Prérequis avant d'exécuter

| Prérequis | Comment vérifier |
|---|---|
| nb_02 exécuté avec succès | Tables `silver_books` et `silver_categories` existent |
| silver_books non vide | `spark.table("silver_books").count() > 0` |

```python
# Vérifier les prérequis avant de lancer nb_03
assert spark.catalog.tableExists("silver_books"), "🔴 silver_books introuvable — relancer nb_02"
assert spark.catalog.tableExists("silver_categories"), "🔴 silver_categories introuvable — relancer nb_02"
assert spark.table("silver_books").count() > 0, "🔴 silver_books est vide — relancer nb_02"
print("✅ Prérequis nb_03 validés")
```

### Points d'attention dans le code

**1. `spark.table()` résout vers le lakehouse par défaut**

```python
silver_books = spark.table("silver_books")
```

Pas de chemin absolu — si le lakehouse n'est pas attaché ou si le nom de la table est différent → `AnalysisException`.

**2. La jointure `fact_books_gold` est un `left join`**

```python
.join(dim_category_gold.alias("c"), F.col("b.category_norm") == F.col("c.category_norm"), "left")
```

Résultat : **tous les livres** sont conservés dans `fact_books_gold`, même si leur catégorie est inconnue (`category_id` sera NULL pour ces livres). C'est voulu — ne pas changer en `inner join` sinon des livres disparaissent.

**3. `dim_rating_gold` est codée en dur — pas une lecture de table**

```python
dim_rating_gold = spark.createDataFrame(
    [(1, "One", "Low"), (2, "Two", "Low"), (3, "Three", "Medium"), (4, "Four", "High"), (5, "Five", "High")],
    ["rating_value", "rating_label", "rating_band"]
)
```

Cette table a **toujours exactement 5 lignes**, peu importe les données. Elle représente un référentiel statique.

**4. Toutes les tables gold sont en `overwrite`**

Relancer nb_03 est sans danger : les tables gold sont entièrement reconstruites à chaque fois.

### ✅ Vérification avant de passer à nb_04

```python
# Vérification après nb_03
silver_count = spark.table("silver_books").count()
gold_catalog_count = spark.table("gold_book_catalog").count()
gold_stats_count = spark.table("gold_category_stats").count()
fact_count = spark.table("fact_books_gold").count()
dim_cat_count = spark.table("dim_category_gold").count()
dim_rating_count = spark.table("dim_rating_gold").count()

print(f"silver_books         : {silver_count}")
print(f"gold_book_catalog    : {gold_catalog_count}   (doit = silver)")
print(f"fact_books_gold      : {fact_count}   (doit = silver)")
print(f"gold_category_stats  : {gold_stats_count} catégories")
print(f"dim_category_gold    : {dim_cat_count} catégories")
print(f"dim_rating_gold      : {dim_rating_count}   (doit = 5)")

# Contrôles critiques
assert gold_catalog_count == silver_count, f"🔴 Écart gold/silver : {gold_catalog_count} vs {silver_count}"
assert fact_count == silver_count, f"🔴 Écart fact/silver : {fact_count} vs {silver_count}"
assert dim_rating_count == 5, f"🔴 dim_rating_gold doit avoir 5 lignes, a {dim_rating_count}"
print("✅ Tous les contrôles gold sont OK")
```

**Résultat attendu :**

```
silver_books         : 100
gold_book_catalog    : 100   ✅ (doit = silver)
fact_books_gold      : 100   ✅ (doit = silver)
gold_category_stats  : 15 catégories
dim_category_gold    : 15 catégories
dim_rating_gold      : 5    ✅ (doit = 5)
✅ Tous les contrôles gold sont OK
```

### 🔴 Erreurs fréquentes et solutions

| Message d'erreur | Cause | Solution |
|---|---|---|
| `AnalysisException: Table or view not found: silver_books` | nb_02 non exécuté ou lakehouse non attaché | Vérifier prérequis, relancer nb_02 |
| `gold_book_catalog` count < `silver_books` count | Perte de lignes dans la sélection ou le join | Inspecter : vérifier les colonnes sélectionnées dans `silver_books.select(...)` |
| `fact_books_gold` count > `silver_books` count | Join qui multiplie les lignes (fanout) | Impossible avec ce code (`left join` sur clé unique dans dim) — si ça arrive, vérifier que `category_norm` est unique dans `dim_category_gold` |
| `dim_rating_gold` absent dans les tables | Lakehouse non attaché | Vérifier l'attachement |

### 🔍 Méthode de debug nb_03

**Vérifier l'intégrité de la jointure fact ↔ dim_category :**

```python
# Livres sans catégorie dans la fact (category_id NULL après le left join)
orphan_books = spark.table("fact_books_gold").filter(F.col("category_id").isNull())
print(f"Livres sans catégorie : {orphan_books.count()}")
# Résultat normal : 0 — si > 0, inspecter silver_categories
```

**Vérifier les buckets de prix :**

```python
spark.table("gold_book_catalog") \
    .groupBy("price_bucket") \
    .count() \
    .orderBy("price_bucket") \
    .show()
# Attendu : 4 buckets (0-15, 15-30, 30-45, 45+)
```

---

## nb_04 — Data Quality Checks

### Prérequis avant d'exécuter

| Prérequis | Comment vérifier |
|---|---|
| nb_03 exécuté avec succès | Tables `gold_book_catalog`, `gold_category_stats` existent |
| `silver_books` existe | Toujours présente si nb_02 a tourné |

```python
# Vérifier les prérequis avant de lancer nb_04
tables_requises = ["silver_books", "gold_book_catalog", "gold_category_stats"]
for t in tables_requises:
    assert spark.catalog.tableExists(t), f"🔴 Table {t} introuvable — vérifier les notebooks précédents"
print("✅ Prérequis nb_04 validés")
```

### Points d'attention dans le code

**1. `FAIL_ON_CRITICAL = False` par défaut**

```python
FAIL_ON_CRITICAL = False
```

En mode TP : le notebook **ne lève pas d'erreur** même si des checks critiques échouent. Il affiche juste les résultats. En production, passer à `True` pour bloquer le pipeline.

**2. `dq_results` est en mode `append`**

```python
dq_df.write.format("delta").mode("append").saveAsTable("dq_results")
```

Chaque exécution de nb_04 **ajoute** des lignes à `dq_results`. Si tu relances 3 fois, tu auras 3 × 8 = 24 lignes dans la table. Pour analyser, filtrer sur `run_ts_utc` pour ne voir que le dernier run.

**3. Le check `gold_has_same_count_as_silver` est le plus important**

```python
add_check("gold_has_same_count_as_silver", "critical",
          gold_count == silver_count, ...)
```

Ce check vérifie qu'aucune donnée n'a été perdue entre silver et gold. Si ce check échoue → relancer nb_03.

### ✅ Interprétation des résultats

Après exécution, le `display()` montre le tableau des checks. Voici ce que tu dois voir :

| check_name | severity | passed | metric_value |
|---|---|---|---|
| silver_has_rows | critical | True | 100 |
| gold_has_same_count_as_silver | critical | True | 100/100 |
| gold_has_categories | major | True | 15 |
| price_positive | critical | True | 0 |
| rating_between_1_and_5 | critical | True | 0 |
| title_not_empty | critical | True | 0 |
| category_not_empty | major | True | 0 |
| source_url_unique | major | True | 0 |

> Pour les checks `price_positive`, `rating_between_1_and_5`, `title_not_empty`, etc. : `metric_value = 0` signifie **zéro anomalie trouvée** → c'est bon. `passed = True`.

### 🔴 Erreurs fréquentes et solutions

| Check échoué | Cause probable | Action |
|---|---|---|
| `silver_has_rows` échoue | nb_02 a produit une table vide | Inspecter `silver_books_rejected`, relancer nb_02 |
| `gold_has_same_count_as_silver` échoue | Perte de données dans nb_03 | Comparer les counts, inspecter le `select()` de `gold_book_catalog` dans nb_03, relancer nb_03 |
| `price_positive` échoue | Prix NULL ou négatif dans silver | Inspecter `silver_books.filter(col("price_gbp").isNull())` |
| `rating_between_1_and_5` échoue | `rating_value` hors [1,5] dans silver | Inspecter `silver_books.select("rating_text","rating_value").distinct()` |
| `source_url_unique` échoue | Doublons dans silver (déduplication ratée) | Vérifier le `dropDuplicates(["source_url"])` dans nb_02 |

### 🔍 Méthode de debug nb_04

**Voir uniquement le dernier run dans `dq_results` :**

```python
last_run = spark.table("dq_results").agg({"run_ts_utc": "max"}).collect()[0][0]
display(
    spark.table("dq_results")
    .filter(F.col("run_ts_utc") == last_run)
    .orderBy("severity", "passed")
)
```

**Voir l'historique de tous les runs :**

```python
display(
    spark.table("dq_results")
    .groupBy("run_ts_utc")
    .agg(
        F.sum(F.when(F.col("passed") == True, 1).otherwise(0)).alias("checks_passed"),
        F.sum(F.when(F.col("passed") == False, 1).otherwise(0)).alias("checks_failed"),
    )
    .orderBy(F.desc("run_ts_utc"))
)
```

---

## Récapitulatif — Tableau de décision avant chaque notebook

```
Avant nb_01 :
  ├── ✅ Lakehouse attaché ?
  ├── ✅ %pip install beautifulsoup4 requests exécuté ?
  └── ✅ Site https://books.toscrape.com/ accessible ?

Avant nb_02 :
  ├── ✅ nb_01 terminé sans erreur ?
  ├── ✅ Fichier JSONL présent dans Files/bronze/... ?
  └── ✅ Au moins 1 partition ingestion_date=* visible ?

Avant nb_03 :
  ├── ✅ nb_02 terminé sans erreur ?
  ├── ✅ silver_books.count() > 0 ?
  └── ✅ silver_categories.count() > 0 ?

Avant nb_04 :
  ├── ✅ nb_03 terminé sans erreur ?
  ├── ✅ gold_book_catalog.count() > 0 ?
  └── ✅ gold_book_catalog.count() == silver_books.count() ?
```

---

## Méthode générale de debugging dans Fabric

### Règle 1 — Isoler avant de corriger

Ne jamais modifier plusieurs choses à la fois. Si un notebook échoue :
1. Lire le message d'erreur jusqu'au bout (la cause réelle est souvent en bas)
2. Tester le problème dans une **cellule séparée** avec un exemple minimal
3. Corriger une seule chose à la fois
4. Relancer uniquement la cellule corrigée

### Règle 2 — Lire l'erreur de bas en haut

Dans les erreurs Spark/PySpark, le message utile est presque toujours **à la fin** du traceback, pas au début.

```
[long traceback Spark...]
[long traceback Spark...]
AnalysisException: Table or view not found: silver_books   ← LIRE ICI
```

### Règle 3 — Vérifier les counts à chaque étape

Ajouter systématiquement un `print(df.count())` ou un `display(df.limit(5))` après chaque transformation importante. Un count à 0 révèle immédiatement où la donnée a disparu.

### Règle 4 — Commande de diagnostic rapide

```python
# Snapshot de l'état du lakehouse — à exécuter en cas de doute
tables = spark.catalog.listTables()
for t in tables:
    count = spark.table(t.name).count()
    print(f"{t.name:40s} → {count:6d} lignes")
```

### Règle 5 — Relancer le kernel en cas de comportement étrange

Si une variable semble avoir une valeur inattendue, ou si `%pip install` a été exécuté en milieu de session :

**Kernel** → **Restart** → relancer les cellules depuis le début

Le kernel Spark de Fabric garde les variables en mémoire entre les cellules d'une même session. Un restart repart à zéro proprement.

### Règle 6 — Inspecter le schéma avant de transformer

```python
# Avant toute transformation, vérifier les types réels des colonnes
raw_df.printSchema()
# ou
spark.table("silver_books").printSchema()
```

Un cast qui échoue silencieusement (retourne NULL au lieu d'une erreur) est souvent dû à un type inattendu dans les données sources.
