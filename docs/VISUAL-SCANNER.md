# Visual reference scanner

Discovers non-equation visuals without rendering or executing source. Supports Markdown images, HTML img tags, LaTeX includegraphics and figure environments, TikZ/PGF, PSTricks, Mermaid, and Graphviz.

Run:

    python scripts/visual_reference_scanner.py ./book-source --edition-id example-edition-1 --output build/visual-references.json

This produces a discovery queue, not a verified visual catalog. The local resolver described below turns that queue into schema-oriented catalog candidates and a separate resolution report. Caption and chapter association remain subsequent enrichment steps. No TeX, notebook, Mermaid, Graphviz, or build scripts are executed.


## Resolve discovered references

First scan the source tree, then resolve the resulting discovery JSON:

    python scripts/visual_reference_scanner.py ./book-source --edition-id example-edition-1 --output build/visual-references.json
    python scripts/visual_asset_resolver.py ./book-source build/visual-references.json --output build/visual-assets.json

The resolver emits schema-oriented visual asset records and a separate resolution report. It resolves only local files within the source root; external URLs are recorded as unresolved and are never fetched. Parent traversal, absolute paths, unsafe separators, symlinks, and paths escaping the root are rejected. It hashes source and asset bytes, records media type, format, byte size, and dimensions when safely detectable. Extension inference is attempted only when the reference omits an extension.

TikZ, PSTricks, Mermaid, Graphviz, and LaTeX figure environments are recorded as embedded source constructs. They are not executed or rendered. Original files are not copied or modified.
