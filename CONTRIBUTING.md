# Contributing
1. Verify the canonical source and classify its actual resource type.
2. Record title, creators where verified, source URL, repository URL, revision/release, and access date.
3. Assign subject identifiers from `registry/taxonomy/subjects.json`.
4. Preserve chapter/section ordering and source anchors.
5. Record separate license assertions for text, code, figures, datasets, notebooks, and third-party assets.
6. Use `unknown` when evidence is insufficient.
7. Run `python scripts/validate_registry.py`.
Use stable lowercase kebab-case IDs. A title or URL change does not automatically create a new intellectual work. Document corrections and retain historical provenance.
