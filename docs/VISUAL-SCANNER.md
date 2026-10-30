# Visual reference scanner

Discovers non-equation visuals without rendering or executing source. Supports Markdown images, HTML img tags, LaTeX includegraphics and figure environments, TikZ/PGF, PSTricks, Mermaid, and Graphviz.

Run:

    python scripts/visual_reference_scanner.py ./book-source --edition-id example-edition-1 --output build/visual-references.json

This produces a discovery queue, not a verified visual catalog. A later resolver must validate local targets, hash asset bytes, record dimensions, preserve vector originals, and associate captions and chapter context. No TeX, notebook, Mermaid, Graphviz, or build scripts are executed.
