# Synthetic spatial architecture across molecular layers

This original teaching figure contains artificial data only. Twelve simulated donor
identifiers each have control (C) and perturbed (P) conditions, with 720 synthetic
cells per donor-condition. No tissue was imaged, donor recruited or molecular feature
identified. The generator deliberately inserts spatial compartments, variable response
amplitudes and several null or opposing changes. The labels describe simulated roles.

**a–d, spatial context and state profiles.** a, D01/C is selected by identifier, not
effect size. Cell type is redundantly encoded by colour and marker shape. The dashed
ellipse is the generator's radius-0.61 boundary. Coordinate units and scale bars are
synthetic dimensional conventions, not instrument calibration. b, the exact cells
inside the source ROI are enlarged without repositioning. c, the same ROI and cells
coloured by RNA-boundary abundance. d, feature means within each of three states,
centred on the all-cell feature mean and divided by the all-cell feature SD. This
is a descriptive standardized profile, not evidence that arbitrary-unit intensities
from different assays are comparable. The invariant feature remains near neutral;
its tiny between-state differences are not independently stretched to fill the scale.

**e–h, donor-aware molecular and spatial summaries.** e, perturbed-minus-control
changes for each donor and feature, divided by the control donor SD of that feature.
The shared diverging scale is symmetric and includes every displayed value. f/g,
individual paired RNA-boundary and protein-surface assay values; connecting lines
link only the same donor. h, cell RNA values are averaged within each donor-condition
and radial-offset bin, then across donors. Solid blue is control; dashed coral is
perturbed. The offset is the generator's elliptical radial difference multiplied by
500 µm, not the exact Euclidean distance to a measured tissue boundary.

**i–k, complementary views.** i, three synthetic tracks share artificial genomic
coordinates. Each assay's two conditions share its maximum-amplitude normalization;
vertical stacking separates assays and does not compare their absolute intensities.
No assembly, regulatory contact or actual protein-position relationship is claimed.
j, RNA-boundary versus ATAC-boundary changes matched by donor identity. Their
association partly follows directly from the simulation equations, not independent
biological validation. k, state fractions separately computed for each control donor;
short black bars mark donor means. Individual cells are not treated as replicates.

**l–n, specificity and scope.** l, all donor changes for the selected RNA, protein,
lipid and invariant features, standardized as in e, with mean and interval. The
invariant and opposing effects remain visible. m, the mean RNA-boundary change against
2,000 sign-flip draws of the same donor-level differences; the marked line is the
unflipped mean. This illustrative within-pair null is not a significance claim.
n, paired donor mean RNA changes after restricting cells to four declared symmetric
radial-offset widths. The width changes the population summarized, not the cell
coordinates or source values.

Intervals in h/l/n are 2.5th–97.5th percentiles from 2,000 fixed-seed resamples of
the corresponding donor summaries. In l the observed control-SD denominator is held
fixed, so the interval is conditional on that display standardization. This bootstrap
is a demonstration, not a universal statistical-analysis recipe. No cells or donors
are excluded for appearance; the named ROI, bins, conditions and width restrictions
define their respective panels. All displayed estimates are recomputed from the
included CSV files. No P values, significance stars or biological conclusions are reported.
