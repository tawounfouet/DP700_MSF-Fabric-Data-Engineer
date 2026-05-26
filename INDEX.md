# INDEX — DP-700 Microsoft Fabric Data Engineer Associate

Index exhaustif de tous les fichiers du dépôt d'étude.

---

## `_data/` — Métadonnées

### `lab-metadata.yml`
Fichier de configuration YAML définissant 11 catégories de labs et 7 parcours de certification (DP-700 à DP-3029). Chaque cours liste l'ordre séquentiel de ses labs. Utilisé pour le rendu de la page d'accueil `index.md`.

---

## `resources/` — Ressources d'étude

### `1. Guide d'étude de l'examen DP-700.md`
Guide d'étude officiel en français pour l'examen DP-700. Détaille le profil du candidat "Fabric Data Engineer Associate", les 3 domaines de compétences (30–35% chacun), les sous-thèmes évalués. Dernière mise à jour : 20 avril 2026.

---

## `Instructions/Labs/` — Labs pratiques

47 fichiers de labs en anglais avec frontmatter YAML (durée, niveau, catégories, cours). Chaque lab est un tutoriel pas-à-pas avec captures d'écran.

### Labs fondamentaux — Lakehouse & ingestion

| Fichier | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| `01-lakehouse.md` | 30 min | 200 | Créer un lakehouse Fabric, uploader des fichiers CSV, charger en table Delta, interroger via SQL et visual query |
| `02-analyze-spark.md` | 45 min | 200 | Analyser des données avec Apache Spark dans un notebook Fabric (DataFrame PySpark, Spark SQL, visualisation) |
| `03-delta-lake.md` | 40 min | 200 | Utiliser des tables Delta Lake (ACID, time travel, streaming, V-order optimization) |
| `03b-medallion-lakehouse.md` | 45 min | 300 | Implémenter l'architecture en médaillon (Bronze → Silver → Gold) dans un lakehouse Fabric |
| `04-ingest-pipeline.md` | 60 min | 200 | Créer un pipeline avec activité Copy Data pour ingérer des données depuis Azure SQL Database |
| `05-dataflows-gen2.md` | 30 min | 200 | Créer et utiliser un Dataflow Gen2 (Power Query Online) pour ingérer et transformer des données |

### Labs — Data Warehouse

| Fichier | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| `06-data-warehouse.md` | 30 min | 200 | Créer et interroger un entrepôt de données Fabric avec T-SQL |
| `06a-data-warehouse-load.md` | 30 min | 200 | Charger des données dans un entrepôt via pipelines, T-SQL (COPY, INSERT), Dataflows Gen2 |
| `06b-data-warehouse-query.md` | 30 min | 200 | Interroger un entrepôt avec l'éditeur SQL, l'éditeur visuel et SSMS |
| `06c-monitor-data-warehouse.md` | 30 min | 200 | Surveiller un entrepôt avec les DMVs (connexions, sessions, requêtes) et les métriques de capacité |
| `06d-secure-data-warehouse.md` | 30 min | 200 | Sécuriser un entrepôt : Dynamic Data Masking, Row-Level Security, Column-Level Security, permissions T-SQL |

### Labs — Real-Time Intelligence

| Fichier | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| `07-real-time-Intelligence.md` | 30 min | 200 | Prise en main de Real-Time Intelligence : Eventstream, Eventhouse, KQL, dashboard |
| `09-real-time-analytics-eventstream.md` | 30 min | 200 | Ingérer des données en temps réel avec Eventstream (sources, destinations, transformations) |
| `11-data-activator.md` | 30 min | 200 | Utiliser Activator pour détecter des patterns et déclencher des actions (email, Teams) |
| `12-query-data-in-kql-database.md` | 35 min | 200 | Interroger des données dans une base de données KQL avec KQL |
| `13-real-time-dashboards.md` | 35 min | 200 | Créer des tableaux de bord en temps réel avec des visualisations KQL |

