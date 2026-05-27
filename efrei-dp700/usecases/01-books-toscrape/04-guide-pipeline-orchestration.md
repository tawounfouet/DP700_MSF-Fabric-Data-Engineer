# 04 - Guide Pipeline d'orchestration — pas à pas pour les nuls

> **Objectif** : créer un Data Pipeline Fabric qui exécute les 4 notebooks dans le bon ordre en un seul clic, avec monitoring et possibilité de planification automatique.

---

## Prérequis

Avant de commencer ce guide, les étapes suivantes doivent être terminées :

- [x] Workspace `ws-efrei-dp700-books-dev-groupeXX` créé et associé à une capacité Fabric
- [x] Lakehouse `lh_books_toscrape` créé
- [x] Les 4 notebooks créés et **chacun attaché** au lakehouse `lh_books_toscrape`
- [x] Les notebooks ont été exécutés au moins une fois manuellement (pour vérifier qu'ils fonctionnent)

---

## C'est quoi un Data Pipeline dans Fabric ?

Un **Data Pipeline** est un chef d'orchestre visuel.

Sans pipeline, tu dois :
1. Ouvrir `nb_01`, cliquer Run, attendre
2. Ouvrir `nb_02`, cliquer Run, attendre
3. Ouvrir `nb_03`, cliquer Run, attendre
4. Ouvrir `nb_04`, cliquer Run, attendre

Avec le pipeline :
1. Cliquer **Run** sur le pipeline → tout s'enchaîne automatiquement

Le pipeline **ne contient pas le code** des notebooks — il les appelle dans l'ordre, comme un script qui lance d'autres scripts.

```
[Pipeline]
    │
    ├──► appelle nb_01  (attend que ce soit fini)
    │         ↓
    ├──► appelle nb_02  (attend que ce soit fini)
    │         ↓
    ├──► appelle nb_03  (attend que ce soit fini)
    │         ↓
    └──► appelle nb_04  (attend que ce soit fini)
```

---

## Étape 1 — Créer le pipeline

1. Dans le workspace `ws-efrei-dp700-books-dev-groupeXX`, cliquer sur **`+ New item`**
2. Dans la liste qui s'ouvre, chercher et cliquer sur **`Data Pipeline`**
3. Une fenêtre demande le nom du pipeline. Saisir :

```text
pl_books_toscrape_end_to_end
```

4. Cliquer **Create**

> Le canvas du pipeline s'ouvre. C'est une zone blanche avec une barre d'outils en haut. C'est normal, il est vide pour l'instant.

---

## Étape 2 — Ajouter la première activité Notebook

Une **activité** = une tâche que le pipeline doit exécuter. Ici on utilise des activités de type **Notebook**.

### Ajouter nb_01

1. Dans la barre d'outils du canvas, cliquer sur **`Add activity`**
2. Dans la liste des types d'activités, cliquer sur **`Notebook`**
3. Une boîte apparaît sur le canvas. Elle s'appelle par défaut `Notebook1` — on va la renommer.

### Configurer l'activité nb_01

Cliquer sur la boîte `Notebook1` pour la sélectionner. Un panneau de configuration s'ouvre en bas (ou à droite selon la version).

**Onglet `General`** :
- Champ `Name` → remplacer `Notebook1` par :
```text
nb_01_ingest_books_bronze
```

**Onglet `Settings`** :
- Champ `Notebook` → cliquer sur la liste déroulante → sélectionner `nb_01_ingest_books_bronze`

> **C'est ce lien entre l'activité et le notebook qui est crucial.** L'activité est juste une "case" dans le pipeline — elle doit pointer vers le vrai notebook.

---

## Étape 3 — Ajouter les 3 autres activités Notebook

Répéter exactement la même procédure pour les 3 notebooks suivants :

| Activité à créer | Notebook à sélectionner |
|---|---|
| `nb_02_transform_books_silver` | `nb_02_transform_books_silver` |
| `nb_03_build_books_gold` | `nb_03_build_books_gold` |
| `nb_04_data_quality_checks` | `nb_04_data_quality_checks` |

À ce stade, tu as **4 boîtes sur le canvas**, mais elles sont indépendantes — elles ne sont pas encore reliées. Si tu lançais le pipeline maintenant, les 4 notebooks se lanceraient **en parallèle et en même temps**, ce qui casserait tout (nb_02 lirait des tables que nb_01 n'a pas encore écrites).

---

## Étape 4 — Relier les activités dans l'ordre

C'est l'étape la plus importante : définir l'**ordre d'exécution**.

### Comment relier deux activités

1. Survoler la boîte `nb_01_ingest_books_bronze` avec la souris
2. Une **petite flèche** (ou un point vert) apparaît sur le bord droit de la boîte
3. Cliquer sur cette flèche et **faire glisser** jusqu'à la boîte `nb_02_transform_books_silver`
4. Relâcher → une ligne apparaît entre les deux boîtes

### Choisir le type de connexion

Quand tu relie deux activités, Fabric te demande quel type de déclenchement :

| Type | Signification | Quand l'utiliser |
|---|---|---|
| **On success** ✅ | Le suivant démarre seulement si le précédent a réussi | En production |
| **On failure** ❌ | Le suivant démarre seulement si le précédent a échoué | Pour envoyer une alerte |
| **On completion** 🔄 | Le suivant démarre dans tous les cas | En cours d'apprentissage |
| **On skip** ⏭️ | Le suivant démarre si le précédent a été ignoré | Cas avancés |

> **Pour ce guide pédagogique : choisir `On completion`**
>
> Pourquoi ? Parce que si le notebook de data quality (nb_04) remonte des warnings, on veut quand même voir tout le pipeline s'enchaîner jusqu'au bout. En production réelle, on utiliserait `On success` pour stopper le pipeline dès qu'une étape échoue.

### Relier les 4 activités en séquence

Répéter l'opération 3 fois :

```
nb_01_ingest_books_bronze
        │
        └──[On completion]──► nb_02_transform_books_silver
                                        │
                                        └──[On completion]──► nb_03_build_books_gold
                                                                        │
                                                                        └──[On completion]──► nb_04_data_quality_checks
```

Le canvas doit maintenant montrer **4 boîtes reliées par 3 flèches** de gauche à droite.

---

## Étape 5 — Sauvegarder

Cliquer sur **`Save`** (icône disquette ou `Ctrl+S`).

> Ne pas oublier cette étape — Fabric ne sauvegarde pas automatiquement.

---

## Étape 6 — Tester le pipeline manuellement

### Lancer le pipeline

1. Cliquer sur **`Run`** (bouton lecture ▶️ dans la barre d'outils)
2. Une confirmation peut apparaître → cliquer **OK / Save and run**

### Suivre l'exécution en temps réel

Le canvas passe en mode monitoring. Chaque activité change de couleur selon son état :

| Couleur | Signification |
|---|---|
| 🔵 Bleu / en cours | L'activité est en train de s'exécuter |
| 🟢 Vert | L'activité a réussi |
| 🔴 Rouge | L'activité a échoué |
| ⚪ Gris | L'activité n'a pas encore démarré |

L'exécution complète prend plusieurs minutes (Spark doit démarrer pour chaque notebook).

### Vérifier les détails d'une activité

Cliquer sur une activité terminée → un panneau affiche :
- Heure de début et de fin
- Durée d'exécution
- Statut détaillé
- Lien vers les logs du notebook

---

## Étape 7 — Vérifier que les données sont bien là

Après l'exécution complète du pipeline :

1. Retourner dans le workspace
2. Cliquer sur `lh_books_toscrape`
3. Dans l'explorateur gauche, ouvrir **`Tables`**
4. Cliquer sur **`Refresh`** si les tables n'apparaissent pas

Tu dois voir ces tables :

```
Tables/
├── bronze_books_raw        ← écrite par nb_01
├── silver_books            ← écrite par nb_02
├── silver_categories       ← écrite par nb_02
├── silver_books_rejected   ← écrite par nb_02
├── gold_book_catalog       ← écrite par nb_03
├── gold_category_stats     ← écrite par nb_03
├── dim_category_gold       ← écrite par nb_03
├── dim_rating_gold         ← écrite par nb_03
├── fact_books_gold         ← écrite par nb_03
└── dq_results              ← écrite par nb_04
```

---

## Étape 8 — Consulter l'historique des exécutions

Le pipeline garde une trace de toutes les exécutions passées.

1. Dans le canvas du pipeline, cliquer sur l'onglet **`Run history`** (ou **`View run history`**)
2. Chaque ligne = une exécution du pipeline
3. Colonnes visibles : date, heure, durée totale, statut global

> C'est utile pour diagnostiquer des problèmes : "le pipeline a échoué hier à 3h du matin, pourquoi ?"

---

## Étape 9 (optionnel) — Planifier une exécution automatique

Pour que le pipeline tourne automatiquement sans intervention manuelle :

1. Dans le canvas, cliquer sur **`Schedule`** (icône horloge 🕐)
2. Activer le toggle **`Scheduled run`**
3. Configurer la fréquence :
   - **Repeat** : `Daily`, `Weekly`, `Hourly`...
   - **Time** : heure d'exécution (ex. 06:00)
   - **Time zone** : Europe/Paris
4. Cliquer **Apply**

> **Attention** : un pipeline planifié consomme des unités de capacité Fabric (CU). En environnement d'apprentissage, ne planifier que si nécessaire et désactiver après les tests.

---

## Résumé visuel de ce qui a été créé

```
WORKSPACE : ws-efrei-dp700-books-dev-groupeXX
│
├── LAKEHOUSE : lh_books_toscrape
│   ├── Files/
│   │   └── bronze/books_toscrape/  (HTML brut + JSON Lines)
│   └── Tables/
│       ├── bronze_*
│       ├── silver_*
│       ├── gold_*
│       ├── dim_* / fact_*
│       └── dq_results
│
├── NOTEBOOKS (tous attachés à lh_books_toscrape)
│   ├── nb_01_ingest_books_bronze
│   ├── nb_02_transform_books_silver
│   ├── nb_03_build_books_gold
│   └── nb_04_data_quality_checks
│
└── PIPELINE : pl_books_toscrape_end_to_end
    └── nb_01 ──► nb_02 ──► nb_03 ──► nb_04
        (On completion entre chaque étape)
```

---

## Erreurs fréquentes et solutions

| Erreur | Cause probable | Solution |
|---|---|---|
| `Table not found: silver_books` | nb_03 s'est lancé avant nb_02 | Vérifier que les flèches sont bien `On completion` et dans le bon sens |
| `Path does not exist: /lakehouse/default/Files` | Notebook non attaché au lakehouse | Ouvrir le notebook, attacher `lh_books_toscrape` comme lakehouse par défaut |
| Notebook ne démarre pas (spinning indefiniment) | Session Spark qui démarre à froid | Normal, attendre 2-3 minutes |
| Pipeline rouge mais notebooks verts | Problème de configuration de l'activité | Vérifier que chaque activité pointe bien vers le bon notebook dans l'onglet Settings |
| `ModuleNotFoundError: beautifulsoup4` | Librairie non installée | Ajouter une activité Notebook en tout premier qui exécute `%pip install beautifulsoup4 requests` |
