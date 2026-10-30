# Parser adapter contract

Every adapter accepts a source snapshot directory plus an immutable run configuration and emits:
1. a manifest reference (never a rewritten source),
2. ordered chapter/section nodes,
3. typed content blocks,
4. citation and bibliography records,
5. figure/table/equation references,
6. extraction warnings and coverage metrics.

## Adapter requirements
- Deterministic output for identical bytes, configuration, and adapter version.
- Preserve source paths, line numbers, anchors, notebook cell IDs, PDF page numbers, and LaTeX labels.
- Retain raw source fragments alongside normalized values where feasible.
- Do not execute notebooks or embedded code.
- Keep math as LaTeX or source-native math; do not flatten it into prose.
- Mark OCR and heuristic structure recovery explicitly.
- Do not invent missing chapter titles, numbering, authors, or publication dates.
- Emit partial results with warnings when a source is incomplete.

## Format-specific discovery
- MyST/Jupyter Book: parse `myst.yml`, `_toc.yml`, `_config.yml`, frontmatter, directives, roles, labels and citations. TOC order is authoritative when valid.
- Jupyter: preserve notebook cell order, cell IDs, cell type, source, metadata, outputs and attachments. Outputs are data, not executable instructions.
- Bookdown/R Markdown: inspect `_bookdown.yml`, `_output.yml`, `index.Rmd`, chapter order, YAML and chunk options.
- LaTeX: resolve `\\input` and `\\include` within the snapshot root, detect cycles, preserve labels, bibliography keys, math environments and section hierarchy.
- PDF: retain page-index mapping, text spans and bounding boxes when available; OCR fallback must include engine, version, language and confidence.
- Markdown: parse heading hierarchy, frontmatter, links, fenced code, tables, images and reference definitions.

## Error states
`unsupported_format`, `missing_toc`, `broken_include`, `include_cycle`, `duplicate_anchor`, `unresolved_citation`, `ocr_required`, `low_confidence_structure`, `unsafe_path`, `license_scope_unknown`.