### Labs — Data Science

| Fichier | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| `08-data-science-get-started.md` | 20 min | 200 | Explorer la science des données dans Fabric : notebooks, MLflow |
| `08a-data-science-explore-data.md` | 30 min | 200 | Explorer et visualiser des données avec des notebooks |
| `08b-data-science-preprocess-data-wrangler.md` | 30 min | 200 | Prétraiter des données avec Data Wrangler dans Fabric |
| `08c-data-science-train.md` | 30 min | 200 | Entraîner et évaluer des modèles ML avec Fabric |
| `08d-data-science-batch.md` | 30 min | 300 | Effectuer des prédictions par lots avec un modèle entraîné |

### Labs — Semantic Models & Power BI

| Fichier | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| `14-create-dax-calculations.md` | 45 min | 200 | Créer des calculs DAX (mesures, colonnes calculées, tables calculées) |
| `15-design-semantic-model-scale.md` | 30 min | 200 | Concevoir des modèles sémantiques pour la mise à l'échelle (Direct Lake, star schema, calculation groups) |
| `15-design-scalable-semantic-models.md` | 30 min | 200 | Variante du précédent (contenu similaire) |
| `16-create-reusable-power-bi-assets.md` | 30 min | 200 | Créer des assets Power BI réutilisables (modèles, themes, field parameters) |
| `16-optimize-semantic-model-performance.md` | 30 min | 300 | Optimiser les performances des modèles sémantiques (Performance Analyzer, DAX Studio, mesures optimisées) |
| `17-enforce-model-security.md` | 30 min | 200 | Appliquer la sécurité au niveau des lignes (RLS) et des objets dans les modèles sémantiques |

### Labs — Sécurité, Gouvernance & Cycle de vie

| Fichier | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| `18-monitor-hub.md` | 30 min | 200 | Surveiller les activités Fabric avec le Monitor Hub |
| `19-secure-data-access.md` | 45 min | 200 | Sécuriser l'accès aux données : rôles workspace, permissions item, OneLake data roles |
| `19b-govern-analytics-data.md` | 30 min | 200 | Gouvernance des données : endorsement, lineage, impact analysis, OneLake catalog |
| `20-work-with-database.md` | 30 min | 200 | Travailler avec SQL Database dans Fabric (base de données transactionnelle) |
| `20a-work-with-graphql.md` | 30 min | 300 | Interroger des données Fabric via l'API GraphQL |
| `21-implement-cicd.md` | 20 min | 200 | Implémenter CI/CD : intégration Git, pipelines de déploiement, API Fabric |
| `21b-manage-semantic-model-lifecycle.md` | 30 min | 300 | Gérer le cycle de vie des modèles sémantiques (Git, pipelines, TMDL, SemPy) |

### Labs — Copilot & AI

| Fichier | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| `22a-copilot-fabric-dataflow-gen2.md` | 30 min | 200 | Utiliser Copilot dans Dataflows Gen2 pour décrire des transformations |
| `22b-copilot-fabric-notebooks.md` | 30 min | 200 | Utiliser Copilot dans les notebooks pour générer du code PySpark |
| `22c-copilot-fabric-data-warehouse.md` | 30 min | 200 | Utiliser Copilot dans Data Warehouse (complétions SQL, chat, quick actions) |
| `22d-copilot-fabric-data-agents.md` | 30 min | 300 | Créer un Data Agent avec Copilot pour interroger des données en langage naturel |

### Labs — Fabric IQ & Ontologies

