# Scientific figure visual contract

## Overall character

Use an open white canvas, precise alignment, restrained colour, sparse copy, and a
reading path that survives final print size. A supplied journal template or approved
figure overrides the default palette, but never the evidence boundary.

## Geometry and type

- Lock physical width before drawing; use an explicit custom width when the target is
  not one of the dated built-in profiles.
- Author at final size. Do not use `bbox_inches="tight"` or a document-level resize that
  changes both canvas and rendered type.
- Use a sans-serif family accepted by the target. The Nature profiles use Arial or
  Helvetica with 5 pt as the floor and 7 pt as the ordinary body ceiling.
- Keep keylines at least 0.3 pt and primary dividers between 0.8 and 1.5 pt.
- Derive height from the scientific content and the venue's caption allowance.

## Palette

The bundled palette uses dark ink, pale semantic fills, and five restrained accents.
Keep text darker than graphical marks. Reserve coral for failure, exclusion, or caution.

Colour never carries a category alone:

- lines use marker shape and line style;
- points use marker shape;
- bars and filled regions use edge treatment, hatch, or direct labels;
- arrows use solid versus dashed style plus a label or other semantic cue.

For microscopy, multiplexed imaging, spatial maps, and other channel-based measurement
images, use a local channel key, direct channel labels, or separately shown
single-channel views. Do not add synthetic hatches or markers to the measured field to
imitate chart redundancy. Any region or object annotation remains source anchored.

Use lightness as an ordered channel only for ordered quantities. Do not reuse a pale
sequential step as an unrelated nominal category.

## Layout

- Use alignment, proximity, and thin dividers before containers.
- A filled region must encode a compartment, cohort, branch, or decision state.
- Keep labels adjacent to the object they name.
- Put definitions, caveats, secondary metrics, and interpretive prose in the caption.
- Keep data plots, microscopy, structures, and quantitative annotations derived from
  their actual source artifacts.

## Assets

Native vector primitives are the default for final scientific schematics. A conceptual bitmap
must contain one object or tightly coupled concept, no embedded text, and no implication
that it is measured evidence. Check the target venue's current AI and third-party rights
policies before using generated or external assets.

These embedded-asset constraints do not apply to a complete image concept used only
as a design reference for native reconstruction. Follow the default schematic route in
[image concept to editable vector](../../../references/image-concept-to-vector.md)
for that route; the generated reference is not the final editable artifact.

## Version and review

Preserve the last accepted version. Compare old and new renders at the same physical
width, then inspect label size, clipping, overlap, arrow attachment, whitespace, colour
redundancy, and scientific fidelity. Automated checks do not replace looking at the
rendered page.
