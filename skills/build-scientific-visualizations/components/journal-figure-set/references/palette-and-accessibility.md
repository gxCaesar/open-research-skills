# Palette and accessibility contract

Use a restrained palette with paper white as the default background and text as the
darkest mark. Assign colour by semantic role, not by figure number, and preserve the
mapping throughout the manuscript.

Colour must not be the only channel for category identity:

- lines use marker shape and line style;
- scatter series use marker shape or direct labels;
- bars, filled areas, box or violin bodies, and pie slices use hatch or direct labels;
- heatmaps use a labelled scale and, when categories rather than quantities are shown,
  boundaries or text labels;
- state and direction use shape, arrow style, or nearby text as well as colour.

Measurement images need a different redundancy contract. For microscopy, multiplexed
imaging, spatial maps, and other channel-based measurement images, pair colour with a
local channel key, direct channel labels, or separately shown single-channel views. Do
not overlay synthetic hatches or markers on the measured field merely to satisfy a chart
rule. Preserve quantitative intensities and mark real regions or objects only when the
source and content ledger authorize those annotations.

Choose all redundant channels at final physical size. Hatches need a visible edge colour
and sufficient spacing after reduction. Test a grayscale rendering and at least a
deuteranopia preview, then inspect rather than relying on a numeric palette score alone.

From the installed skill root, use `shared/figure-core/assets/palette.json` as an optional
neutral starting point.
An established manuscript palette takes precedence when its semantic mapping remains
legible and accessible.