| Fichier | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| `23-build-ontology-manually.md` | 30 min | 300 | Construire manuellement une ontologie Fabric IQ (entités, relations, timeseries) |
| `24-build-ontology-semantic-model.md` | 30 min | 300 | Générer une ontologie à partir d'un modèle sémantique Power BI existant |
| `25-discover-onelake.md` | 45 min | 200 | Découvrir OneLake : shortcuts, catalog, gouvernance |
| `26-design-dimensional-models.md` | 30 min | 200 | Concevoir des modèles dimensionnels (schéma en étoile, tables de faits et dimensions) |
| `26b-transform-data-dataflows.md` | 30 min | 200 | Transformer des données avec Dataflows Gen2 |
| `26c-transform-data-notebooks.md` | 30 min | 200 | Transformer des données avec des notebooks Spark |
| `26d-transform-data-tsql.md` | 30 min | 200 | Transformer des données avec T-SQL (vues, procédures stockées, CTE) |
| `27-visualize-ontology.md` | 30 min | 300 | Visualiser une ontologie Fabric IQ (graph view, card view, composants) |
| `28-build-data-agent-ontology.md` | 30 min | 300 | Construire un Data Agent basé sur une ontologie pour le questionnement en NL |
| `30-prepare-model-ai.md` | 30 min | 200 | Préparer un modèle sémantique pour l'IA (enrichissement, tagging, metadata) |

### `Images/` — Captures d'écran
344 fichiers PNG utilisés par les labs pour illustrer chaque étape.

---

## `mslearn-training/` — Modules Microsoft Learn

Contenu théorique en français extrait de Microsoft Learn, organisé par parcours d'apprentissage. Chaque section contient un `Readme.md` listant les modules, durées, XP, et objectifs.

### `0. Commencez avec Microsoft Fabric` (6h12 — Débutant)
8 modules — 6900 XP total. Fondamentaux de la plateforme Fabric.
- `Readme.md` — Présentation du parcours
- `1. Présentation de l'analytique...Fabric.md` — *(fichier vide)*
- `2. Commencez avec les lakehouses...md` — Lakehouses, OneLake, SQL endpoint
- `3. Commencez avec les entrepôts de données...md` — Data warehouse, T-SQL, modélisation
- `4. Commencez avec l'Intelligence en temps réel...md` — RTI, Eventstream, Eventhouse, KQL
- `5. Commencez avec la science des données...md` — Data science, notebooks, MLflow
- `6. Prise en main de SQL Database...md` — SQL Database, mirroring, Copilot
- `7. Concevoir des modèles sémantiques...md` — Direct Lake, star schema, calculation groups
- `8. Comprendre les principes fondamentaux de Fabric IQ.md` — Ontologies, data agents, Graph
- `labs/` — Labs redondants (01-lakehouse, 02-analyze-spark, 03-delta-lake)

### `I. Ingérer des données avec Microsoft Fabric` (3h48 — Intermédiaire)
4 modules — 3500 XP total.
- `Readme.md` — Présentation du parcours
- `01. Ingérer des données avec des flux de données Gen2...md` — Dataflows Gen2, Power Query Online
- `02. Orchestrer des processus...md` — Pipelines, Copy Data, programmation
- `03. Utiliser Apache Spark...md` — PySpark DataFrames, Spark SQL, visualisation
- `04. Utiliser des données en temps réel...Eventhouse...md` — Eventhouse, bases KQL
- Labs redondants : `02-analyze-spark.md`, `04-ingest-pipeline.md`, `05-dataflows-gen2.md`, `12-query-data-in-kql-database.md`

### `II. Implémenter un Lakehouse avec Microsoft Fabric` (5h01 — Intermédiaire)
7 modules — 5900 XP total.
- `Readme.md` — Architecture du lakehouse, Delta Lake, médaillon
- `01. Présentation de l'analytique...Fabric.md` — Vue d'ensemble Fabric (cross-listed)
- `02. Commencez avec les lakehouses...md` — Création lakehouse, ingestion, requêtes
- `03. Utiliser Apache Spark...md` — Notebooks, Spark SQL, visualisation
- `04. Utiliser des tables Delta Lake...md` — Delta format, ACID, time travel, streaming
- `05. Ingérer des données avec Dataflows Gen2...md` — Power Query pour lakehouse
- `06. Orchestrer les processus...md` — Pipelines Data Factory
- `07. Organiser...architecture en médaillon.md` — Bronze/Silver/Gold
- `media/` — `onelake-architecture.png`, `onelake-catalog.png`

