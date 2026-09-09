# Genomic, structural and clinical panel handoffs

Use the relevant section only. These recipes consume an existing scientific analysis;
they do not authorize new causal, binding or clinical-utility claims.

## Genomic tracks and regulation

Input: `genome_build, chromosome, start, end, coordinate_convention, strand,
sample_id, donor_id, condition, assay, normalization, value` plus exact variant alleles
or feature annotations when shown. BED coordinates need an explicit conversion when
combined with another format. The [bedtools format documentation](https://bedtools.readthedocs.io/en/latest/content/general-usage.html)
defines BED start/end semantics (opened 2026-09-09); never join tracks by displayed
chromosome labels alone.

Place aligned condition tracks over the same interval with one coordinate axis.
Match y limits only for comparable assays/normalization. Draw gene direction and variant
position from source coordinates. Put donor/replicate effects or a distance-stratified
contact summary beside the locus, not an unrelated genome-wide decoration. If a contact
matrix is rescaled per sample, label this and do not infer intensity differences from
the colours. A motif logo or attribution track is computational support, not proof of
regulation. Preserve background, tested feature universe and uncertainty from the analysis.

Useful primitives: `ax.step` or `fill_between` for a binned track, `pcolormesh` for
contact bins, and source-coordinate arrows for transcript direction. Do not smooth
away a narrow peak or drop an inconvenient neighboring locus to improve appearance.

## Protein, molecule and structural evidence

Input: exact PDB/mmCIF/SDF or equivalent coordinates; `model_id, chain_id,
residue_id, insertion_code, ligand_id, source_status` and the camera/selection commands.
Preserve experimental versus predicted status, numbering and confidence/resolution.
For a contact view, supply atom/residue pairs, distance rule and source-calculated
distances. For an assay companion, supply compound/variant identity, concentration,
unit, biological/technical replicate map and censored-value handling.

Use a structure overview with a bounded local view, then an independently sourced
functional panel. Keep camera direction and residue colouring consistent across matched
structures. Render geometry with domain software; never reconstruct coordinates from
an image or use generated molecular-looking illustrations as evidence. Preserve the
domain-software scene or commands. A rendered 3D structure may be a legitimate high-
resolution raster layer inside a vector composite; retain vector labels and report the
mixed export honestly. Docking contacts do not become measured affinity.

## Clinical cohorts, calibration and survival

Input: opaque `participant_id, site, split, inclusion, exclusion_reason` plus
`time_origin, followup_time, event` for survival or `prediction, outcome, horizon`
for calibration. Keep repeated visits and sites linked to the participant. The
scientific source defines censoring, competing events, estimators and intervals.

For a dense translational group, reserve a shallow participant-flow panel, a wider
outcome panel and a neighboring calibration/external-cohort panel. All denominators
must reconcile. A survival plot includes censoring/interval definitions and an at-risk
table aligned to its actual x ticks. In a supported lifelines environment,
`add_at_risk_counts` is provided for fitted curves in the
[official plotting API](https://lifelines.readthedocs.io/en/latest/lifelines.plotting.html)
(opened 2026-09-09); verify whether the requested counts refer to the start or end of
each interval. Do not type a risk table from memory.

For calibration, show predicted probability against observed frequency, the identity
line and bin/smoothing support. State held-out versus recalibrated status and the
time horizon. An AUC panel does not replace calibration; a decision curve additionally
needs stated clinical utility assumptions. Put prespecified subgroup effects and
interaction estimates in a forest display with visible n, retaining unfavorable sites.

Patient-level data need not be public to make a figure reproducible: share approved
aggregate plotting tables or a controlled-access route. The renderer must not export
patient identifiers, private file paths or unauthorized clinical images.
