# Use cases end-to-end

Ce dossier regroupe les cas pratiques complets de la journee.

| Use case | Source | Objectif pedagogique |
| --- | --- | --- |
| `01-books-toscrape/` | Site pedagogique `books.toscrape.com` | Montrer une plateforme data a partir d'une source web semi-structuree |
| `02-mslearn-sales-medallion/` | Exemple Microsoft Learn `mslearn-fabric` | Rejouer un cas officiel ventes avec architecture medaillon, Delta et modele etoile |

## Choix pour l'animation

Pour l'apres-midi, vous pouvez choisir :

- **Books to Scrape** si vous voulez un cas plus vivant, avec scraping, HTML brut, parsing et qualite.
- **Microsoft Learn Sales Medallion** si vous voulez rester proche des labs officiels DP-700/DP-601 et eviter la dependance a un site externe.

Le fil conducteur Fabric reste le meme :

```text
Source -> Bronze -> Silver -> Gold -> SQL endpoint -> Modele semantique -> Power BI
```

