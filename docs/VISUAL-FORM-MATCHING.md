# Visual form matching engine

The first matcher is deliberately transparent and conservative. It ranks candidate forms from extracted structural evidence; it does not classify pixels or claim to understand an image.

## Candidate input
Provide arrays of `component_types`, `relationship_types`, and optional `domains` and `required_component_types`. Terms should use the same vocabulary as the form registry.

## Scoring
The current score is a weighted combination:
- 35% component-type Jaccard similarity
- 35% relationship-type Jaccard similarity
- 15% domain overlap
- 15% required-component coverage

Each result includes component and relationship intersections, missing required components, and the component scores. The weights and threshold are explicit CLI parameters, not hidden model behavior.

## Run
```bash
python scripts/visual_form_matcher.py candidate.json
python scripts/visual_form_matcher.py candidate.json --threshold 0.5 --limit 5
python scripts/validate_visual_forms.py
```

## Interpretation
A high score means that the supplied extracted structure resembles a registered form. It is not proof of semantic identity. A low score can mean poor extraction, an absent form, or a different structure. Human review is required before a form is accepted or a new form is created. Future versions should support graph topology, spatial constraints, notation profiles, optional/required components, and evidence provenance.

## Example

A sample candidate is provided at `examples/visual-form-candidate.json`. Run it with the command above to inspect the ranked candidate forms and the evidence contributing to each score.
