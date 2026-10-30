# Schema index
- `resource.schema.json`: catalog resource.
- `source-manifest.schema.json`: immutable source snapshot and artifact hashes.
- `textbook.schema.json`: abstract work identity.
- `edition.schema.json`: distinct publication/revision.
- `chapter.schema.json`: hierarchical chapter/section structure.
- `content-block.schema.json`: typed extracted content.
- `ingestion-run.schema.json`: reproducible parser execution.
All schemas use JSON Schema Draft 2020-12. IDs are stable within their stated entity scope; provenance links must not be discarded during normalization.

- `visual-asset.schema.json`: illustration, figure, chart, and diagram asset.
- `diagram-model.schema.json`: optional semantic graph representation of a diagram.
- `visual-form.schema.json`: reusable generalized visual structure and constraints.\n- `visual-component.schema.json`: reusable visual component vocabulary.\n- `visual-relationship.schema.json`: typed relationships between visual components.\n