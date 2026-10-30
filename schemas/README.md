# Schema index
- `resource.schema.json`: catalog resource.
- `source-manifest.schema.json`: immutable source snapshot and artifact hashes.
- `textbook.schema.json`: abstract work identity.
- `edition.schema.json`: distinct publication/revision.
- `chapter.schema.json`: hierarchical chapter/section structure.
- `content-block.schema.json`: typed extracted content.
- `ingestion-run.schema.json`: reproducible parser execution.
All schemas use JSON Schema Draft 2020-12. IDs are stable within their stated entity scope; provenance links must not be discarded during normalization.
