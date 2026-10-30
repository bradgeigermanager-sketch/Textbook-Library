# Generalized visual forms

This registry describes reusable structures underlying individual textbook illustrations and diagrams. A form is not an image and does not replace any source visual.

- Families classify broad visual purposes and structures.
- Forms describe reusable arrangements and constraints.
- Component types define reusable visual/semantic building blocks.
- Relationship types define typed connections among components.
- Instances remain in the visual asset catalog and link to one or more form IDs.

Do not infer a form solely from appearance. Preserve source evidence and uncertainty. Forms may be cross-disciplinary or discipline-specific and may have parent/child specialization relationships.

## Registry size and validation

The initial seed contains 21 proposed forms, a shared vocabulary of component types and relationship types, and a structural matcher. Run `python scripts/validate_visual_forms.py` to check identifiers, family references, parent references, inverse relationships, and signature-to-vocabulary references. Run `python -m unittest discover -s tests -v` for tests.
