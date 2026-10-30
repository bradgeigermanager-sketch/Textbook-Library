# MyST / Markdown adapter

The initial adapter extracts heading hierarchy, paragraphs, simple lists, fenced code blocks and display equations from Markdown-compatible files. It does not execute code or evaluate MyST directives.

Install the optional YAML dependency to use a Jupyter Book `_toc.yml` as an ordering hint:

```bash
python -m pip install pyyaml
```

Run:

```bash
python scripts/myst_adapter.py ./book-source \
  --edition-id modern-physics-edition-1 \
  --output-dir build/modern-physics
```

Outputs:
- `chapter-nodes.json`
- `content-blocks.json`
- `ingestion-report.json`

This first version is intentionally conservative. It does not yet fully parse MyST directives, roles, cross-references, bibliography syntax, embedded figures, admonitions, or all nested TOC forms. Review warnings and compare extracted counts against the source before treating output as complete.
