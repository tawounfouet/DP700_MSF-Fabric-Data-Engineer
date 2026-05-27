# Sources exploitees

Consultation : 2026-05-27.

## Sources locales du depot

- `README.md` : structure DP-700, themes cles, parcours et prerequis.
- `INDEX.md` : inventaire des modules, labs, images et mapping DP-700.
- `resources/1. Guide d’étude de l’examen DP-700.md` : domaines de competences DP-700 au 20 avril 2026.
- `mslearn-training/0. Commencez avec Microsoft Fabric/00. Découvrir et se connecter aux données dans OneLake.md` : OneLake, catalogue, raccourcis, SQL endpoint.
- `mslearn-training/II. Implémenter un Lakehouse avec Microsoft Fabric/07. Organiser un lakehouse Fabric à l’aide de la conception d’architecture en médaillon.md` : module medaillon.
- `Instructions/Labs/01-lakehouse.md` : creation lakehouse, table Delta, SQL endpoint.
- `Instructions/Labs/04-ingest-pipeline.md` : pipeline, Copy Data, notebook activity.
- `Instructions/Labs/05-dataflows-gen2.md` : Dataflow Gen2 et pipeline.
- `Instructions/Labs/03b-medallion-lakehouse.md` : lab medaillon bronze, silver, gold, semantic model.
- `../../../../ms-learn/mslearn-fabric/Instructions/Labs/03b-medallion-lakehouse.md` : version source Microsoft Learn du lab medaillon.
- `../../../../ms-learn/mslearn-fabric/Allfiles/Labs/01/orders/` : fichiers CSV Microsoft Learn utilises dans le use case Sales Medallion.
- Images locales selectionnees depuis `Instructions/Labs/Images/` et `mslearn-training/.../media/`.

## Sources en ligne

- Microsoft Fabric overview : https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview
- Architecture medaillon Fabric avec OneLake : https://learn.microsoft.com/fr-fr/fabric/onelake/onelake-medallion-lakehouse-architecture
- SQL analytics endpoint du lakehouse : https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint
- Preparation et transformation dans Fabric : https://learn.microsoft.com/en-us/fabric/fundamentals/prepare-transform-data
- Dataflow Gen2 dans un pipeline : https://learn.microsoft.com/en-us/fabric/data-factory/tutorial-dataflows-gen2-pipeline-activity
- Notebooks Fabric : https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook
- Lakehouse et tables Delta : https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-and-delta-tables
- Guide DP-700 Microsoft Learn : https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700
- Books to Scrape : https://books.toscrape.com/

## Points confirmes en ligne

- Fabric est presente comme une plateforme SaaS end-to-end pour ingestion, traitement et visualisation.
- L'architecture medaillon est l'approche de conception recommandee pour Fabric avec OneLake.
- Le SQL analytics endpoint fournit une surface T-SQL en lecture seule sur les tables Delta du lakehouse.
- Dataflow Gen2 peut etre utilise seul ou comme activite de pipeline.
- Les notebooks Fabric sont adaptes aux traitements Spark, ingestion, preparation et transformation.
- Books to Scrape affiche 1000 resultats, 20 livres par page, et indique que prix et notes sont fictifs.
