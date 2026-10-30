# Ingestion specification
Pipeline: `discover → snapshot → classify → inspect → parse → normalize → extract → resolve citations → assess license → validate → index → report`.

| Adapter | Inputs | Preserve |
|---|---|---|
| MyST/Jupyter Book | Markdown, `myst.yml`, `_toc.yml` | directives, roles, TOC, labels, citations, math |
| Jupyter | `.ipynb` | ordered cells, cell types, source, metadata, outputs, attachments |
| Bookdown/R Markdown | `.Rmd`, `_bookdown.yml` | chapter order, YAML, chunks, citations |
| LaTeX | `.tex`, `.bib` | section hierarchy, includes, labels, equations, bibliography |
| PDF | `.pdf` | page mapping, reading order, figures, tables; OCR provenance |
| Markdown | `.md` | headings, links, code fences, tables, images |
| HTML/EPUB | `.html`, `.epub` | semantic hierarchy, anchors, links, media |

Preserve raw source files; normalized data is derivative. Never execute untrusted notebook cells or repository build scripts. Keep equations, code, figures, tables, citations, and exercises as typed blocks. Preserve PDF page mapping and label OCR text with engine/version/confidence. Record parser version, configuration, source commit, timestamps, hashes, and warnings.

States: `discovered`, `inspected`, `parseable`, `parsed`, `validated`, `indexed`, `quarantined`. Quarantined items remain recorded with a reason.
