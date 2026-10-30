#!/usr/bin/env python3
"""Validate generalized visual-form registry structure and cross-references."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "registry/visual-forms"
ID = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$")
errors = []


def load(name, key):
    path = BASE / name
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        records = data.get(key, [])
        if not isinstance(records, list):
            raise ValueError(f"{key} must be an array")
        return records
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return []


families_data = json.loads((ROOT / "registry/taxonomy/visual-families.json").read_text(encoding="utf-8"))
families = {item.get("family_id") for item in families_data.get("families", [])}
forms = load("forms.json", "forms")
components = load("components.json", "components")
relationships = load("relationships.json", "relationships")

for label, records, key in [
    ("forms", forms, "form_id"),
    ("components", components, "component_type_id"),
    ("relationships", relationships, "relationship_type_id"),
]:
    seen = set()
    for index, record in enumerate(records):
        identifier = record.get(key, "")
        if not ID.fullmatch(identifier):
            errors.append(f"{label}[{index}]: invalid {key}: {identifier!r}")
        if identifier in seen:
            errors.append(f"{label}[{index}]: duplicate {key}: {identifier}")
        seen.add(identifier)

form_ids = {item.get("form_id") for item in forms}
component_terms = {item.get("canonical_term") for item in components if item.get("canonical_term")}
relationship_ids = {item.get("relationship_type_id") for item in relationships}
relationship_terms = {item.get("canonical_term") for item in relationships if item.get("canonical_term")}
for index, relationship in enumerate(relationships):
    inverse = relationship.get("inverse_relationship")
    if inverse and inverse not in relationship_ids:
        errors.append(f"relationships[{index}]: unknown inverse_relationship {inverse!r}")

for index, form in enumerate(forms):
    if form.get("family_id") not in families:
        errors.append(f"forms[{index}]: unknown family_id {form.get('family_id')!r}")
    parent = form.get("parent_form_id")
    if parent and parent not in form_ids:
        errors.append(f"forms[{index}]: unknown parent_form_id {parent!r}")
    signature = form.get("structural_signature", {})
    for term in signature.get("component_types", []):
        if term not in component_terms:
            errors.append(f"forms[{index}]: component type has no canonical vocabulary record: {term}")
    for term in signature.get("relationship_types", []):
        if term not in relationship_terms:
            errors.append(f"forms[{index}]: relationship type has no canonical vocabulary record: {term}")
    if not signature.get("component_types"):
        errors.append(f"forms[{index}]: structural_signature.component_types is empty")
    if not signature.get("relationship_types"):
        errors.append(f"forms[{index}]: structural_signature.relationship_types is empty")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Visual form registry checks passed: {len(forms)} forms, {len(components)} components, {len(relationships)} relationships.")
