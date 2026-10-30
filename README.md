# STEM Textbook Library

A structured, provenance-aware registry of STEM textbooks, open educational resources, companion notebooks, datasets, simulations, laboratory resources, and scientific software.

## Purpose
Catalog learning resources while preserving source identity, editions, chapter structure, subject classification, citations, licensing evidence, and inspection history. The default is to link to canonical sources, not mirror copyrighted content.

## Principles
- Distinguish textbooks from companion notebooks, software, datasets, and course materials.
- Preserve source URLs, repository commits/releases, paths, retrieval dates, and hashes.
- Assess licenses independently for text, code, figures, datasets, notebooks, and third-party assets.
- Treat unknown license status as unknown, never as open permission.
- Preserve original structure and terminology during ingestion.
- Use additive source snapshots and extraction runs.
- Label inferred classifications and uncertain metadata.

## Layout
- `registry/taxonomy/`: subject taxonomy and relationships.
- `registry/resources/`: resource catalog records.
- `schemas/`: machine-readable validation schemas.
- `docs/`: architecture, ingestion, licensing, and contribution rules.
- `scripts/`: validation utilities.
- `.github/workflows/`: automated checks.

## Initial scope
The initial catalog covers physics, nuclear and accelerator physics, quantum mechanics, materials science, thermodynamics, biology, genetics, neuroscience, computational science, seismology, CFD, operations research, and medical physics. Records distinguish textbooks from companion and software resources.

## Licensing note
The repository's existing `LICENSE` is CC0 1.0. It applies only to contributions whose rights are held by the contributor and intentionally dedicated under CC0; it does not change the licenses of third-party works described in this catalog. See [Licensing](docs/LICENSING.md).

## Status
Initial registry scaffold. Catalog entries are discovery/inspection candidates, not legal or scientific certifications. See [Architecture](docs/ARCHITECTURE.md), [Ingestion](docs/INGESTION.md), [Licensing](docs/LICENSING.md), and [Contributing](CONTRIBUTING.md).


## Visual and diagram preservation

Illustrations, diagrams, charts, maps, schematics, and scientific plots are first-class records, independent of equation extraction. See [visual ingestion](docs/VISUAL-INGESTION.md), [renderer strategy](docs/VISUAL-RENDERERS.md), and [visual reference scanner](docs/VISUAL-SCANNER.md). The scanner discovers source references; it does not execute or render untrusted source. Original visual assets must be preserved separately from machine-generated semantic interpretations.

## Generalized visual forms

The library now distinguishes visual families, generalized forms, specialized variants, reusable component types, relationship types, rendering templates, and individual visual instances. See [the generalized visual forms guide](docs/GENERALIZED-VISUAL-FORMS.md) and the seeded [forms](registry/visual-forms/forms.json), [components](registry/visual-forms/components.json), and [relationships](registry/visual-forms/relationships.json) registries.

## Visual form matching

A transparent structural matcher ranks candidate generalized forms using component, relationship, and domain evidence. See [the matching guide](docs/VISUAL-FORM-MATCHING.md), [matcher script](scripts/visual_form_matcher.py), and [registry validator](scripts/validate_visual_forms.py). The form registry currently contains 21 proposed forms with a shared component and relationship vocabulary. These are candidate definitions, not approved scientific standards.