### `III. Implémenter Real-Time Intelligence avec Microsoft Fabric` (5h31 — Débutant)
5 modules — 4300 XP total.
- `Readme.md` — RTI pipeline complet
- `01. Bien démarrer avec Real-Time Intelligence...md` — Concepts temps réel Fabric
- `02. Utiliser Eventstream...md` — Sources, destinations, transformations
- `03. Utiliser des données en temps réel...Eventhouse...md` — KQL, vues matérialisées
- `04. Créer des tableaux de bord en temps réel...md` — Visualisations KQL, paramètres
- `05. Utilisez Activator...md` — Règles, actions, notifications

### `IV. Implémenter un data warehouse avec Microsoft Fabric` (6h24 — Débutant)
7 modules — 5900 XP total.
- `Readme.md` — Data warehouse Fabric complet
- `01. Présentation de l'analytique...Fabric.md` — Vue d'ensemble (cross-listed)
- `02. Commencez avec les entrepôts de données...md` — Fabric DW vs lakehouse SQL endpoint
- `03. Charger des données dans un entrepôt...md` — Pipelines, T-SQL, Dataflows
- `04. Interroger un entrepôt de données...md` — SQL editor, visual query, SSMS
- `05. Prise en main de Copilot...Data Warehouse.md` — IA pour T-SQL
- `06. Surveiller un entrepôt de données...md` — DMVs, métriques capacité
- `07. Sécuriser un entrepôt de données...md` — DDM, RLS, column-level, T-SQL permissions
- `labs/` — 6 labs redondants (06-data-warehouse, 06a, 06b, 06c, 06d, 22c-copilot)

### `V. Gérer un environnement Microsoft Fabric` (3h34 — Intermédiaire)
4 modules — 3300 XP total.
- `Readme.md` — CI/CD, monitoring, sécurité, administration
- `01. Implémenter...CI/CD...md` — Git integration, deployment pipelines, API Fabric
- `02. Surveiller les activités...md` — Monitor Hub, Activator
- `03. Sécuriser l'accès aux données...md` — *(fichier vide)*
- `04. Sécuriser l'accès aux données...md` — Modèle sécurité multi-couche
- `05. Administrer un environnement...md` — Admin portal, tenant settings, gouvernance

### `VI. Utilisez Activator dans Microsoft Fabric` (1h01 — Débutant)
1 module.
- `Readme.md` — Objets, règles, actions email/Teams
- `11-data-activator.md` — Lab redondant
- `lab.txt` — Notes

---

## Statistiques

| Métrique | Valeur |
|----------|--------|
| Labs uniques | 47 |
| Modules théoriques | ~45 |
| Captures d'écran | 344 |
| Certifications couvertes | 7 (DP-700, DP-600, DP-601, DP-602, DP-603, DP-604, DP-3029) |
| Temps d'étude estimé | ~31 heures |
| Niveaux | Débutant à 300 (avancé) |
| Langues | Modules : français / Labs : anglais |

---

## Notes

- Les fichiers marqués "redondants" dans `mslearn-training/` sont des duplications des labs de `Instructions/Labs/` et peuvent être ignorés
- Le lab numéro 10 est absent (saut volontaire dans la numérotation entre 09 et 11)
- Le fichier `mslearn-training/0.../1...md` et `mslearn-training/V.../03...md` sont vides
- Certains labs existent en deux exemplaires avec des noms légèrement différents (e.g., `15-design-semantic-model-scale.md` et `15-design-scalable-semantic-models.md`)
- Les labs référencent des données externes via `MicrosoftLearning/dp-data` et `mslearn-fabric` sur GitHub
