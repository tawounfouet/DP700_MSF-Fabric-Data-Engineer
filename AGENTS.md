# AGENTS.md — DP-700 Microsoft Fabric Data Engineer

**Study repo** for Microsoft DP-700 (Fabric Data Engineer Associate) and related certs (DP-600 through DP-604, DP-3029). Pure Markdown — no code, no build, no tests.

## Directory layout

| Path | Content |
|------|---------|
| `Instructions/Labs/` | 47 lab tutorials (English), YAML frontmatter, 344 screenshots in `Images/` |
| `mslearn-training/` | 6 learning-path dirs (French), each with module Markdown |
| `_data/lab-metadata.yml` | Lab→cert mapping, category taxonomy |
| `resources/` | Study guide |

## Conventions & quirks

- **Lab frontmatter** uses `categories` and `courses` fields that must match the controlled values in `_data/lab-metadata.yml`.
- **French** = learning modules; **English** = lab files (labs reference GitHub repos `MicrosoftLearning/dp-data` and `mslearn-fabric`).
- **Lab 10 is intentionally skipped** in the numbering. No missing file.
- **Duplicate labs**: `15-design-semantic-model-scale.md` ≈ `15-design-scalable-semantic-models.md` (similar content, both kept).
- Some `mslearn-training/` module files are empty stubs.
- Labs under `mslearn-training/*/labs/` are **redundant copies** of files in `Instructions/Labs/`.
- External dependency: a Microsoft Fabric capacity (trial or paid) is required to run the labs.
