# Utilisez Activator dans Microsoft Fabric

*1 h 1 min* | *1 module* | *7 Unités* | **800 XP**

| Propriété | Valeur |
|-----------|--------|
| **Niveau** | Débutant |
| **Rôles** | Ingénieur Data · Analyste de données |
| **Produit** | Microsoft Fabric |
| **Domaine** | Real-Time Intelligence |
| **Parcours associés** | Implémenter Real-Time Intelligence avec Microsoft Fabric |

---

## Aperçu

Fabric Activator est le moteur d'intelligence automatisée de Microsoft Fabric. Il surveille en continu vos flux de données en temps réel et déclenche automatiquement des actions (emails, Teams, Power Automate, webhooks) lorsque des conditions ou patterns spécifiques sont détectés.

Activator complète le pipeline **Real-Time Intelligence** de Fabric :

```
Sources → Eventstream → Eventhouse (KQL) → Real-Time Dashboards
                                         ↓
                                    ACTIVATOR
                                         ↓
                    Email / Teams / Power Automate / Azure Functions
```

---

## Modules de ce parcours

### 800 XP — Utilisez Activator dans Microsoft Fabric *(1 h 1 min)*

**7 Unités :**

| # | Unité | Durée |
|---|-------|-------|
| 1 | Présentation | 4 min |
| 2 | Configurer Activator pour vos données | 7 min |
| 3 | Créer des règles dans Activator | 6 min |
| 4 | Configurer des actions dans Activator | 3 min |
| 5 | Exercice — Utiliser Activator dans Fabric | 30 min |
| 6 | Évaluation du module | 10 min |
| 7 | Résumé | 1 min |

---

## Objectifs du parcours

À l'issue de ce module, vous serez capable de :

- ✅ Expliquer le rôle d'Activator dans l'écosystème Real-Time Intelligence de Fabric
- ✅ Créer et configurer un projet Activator
- ✅ Définir des **objets** (entités métier) et leurs **propriétés** depuis un eventstream
- ✅ Concevoir des **règles** avec conditions complexes et filtres multi-critères
- ✅ Configurer des **actions automatisées** (email, Teams, Power Automate, webhooks)
- ✅ Tester et valider le déclenchement d'une règle

---

## Concepts clés

### Les 4 composants d'un Activator

| Composant | Description | Exemple |
|-----------|-------------|---------|
| **Objet** | Entité métier surveillée, identifiée de façon unique | Colis (ID: PackageId), Capteur (ID: SensorId) |
| **Propriété** | Valeur mesurée sur chaque objet | Temperature, Status, Amount |
| **Règle** | Condition déclenchant une action | Temperature > 41°C AND City = "Redmond" |
| **Action** | Réponse automatique au déclenchement | Email au service logistique |

### Types de conditions supportées

| Condition | Comportement |
|-----------|-------------|
| `Is greater than` | Se déclenche à **chaque** événement où la valeur est > seuil |
| `Increases above` | Se déclenche **une seule fois** lors du passage du seuil (évite les doublons) |
| `Decreases below` | Transition descendante sous un seuil |
| `Is equal to` | Valeur exacte atteinte |
| `Changes to` | Changement de valeur vers une valeur cible |
| `Is outside range` | Valeur hors d'un intervalle [min, max] |

### Sources de données compatibles

- **Eventstream** (source principale)
- **KQL Database** (Eventhouse)
- **Real-Time Hub** (Event Hubs, IoT Hub, Kafka)
- **Power BI** (datasets et rapports)

---

## Cas d'usage métier

| Secteur | Problème | Solution Activator |
|---------|----------|-------------------|
| **Logistique** | Médicaments mal réfrigérés pendant livraison | Température hors plage → Email service logistique |
| **Finance** | Détection de fraude en temps réel | Montant > seuil + pays inhabituel → Blocage + alerte |
| **Industrie 4.0** | Maintenance prédictive équipements | Vibration anormale → Ticket ITSM automatique |
| **E-commerce** | Rupture de stock imminente | Stock < seuil → Déclenchement réappro Power Automate |
| **Santé** | Surveillance patients critiques | Paramètres vitaux hors norme → Alerte soignant Teams |

---

## Fichiers de ce module

| Fichier | Type | Description |
|---------|------|-------------|
| [01. Utilisez Activator dans Microsoft Fabric.md](./01.%20Utilisez%20Activator%20dans%20Microsoft%20Fabric.md) | Cours | Cours complet — concepts, configuration, règles, actions |
| [11-data-activator.md](./11-data-activator.md) | Lab | Lab pratique guidé (anglais) — scénario livraison médicaments Redmond |

---

## Liens utiles

- **Module Microsoft Learn** : [https://learn.microsoft.com/fr-fr/training/paths/use-activator-microsoft-fabric/](https://learn.microsoft.com/fr-fr/training/paths/use-activator-microsoft-fabric/)
- **Documentation Activator** : [https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/data-activator-introduction](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/data-activator-introduction)
- **Lab GitHub** : [https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/11-data-activator.html](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/11-data-activator.html)
- **Conditions de détection** : [https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/data-activator-detection-conditions](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/data-activator-detection-conditions)

---

## Prérequis recommandés

Avant ce module, assurez-vous d'avoir complété :

1. **Bien démarrer avec Real-Time Intelligence** — pour comprendre l'architecture RTI de Fabric
2. **Utiliser Eventstream dans Microsoft Fabric** — pour comprendre les sources de données streaming
3. **Créer des tableaux de bord en temps réel** — pour contextualiser la surveillance des données

---

*Ce module fait partie du parcours certifiant **DP-700 : Microsoft Certified Fabric Data Engineer Associate***
