#!/usr/bin/env python3
"""Validate generalized visual registries against JSON Schema Draft 2020-12."""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
JOBS = [
    ("schemas/visual-form.schema.json", "registry/visual-forms/forms.json", "forms"),
    ("schemas/visual-component.schema.json", "registry/visual-forms/components.json", "components"),
    ("schemas/visual-relationship.schema.json", "registry/visual-forms/relationships.json", "relationships"),
]
errors = []
validated = 0
for schema_path, data_path, key in JOBS:
    try:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        data = json.loads((ROOT / data_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for index, record in enumerate(data.get(key, [])):
            for error in validator.iter_errors(record):
                location = ".".join(str(part) for part in error.absolute_path)
                errors.append(f"{data_path} {key}[{index}] {location}: {error.message}")
            validated += 1
    except Exception as exc:
        errors.append(f"{schema_path} / {data_path}: {exc}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Visual JSON Schema validation passed: {validated} records across {len(JOBS)} schemas.")
