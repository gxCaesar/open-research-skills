# Synthetic multi-modal atlas: figure legend

All data are artificial. This original example demonstrates figure construction;
it makes no biological, diagnostic or method-performance claim. D01–D08 identify
eight simulated units with control and perturbed conditions, not recruited donors.
Each donor-condition contains 80 cells, yielding 1,280 cells. Coordinates and their
micrometre labels are synthetic dimensional conventions, not instrument calibration.

**a–d, spatial context and identity.** a, D01 control is selected by identifier, not
signal or quality. The rectangle selects x = 220–520 and y = 100–400 in the artificial
coordinate system. b, the exact same selected cells enlarged, with a synthetic 100 µm
scale bar. No cell is moved to improve the crop. Colours and marker shapes encode
states S1–S3 consistently. c, all cells in directly generated latent coordinates;
this is not UMAP, an inferred trajectory or evidence of successful integration.
d, within-state means of RNA-A/B determine colour and the fraction of cells with
value > 1 determines point area; zeros enter the mean. These are descriptive pooled
cell summaries, not independent-unit effect estimates.

**e–g, paired-unit summaries.** e, separate assay-table RNA values for each donor,
with control and perturbed members connected. These assay summaries are simulated
separately from cellular marker values. f, RNA-A is averaged first within each
donor-condition and each of four equal x bins, then across the eight donors. g,
within-donor assay changes divided by the control donor standard deviation of the
same assay; these are dimensionless standardized changes, not comparable absolute
RNA, ATAC and protein abundances. Grey points show individual standardized changes,
diamonds their means. For f, g, i and q, intervals are 2.5th/97.5th percentiles of
2,000 bootstrap resamples of the respective independent unit summaries, with a fixed
display seed. For g the displayed standardization denominator is held fixed during
the bootstrap. This conditional interval is illustrative, not a universal inferential
recipe. No significance test or corrected discovery list is claimed.

**h–k, molecular evidence.** h, perturbed-sample feature detection for M1–M4; white
means absent measurement, not measured zero. M1 is deliberately missing in D03/D07.
i, differences of simulated log2 abundance, perturbed minus control, for each feature.
Only complete donor pairs contribute: six for M1, eight for M2–M4. All labels retain
the feature class; no exact molecular identity or glycan topology is implied.
j, paired fractions on the full 0–1 scale, with denominator defined by the simulated
total. This is not an occupancy assay. k, artificial m/z sticks with relative
intensity; there is no library match, fragmentation assignment or identification.

**l–o, context and controls.** l, two functions over an artificial 0–1,000 bp locus
on a common amplitude scale, not a real genome assembly or a measured accessibility
track. m, donor-level RNA/ATAC changes, with donor-number labels. n, the mean RNA
change against 2,000 within-pair sign-flip draws; the same paired changes are retained
and only their signs are randomized. o, simulated concentration responses for all
eight units, with a symlog x axis retaining the zero-concentration control. Lines
connect observations within units; no fitted potency or affinity is reported.

**p–r, limitations and linkage.** p, available perturbed donor-level RNA, ATAC and
metabolite measurements: eight, eight and six. q, the same RNA contrast using all
eight paired units versus the six with linked metabolite measurements; missingness
is not imputed. r, observed correlation of paired RNA/ATAC changes against 2,000
draws shuffling the ATAC donor labels. This differs from the within-pair null in n:
it destroys cross-assay pairing while retaining each marginal distribution. Neither
randomization is an empirical scientific conclusion from this artificial dataset.

No fields or units were removed for aesthetic quality. The only complete-pair
exclusions are the declared missing M1 measurements and linked-subset restriction.
Source tables, generation code and rendering code are included with this example.
