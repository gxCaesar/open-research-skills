# Two diagram styles, six palettes

Use these as configurable starting points, not venue rules. Both Nature-family and
top-CS papers use pale blocks, white space and structured modules. The useful choice
is the visual relationship: object transformation or computational decomposition.
Keep an established project style unless a redesign is requested.

## Choose the visual grammar before the colour

| Profile | Composition and objects | Lines and labels | Good starting job |
|---|---|---|---|
| `nature-pastel` | Open white canvas; object-specific silhouettes, vectors or matrices; unequal space for the main transformation; a quiet field or small detail inset | Thin neutral connectors, direct labels, restrained round corners; dark text on light fills | Specimen-to-representation flow; lifecycle overview; a scientific object changing through a model |
| `conference-structured` | Compact aligned modules; repeated token/tensor states; clear model boundary; overview beside an expanded computational block | Consistent module geometry; stronger selected-module outline; training-only paths separated and labelled | Algorithm pipeline; model architecture; shared backbone and block detail |

These are authored profiles. Neither profile mandates equal cards, a fixed number of
stages, a particular architecture, or more annotations. A Nature architecture can use
aligned modules; a conference figure can be object-led. Use the source-defined graph
and remove optional branches that do not exist in the actual method.

## Select a palette

The [palette catalog](../shared/figure-core/assets/diagram-styles.json) is the single
source for exact colours. Each palette supplies three semantic fill/stroke pairs,
plus common white, dark ink and muted labels. Assign those roles to actual objects
once; a palette swap changes colours, not the graph, labels or category identities.

| ID | Name | Roles: primary / secondary / tertiary |
|---|---|---|
| `mist-blue` | N1 | Mist blue / sea glass / oat |
| `sage-lilac` | N2 | Sage / lilac / cream |
| `lilac-sand` | N3 | Lilac / ice blue / sand |
| `blue-orange` | C1 | Blue / apricot / slate |
| `indigo-teal` | C2 | Indigo / teal / wheat |
| `plum-cyan` | C3 | Plum / cyan / cool gray |

N1–N3 belong to `nature-pastel`; C1–C3 to `conference-structured`. The first is the
default in each family. These colours are original curated choices, not extracted
swatches or official publisher palettes. Use dark `ink` for essential text, including
inside coloured modules. Pale fills are grouping aids, not sufficient category cues:
retain direct labels, shapes or line patterns. Accent strokes are not small-text inks.

See the [editable style library](design-template-library.md#two-style-library) for
four original examples and two palette boards. Inspect the actual preview before
designing. A palette board is a choice aid, not a figure to paste into a manuscript.

## Apply the selection

A user may name a style, a palette ID, or a colour direction in ordinary language.
Resolve to the nearest catalog option without an extra approval question when the
choice is reversible and no project palette is locked. For a new project:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/init_figure_project.py" <new-project> \
  --figure-id <id> --mode flowchart --layout-profile custom --page-width-mm 180 \
  --diagram-style nature-pastel --palette sage-lilac
```

The custom width is an authoring example, not a publisher requirement. `--palette`
alone infers the family; `--diagram-style` alone selects its default palette. A
family/palette mismatch is rejected. No flags preserves the legacy starter. Selection
refuses an existing `figure_spec.json`; do not reinitialize a completed figure to
recolour it.

Initialization records the chosen style and writes the same colours to
`figure_spec.json` → `style.colors` and `palette.json`. The shared renderer consumes
the former. Use semantic keys `primary_fill`, `primary_stroke`, `secondary_fill`,
`secondary_stroke`, `tertiary_fill`, and `tertiary_stroke` in new diagram elements.
The initializer colours the starter divider; it does **not** generate a finished
diagram or automatically transform its layout. The author applies the selected visual
grammar using the native template or canonical scene. Existing hue-named roles remain
for compatibility and are not automatically recoloured by a semantic palette change.

For every new or redesigned schematic, carry the selected grammar and role colours into
[image concept to editable vector](image-concept-to-vector.md). Generate an original
composition using the inspected template as a design reference, then reconstruct its
objects natively. Keep the scientific source authoritative for arrows and notation.
For a small edit to an approved native design, edit that scene directly. In either route,
inspect the actual exported result and a representative edit, not just its thumbnail.

## Source-informed design lessons

Figures and captions were inspected on 2026-09-09. The original paper images are not
distributed. These concise lessons describe composition, not the papers' scientific
claims or a licence to reuse their artwork.

- **scGPT, Nature Methods (2024), Fig. 1a–c.** A paired lifecycle overview sits beside
  embedding and transformer detail. White space and a few phase colours distinguish
  the overview from model internals. Borrow that hierarchy; do not inherit its
  attention design, corpus size, task claims or lower-panel embedding displays.
  [Publisher article and figure](https://www.nature.com/articles/s41592-024-02201-0).
- **scFoundation, Nature Methods (2024), Fig. 1a–b.** Repeated typed tiles traverse a
  pale model field; a legend explains states and a pooled branch is visually separate.
  Borrow the typed-object rhythm and overview-to-detail relationship, not its
  RDA objective, masking semantics, token meanings or downstream findings.
  [Publisher article and figure](https://www.nature.com/articles/s41592-024-02305-7).
- **DiT, ICCV (2023), Fig. 3, PDF p. 3.** A main architecture occupies the left;
  alternative block details sit on the right. Aligned blocks and warm/cool operator
  roles make a compact computation readable. This is also a pastel design: venue
  families overlap. Do not transfer its latent dimensions, conditioning choices or
  selected adaLN-Zero design into a generic template.
  [Official proceedings PDF](https://openaccess.thecvf.com/content/ICCV2023/papers/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.pdf).

The Nature references were visually inspected from publisher figure PNGs; publisher
PDF endpoints returned HTML, so no PDF-page claim is made for them. Earlier inspected
diaTracer, AlphaFold 3 and DPO precedents remain in the
[design template library](design-template-library.md#inspected-paper-precedents).

The current [Nature research figure guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)
supports legible dark text, accessible encoding and sufficient contrast. The
[Nature commissioned-content artwork guide](https://www.nature.com/documents/natrev-artworkguide.pdf)
also illustrates selective colour emphasis and quiet backgrounds, but concerns
commissioned conceptual artwork; it is not a universal original-research specification.
Neither source prescribes the six palettes above.
