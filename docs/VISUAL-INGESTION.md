# Illustration, diagram, and visual-content ingestion

## Principle

A visual is a first-class instructional resource. Do not reduce it to a file attachment, a caption, or a paragraph. Store the original asset, its placement and source coordinates, its caption and labels, its instructional purpose, and (where feasible) a separate semantic model of the depicted entities and relationships.

## Three linked layers

1. **Visual asset** — original bytes or stable source reference, media type, dimensions, vector/raster status, digest, and rendering information.
2. **Semantic interpretation** — visual type, labels, regions, symbols, nodes, edges, directionality, units, legends, and uncertainty.
3. **Instructional context** — textbook, edition, chapter, nearby text, figure number, caption, references, learning objectives, and related concepts.

A semantic interpretation must never overwrite or replace the original visual.

## Visual families

- Scientific plots and charts: axes, units, scales, data series, error bars, legends, annotations.
- Structural diagrams: components, containment, adjacency, orientation, labels.
- Process diagrams: stages, transitions, inputs, outputs, feedback loops, direction.
- Physical schematics: apparatus, circuits, free-body diagrams, optical paths, particle detectors.
- Biological and medical illustrations: anatomical structures, cell compartments, tissue, pathways, imaging plates.
- Chemistry: molecular structures, reaction schemes, orbital depictions, energy diagrams.
- Geography and Earth science: maps, cross-sections, stratigraphic columns, seismic sections.
- Conceptual illustrations: taxonomies, comparisons, timelines, explanatory drawings.

## Source formats and rendering strategy

| Source | Preserve | Render / interpret |
|---|---|---|
| PNG, JPEG, TIFF, WebP | Original bytes, dimensions, color profile if available | Image preview, OCR, region annotation |
| SVG | Original XML and digest | Native SVG renderer; parse labels and shapes conservatively |
| PDF | Original PDF and page coordinates | Extract embedded images/vector drawings; page crop preview |
| LaTeX `\\includegraphics` | Source command, options, target path | Resolve local asset and render it independently |
| TikZ / PGF | Source fragment, packages, labels | Optional isolated LaTeX render; never assume equation rendering |
| PSTricks | Source and dependencies | Dedicated renderer or source-only fallback |
| Mermaid | Original diagram source | Mermaid renderer when available |
| Graphviz DOT | DOT source | Graphviz renderer when available |
| draw.io / diagrams.net | XML source | Native export or compatible renderer |
| Jupyter notebooks | Markdown image refs, outputs, attachments, cell IDs | Preserve outputs and attachment references; never execute notebook cells |
| HTML / MyST | `img`, `figure`, directives, alt text, captions | Resolve relative paths safely |

## Extraction rules

1. Preserve original asset bytes and calculate SHA-256 before conversion.
2. Record both source-relative path and exact placement (page, line, anchor, notebook cell, or LaTeX label).
3. Keep figure numbering and caption text exactly as published; store normalized search text separately.
4. Resolve relative paths only inside the pinned source snapshot. Reject path traversal and external fetches unless separately authorized.
5. Preserve SVG, TikZ, Mermaid, DOT, and draw.io source even when a renderer is unavailable.
6. Rendering failure is not extraction failure. Use `source_only` status and retain the asset.
7. Never rasterize a vector source as the sole retained representation.
8. OCR labels and classify visual type as machine-extracted hypotheses, not verified facts.
9. Keep separate confidence values for OCR, type classification, component detection, and relationship inference.
10. Human verification is required before a semantic diagram is treated as authoritative.

## LaTeX is not synonymous with mathematics

A LaTeX document can contain non-equation visuals through `figure`, `includegraphics`, `tikzpicture`, `pgfpicture`, PSTricks, and externalized graphics. These must be sent to the visual pipeline, not the equation pipeline. Equations remain mathematical content blocks; figures and diagrams become visual assets and optional diagram models.

## Relationship graph

A visual can be:
- contained in a chapter/section;
- referenced by a paragraph or exercise;
- captioned by a figure caption;
- composed of subfigures;
- explained by one or more concepts;
- supported by cited sources;
- linked to another visual as a sequence, comparison, detail, or alternative view.

Represent each relation as an explicit typed edge with provenance. Do not infer equivalence merely from visual similarity.

## Accessibility and quality control

Store source alt text and separately generated long descriptions. Keep OCR text with bounding boxes when available. Preserve color-independent meaning, symbol legends, units, axis labels, scale, and direction. Flag low-resolution, clipped, illegible, missing, or unresolved assets. A generated description must not be presented as publisher-authored alt text.

## Outputs

The visual adapter should emit:
- visual asset records;
- source-location records;
- optional semantic diagram models;
- rendering and extraction reports;
- unresolved asset references;
- quality warnings and confidence measures.
