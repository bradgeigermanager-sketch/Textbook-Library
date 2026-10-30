#!/usr/bin/env python3
"""Dependency-free structural checks for registry JSON records."""
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ID=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TYPES={"textbook","textbook_companion","lecture_notes","reference_database","scientific_software","dataset","simulation","educational_material","educational_platform","study_notes_collection","laboratory_resource"}
errors=[]
for p in sorted((ROOT/"registry").rglob("*.json")):
    try: data=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"{p}: invalid JSON: {e}"); continue
    for i,r in enumerate(data.get("records",[])):
        w=f"{p.relative_to(ROOT)} records[{i}]"
        for k in ("resource_id","title","resource_type","source","subjects","record_status"):
            if k not in r: errors.append(f"{w}: missing {k}")
        if not ID.fullmatch(r.get("resource_id","")): errors.append(f"{w}: invalid resource_id")
        if r.get("resource_type") not in TYPES: errors.append(f"{w}: invalid resource_type")
        if not r.get("subjects"): errors.append(f"{w}: subjects must not be empty")
        if not str(r.get("source",{}).get("canonical_url","")).startswith(("https://","http://")): errors.append(f"{w}: invalid canonical_url")
if errors: print("\n".join(errors),file=sys.stderr); sys.exit(1)
print("Registry structural checks passed.")
