# Textbook Library development roadmap

This roadmap is an implementation-oriented backlog. Status describes repository artifacts, not claims that every capability has been exercised against production textbook sources.

## Completed foundations

- [x] Resource catalog, subject taxonomy, and resource record validation.
- [x] Source manifest, textbook, edition, chapter, content-block, and ingestion-run schemas.
- [x] Non-executing source-tree scanner with hashes and exclusions.
- [x] Initial MyST/Markdown content adapter and tests.
- [x] First-class visual asset and semantic diagram model schemas.
- [x] Visual reference discovery scanner and tests.
- [x] Generalized visual family taxonomy and 21 proposed visual forms.
- [x] Shared component and relationship vocabularies for generalized forms.
- [x] Transparent structural candidate matcher with evidence breakdown.
- [x] Visual form registry cross-reference validation and JSON Schema validation scripts.
- [x] CI workflow expanded to include registry checks, visual schema checks, matcher smoke test, and unit tests.

## Next implementation priorities

### P0 — Resolve and catalog actual visual assets
- [x] Resolve local image and vector references safely within source roots.
- [x] Hash source and asset bytes, detect supported formats and dimensions, and reject unsafe paths.
- [x] Distinguish embedded constructs (TikZ, PSTricks, Mermaid, Graphviz) from linked assets without executing them.
- [x] Emit schema-oriented visual-asset records and separate resolution reports.
- [x] Add tests for path traversal, external references, PNG metadata, and embedded constructs.
- [ ] Add broader image-format coverage, SVG edge cases, extension inference, and duplicate-asset detection.

### P1 — Connect textbook structure to visuals
- Extract figure numbers, captions, labels, page references, and nearby explanatory text.
- Link visual assets to edition, chapter, content block, concepts, citations, and generalized forms.
- Preserve uncertainty and competing figure-to-caption associations.
- Add figure sequence and cross-reference resolution.

### P1 — Build renderer adapters
- Add safe, isolated adapters for SVG, Mermaid, Graphviz, TikZ/CircuitikZ, PDF figure extraction, and notebook outputs.
- Preserve source-native assets; rendered previews are derivatives.
- Pin renderer versions, disable network access, and apply resource limits.

### P2 — Improve semantic interpretation
- Add OCR and label-region extraction.
- Represent spatial layout, graph topology, axes, units, legends, scale, and direction.
- Compare structural and visual similarity separately.
- Keep machine predictions, human corrections, and evidence as separate records.

### P2 — Broaden textbook ingestion
- Add adapters for Jupyter Book, Sphinx/MyST, Quarto, Bookdown, LaTeX, EPUB, and PDF.
- Preserve source line/page locations and original terminology.
- Add reproducible extraction manifests and parser version histories.

### P3 — Catalog governance and discovery
- Verify resource metadata and license scope against current canonical sources.
- Add resource deduplication and edition/work identity reconciliation.
- Add cross-resource concept and prerequisite relationships.
- Build faceted search by discipline, topic, level, format, license, and content coverage.

## Operating rules

- Never infer reuse permission from catalog inclusion.
- Never overwrite immutable source snapshots or prior extraction runs.
- Keep original assets separate from derived previews and semantic interpretations.
- Require evidence and review state for inferred classifications.
- A matcher score ranks candidates; it does not establish identity or correctness.
