# DP-700 — Microsoft Fabric Data Engineer Associate

Dépôt d'étude complet pour la certification **Microsoft Certified: Fabric Data Engineer Associate** (examen DP-700) et les certifications associées de l'écosystème Microsoft Fabric.

---

## Certifications couvertes

| Code | Titre |
|------|-------|
| **DP-700** | Implémenter des solutions d'ingénierie des données avec Microsoft Fabric |
| DP-600 | Implémenter des solutions d'analytique avec Microsoft Fabric |
| DP-601 | Implémenter un Lakehouse avec Microsoft Fabric |
| DP-602 | Implémenter un entrepôt de données avec Microsoft Fabric |
| DP-603 | Implémenter Real-Time Intelligence avec Microsoft Fabric |
| DP-604 | Implémenter une solution Data Science & ML pour l'IA avec Microsoft Fabric |
| DP-3029 | Travailler plus intelligemment avec Copilot dans Microsoft Fabric |

---

## Structure du dépôt

```
├── _data/                          ← Métadonnées (catégories, mapping cours/labs)
│   └── lab-metadata.yml
├── resources/                      ← Ressources d'étude
│   └── 1. Guide d'étude de l'examen DP-700.md
├── Instructions/Labs/              ← Labs pratiques (47 fichiers)
│   ├── 01-lakehouse.md             ...
│   ├── ...
│   └── Images/                     ← 344 captures d'écran des labs
└── mslearn-training/               ← Modules Microsoft Learn (français)
    ├── 0. Commencez avec Fabric
    ├── I. Ingérer des données
    ├── II. Implémenter un Lakehouse
    ├── III. Implémenter Real-Time Intelligence
    ├── IV. Implémenter un entrepôt de données
    ├── V. Gérer un environnement Fabric
    └── VI. Utiliser Activator
```

---

## Domaines de l'examen DP-700

| Domaine | Poids | Labs associés |
|---------|-------|---------------|
| Implémenter & gérer une solution d'analytique | 30–35% | 18, 19, 19b, 21, 21b, 23–25 |
| Ingérer & transformer des données | 30–35% | 01–05, 09, 12, 26b–26d |
| Surveiller & optimiser une solution d'analytique | 30–35% | 06c, 15, 16, 17, 18 |

---

## Parcours d'apprentissage

| Section | Durée | Niveau | Description |
|---------|-------|--------|-------------|
| 0. Commencez avec Microsoft Fabric | 6h12 | Débutant | Fondamentaux : lakehouse, entrepôt, RTI, data science, SQL DB, modèles sémantiques, Fabric IQ |
| I. Ingérer des données | 3h48 | Intermédiaire | Dataflows Gen2, pipelines, Spark, Eventhouse/KQL |
| II. Implémenter un Lakehouse | 5h01 | Intermédiaire | Lakehouse, Delta Lake, architecture médaillon, orchestration |
| III. Real-Time Intelligence | 5h31 | Débutant | Eventstream, Eventhouse, dashboards temps réel, Activator |
| IV. Implémenter un entrepôt de données | 6h24 | Débutant | Chargement, requêtes, Copilot, surveillance, sécurité |
| V. Gérer un environnement Fabric | 3h34 | Intermédiaire | CI/CD, monitoring, sécurité multi-couche, administration |
| VI. Utiliser Activator | 1h01 | Débutant | Objets, règles, actions (email/Teams) |
| **Total** | **~31h** | | 47 labs + ~45 modules théoriques |

---

## Thèmes clés couverts

- **OneLake / Lakehouse** — architecture unifiée fichiers + tables Delta-Parquet
- **Delta Lake** — ACID, time travel, streaming, optimization (V-order)
- **Medallion Architecture** — Bronze → Silver → Gold
- **Real-Time Intelligence** — Eventstream → Eventhouse (KQL) → Dashboards → Activator
- **Data Factory** — Pipelines (Copy Data), Dataflows Gen2 (Power Query Online)
- **Apache Spark** — Notebooks PySpark, Spark SQL, Data Wrangler, MLflow
- **Data Warehouse** — T-SQL complet, requêtes visuelles, SSMS, vues, procédures stockées
- **Semantic Models** — Direct Lake, star schema, calculation groups, DAX, TMDL
- **Fabric IQ** — Ontologies, Knowledge Graphs, Data Agents, Copilot
- **Sécurité multi-couche** — Workspace roles → Item permissions → RLS/DDM/Column-level → T-SQL granular
- **CI/CD** — Git integration, deployment pipelines, Fabric APIs
- **Surveillance** — Monitor Hub, DMVs, capacity metrics, Activator alerts
- **Copilot** — Dataflows Gen2, Notebooks, Data Warehouse, Data Agents

---

## Comment utiliser ce dépôt

1. **Étude théorique** — Parcourez `mslearn-training/` pour les modules Microsoft Learn en français (XP, durées, objectifs)
2. **Pratique** — Suivez les labs dans `Instructions/Labs/` (anglais, avec captures d'écran)
3. **Révision** — Consultez `resources/` pour le guide d'étude DP-700
4. **Préparation à l'examen** — Concentrez-vous sur les 3 domaines de l'examen via le mapping `_data/lab-metadata.yml`

> **Remarque** : Les labs référencent des dépôts GitHub externes (`MicrosoftLearning/dp-data`, `mslearn-fabric`). Une capacité Fabric (essai gratuit ou capacité payante) est requise.

---

## Prérequis

- Expérience en ingénierie des données
- Connaissance de SQL, PySpark et/ou KQL
- Compréhension des concepts cloud et Data Lake/Data Warehouse
- Compte Microsoft Fabric (essai gratuit disponible sur `https://app.fabric.microsoft.com/`)
