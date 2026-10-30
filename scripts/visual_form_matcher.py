#!/usr/bin/env python3
"""Rank generalized visual-form candidates using transparent structural evidence.

Input JSON:
{
  "component_types": ["x_axis", "data_series"],
  "relationship_types": ["plotted_on_axis"],
  "domains": ["physics"],
  "required_component_types": ["x_axis"]
}
This is a candidate-ranking aid, not an image classifier or semantic authority.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def jaccard(left, right):
    a, b = set(left), set(right)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def score_candidate(candidate, form):
    sig = form.get("structural_signature", {})
    observed_components = set(candidate.get("component_types", []))
    observed_relationships = set(candidate.get("relationship_types", []))
    form_components = set(sig.get("component_types", []))
    form_relationships = set(sig.get("relationship_types", []))
    component_score = jaccard(observed_components, form_components)
    relationship_score = jaccard(observed_relationships, form_relationships)
    candidate_domains = set(candidate.get("domains", []))
    form_domains = set(form.get("applicable_domains", []))
    domain_score = 1.0 if "all_stem" in form_domains or not candidate_domains else (
        len(candidate_domains & form_domains) / len(candidate_domains | form_domains)
    )
    required = set(candidate.get("required_component_types", []))
    required_coverage = 1.0 if not required else len(required & form_components) / len(required)
    weights = {"components": 0.35, "relationships": 0.35, "domains": 0.15, "required_coverage": 0.15}
    total = (
        component_score * weights["components"]
        + relationship_score * weights["relationships"]
        + domain_score * weights["domains"]
        + required_coverage * weights["required_coverage"]
    )
    missing = sorted(required - form_components)
    return {
        "form_id": form["form_id"],
        "name": form["name"],
        "score": round(total, 4),
        "evidence": {
            "component_similarity": round(component_score, 4),
            "relationship_similarity": round(relationship_score, 4),
            "domain_similarity": round(domain_score, 4),
            "required_component_coverage": round(required_coverage, 4),
            "missing_required_components": missing,
            "shared_components": sorted(observed_components & form_components),
            "shared_relationships": sorted(observed_relationships & form_relationships),
        },
    }


def rank_forms(candidate, forms, limit=10):
    ranked = [score_candidate(candidate, form) for form in forms]
    return sorted(ranked, key=lambda item: (-item["score"], item["form_id"]))[:limit]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="Candidate visual structure JSON")
    parser.add_argument("--forms", type=Path, default=ROOT / "registry/visual-forms/forms.json")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--threshold", type=float, default=0.35)
    args = parser.parse_args()
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    forms_data = json.loads(args.forms.read_text(encoding="utf-8"))
    ranked = rank_forms(candidate, forms_data.get("forms", []), args.limit)
    output = {
        "method": "weighted_structural_similarity_v1",
        "threshold": args.threshold,
        "classification": "candidate_matches_found" if ranked and ranked[0]["score"] >= args.threshold else "no_confident_form_match",
        "ranked_matches": ranked,
        "limitations": [
            "Ranks only supplied component, relationship, and domain evidence.",
            "Does not inspect pixels or infer diagram semantics from an image.",
            "A low score may reflect incomplete extraction, an unrepresented form, or a genuinely different structure.",
            "Human review is required before adding or accepting a generalized form."
        ]
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
