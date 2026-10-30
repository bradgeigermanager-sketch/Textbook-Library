# Architecture
Pipeline: discovery → source snapshot → classification → extraction → canonical normalization → evidence/licensing → validation → publication/indexing.

Core entities: Resource, Edition, SourceArtifact, Chapter, Section, ContentBlock, Citation, LicenseAssertion, SubjectAssignment, ExtractionRun.

Keep intellectual resource identity distinct from edition, source revision, and parser output. New upstream revisions or parser versions create new snapshots/runs; do not overwrite historical provenance.

The registry may exchange process and procedure records with the Canonical Process Library through stable identifiers and documented interfaces. Neither repository should depend on the other.
