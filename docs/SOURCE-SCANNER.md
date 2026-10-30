# Source scanner

The first scanner is deliberately local and non-executing. It inventories files in a previously acquired source tree, computes SHA-256 over raw bytes, assigns a best-effort media type/format, and emits a source manifest.

```bash
python scripts/source_scanner.py ./source-checkout \
  --resource-id modern-physics-quadrivium-press \
  --source-uri https://github.com/QuadriviumPress/modernPhysics \
  --source-kind git_repository \
  --revision FULL_COMMIT_SHA \
  --branch-or-tag main \
  --output manifests/modern-physics-source.json
```

The scanner does not clone repositories, access the network, execute code, parse content, or establish licenses. Acquire the source separately, pin its commit, and record the acquisition method. Symlinks are skipped; common build/cache directories are excluded. Review exclusions before using the manifest as a complete archival inventory.

The output includes a tree digest derived from sorted relative paths and file hashes. Retrieval timestamp is intentionally separate from the content digest.
