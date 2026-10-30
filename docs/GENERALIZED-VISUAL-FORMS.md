# Generalized visual forms library

## Purpose
Capture reusable visual structures independently of individual textbook images. Each generalized form defines a recognizable arrangement, its component vocabulary, permitted relationships, parameters, constraints, variants, and possible renderers.

## Form vs. instance
- A **family** is a broad category (for example, quantitative plots).
- A **form** is a reusable structural pattern (for example, Cartesian x-y plot).
- A **variant** specializes a form (for example, logarithmic x-y plot).
- A **template** is a parameterized construction recipe that can generate a new visual.
- An **instance** is an actual textbook figure or newly authored diagram.

A source image may instantiate several forms. A form can have many instances. Similar appearance alone does not establish semantic equivalence.

## Recommended identification procedure
1. Identify the visual's apparent instructional role and broad family.
2. Identify its component types and their attributes.
3. Extract relationships, directionality, ordering, spatial constraints, and measurement semantics.
4. Compare the candidate structure with existing forms.
5. Assign an existing form if its required structure and constraints fit.
6. Propose a child form or new form if important structural features differ.
7. Record alternative classifications and uncertainty when multiple forms fit.
8. Preserve the original visual and the evidence supporting the classification.

## Matching and specialization
Use structural signatures rather than image similarity alone. Compare component-type overlap, relationship-type overlap, required-component satisfaction, graph topology, ordering, spatial constraints, and domain-specific semantics. Missing components may be due to cropping or incomplete extraction; do not automatically reject a match. Record a match score and the evidence behind it.

## Templates
A rendering template is separate from a form definition. The form describes what a visual means and the constraints it obeys; the template describes how to draw it in SVG, TikZ, Mermaid, Graphviz, CircuitikZ, Vega-Lite, or another format. A single form may have multiple renderer templates.

## Governance
All initial forms are proposed, not authoritative standards. Promotion to reviewed/accepted requires documented examples, source references, constraints, and review. Retain deprecated forms and redirects rather than reusing identifiers. IDs are immutable.

## Examples
See `registry/visual-forms/forms.json`, `components.json`, and `relationships.json`. These are initial seeds, deliberately limited and subject to review.
