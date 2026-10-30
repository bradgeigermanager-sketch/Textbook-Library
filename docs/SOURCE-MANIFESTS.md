# Source manifests and identity model

## Separate identity layers
- **Resource**: the cataloged intellectual/educational resource, such as a textbook or companion.
- **Textbook identity**: the abstract work across editions and formats.
- **Edition**: a distinct publication/revision of that work.
- **Source snapshot**: exact upstream repository/archive state at a commit, tag, or retrieval time.
- **Artifact**: a file within that snapshot, identified by path, media type, byte length, and SHA-256.
- **Ingestion run**: one deterministic parser execution over a snapshot with pinned adapter versions.

Never use a branch name alone as an immutable revision. Resolve Git sources to a commit SHA. If resolution is unavailable, mark the revision unknown rather than inventing one.

## Manifest rules
1. Record retrieval time in UTC ISO 8601.
2. Hash file bytes before text decoding or normalization.
3. Exclude generated caches and bulky build output by explicit, versioned rules; record exclusions in the run report.
4. Do not follow symlinks outside the source root.
5. Do not execute build scripts, notebooks, macros, or repository code during discovery.
6. Keep license evidence scoped to the artifact classes it actually covers.
7. A changed file creates a new snapshot artifact; do not mutate a prior manifest.

## Stable identifiers
Use readable slugs for resource/textbook IDs. Edition IDs should combine textbook ID with a verified edition key or source revision. Chapter IDs should be derived from edition ID plus source path and anchor; preserve the source's original numbering separately. Content block IDs should be derived from the source artifact digest, structural location, and block order. Hash-based IDs are reproducible, but a corrected parse is a new extraction version, not a claim that the source changed.

## Manifest example
```json
{
  "manifest_id": "manifest-example-2026-01",
  "resource_id": "example-textbook",
  "edition_id": "example-textbook-edition-1",
  "source_uri": "https://github.com/example/book",
  "source_kind": "git_repository",
  "retrieved_at": "2026-01-01T00:00:00Z",
  "revision": "full-commit-sha",
  "branch_or_tag": "main",
  "scanner_version": "0.1.0",
  "artifacts": [
    {
      "path": "chapters/ch01.md",
      "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "byte_size": 1234,
      "media_type": "text/markdown",
      "detected_format": "markdown",
      "included": true
    }
  ]
}
```
