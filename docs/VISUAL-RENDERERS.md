# Visual renderer registry

Rendering is a pluggable capability, not a prerequisite for preserving a visual.

| Source family | Preferred strategy | Safe fallback |
|---|---|---|
| Raster images | Pillow/ImageMagick-compatible metadata and preview | Preserve original file |
| SVG | SVG renderer plus conservative XML parser | Preserve SVG source |
| PDF figures | PDF page crop and embedded-image extraction | Preserve PDF with page reference |
| TikZ/PGF | Isolated TeX toolchain with pinned packages | Preserve source and mark source-only |
| Mermaid | Pinned Mermaid CLI or compatible service | Preserve diagram source |
| Graphviz | Pinned Graphviz renderer | Preserve DOT |
| draw.io | diagrams.net export | Preserve XML |
| Notebook outputs | Read stored outputs and attachments | Preserve notebook JSON |
| HTML/Sphinx/MyST | Resolve local figure references and directives | Preserve markup and unresolved reference |

## Execution boundary

Do not run arbitrary repository build scripts, notebook cells, shell commands, or TeX package installation from untrusted sources. Rendering should happen in a sandbox with network disabled, resource/time limits, pinned tool versions, and a read-only source mount. Record renderer version, options, input digest, output digest, and warnings.

## Registry entry shape

A renderer registry entry should include renderer ID, supported input formats, output formats, version constraint, sandbox profile, determinism level, security notes, and availability status. Renderer presence does not imply that every source file is safe or renderable.
