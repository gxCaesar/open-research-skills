# Proteomics, metabolomics and glycan visualization recipes

Use for molecular feature tables, spectra, glycoforms and pathway summaries. Select
the identification level before the display: an attractive symbol cannot upgrade an
uncertain feature into a confirmed molecular structure.

## Input contracts

| Modality | Required plotting fields | Keep separate |
|---|---|---|
| Proteomics | `sample_id, donor_id, condition, protein_group, peptide_or_precursor_id, abundance, detected, normalization` | Peptide support, protein groups and unambiguous protein IDs; technical injections versus biological units |
| Metabolomics/lipidomics | `sample_id, feature_id, mz, retention_time, polarity, adduct, abundance, detected, annotation, identification_status` | Measured feature versus assigned molecule; isomers; relative signal versus calibrated concentration |
| MS/MS | `spectrum_id, precursor_mz, charge, collision_energy, product_mz, intensity, assignment_status` | Experimental versus library/predicted peaks; independently normalized versus absolute intensity |
| Glycomics/glycoproteomics | `sample_id, feature_id, protein, site, composition, structure_status, abundance, denominator` | Composition versus linkage/topology; glycopeptide abundance versus site occupancy |
| Pathway result | `term_id, term_label, estimate, interval_low, interval_high, tested_universe, measured_members` | Directional abundance evidence versus set enrichment and its background |

Export analysis-defined estimates and exclusions rather than recomputing a new test
for a nicer panel. Preserve missing, below detection, excluded and measured zero as
different states. Feature counts, identified molecule counts and unique proteins are
different denominators.

## Build the comparison

**Coverage before abundance.** Put a sample-by-feature detection matrix beside the
effect plot. Use blank plus a local label for unmeasured values; do not colour them as
zero fold change. Show how many complete biological pairs support each estimate.
When imputation was part of the approved analysis, show its label and sensitivity;
do not invent imputed values during drawing.

**Full names deserve width.** For a lipid/pathway/glycopeptide effect plot, allocate
approximately half the panel to labels if the actual measured glyph widths need it.
Wrap at chemical or phrase boundaries, keep site/residue identity intact, and align
effects and intervals in the remaining plotting rectangle. Short IDs can join to a
full-name table; unexplained abbreviations should not replace the molecular identity.

**Spectra need source context.** Use a stick spectrum with m/z coordinates and a stated
intensity normalization. For an observed/reference mirror view, retain separate labels,
matching tolerance and unmatched peaks. Only label fragment assignments actually
supported by the source. A few pretty peaks do not establish an identification.

**Glycan identity has constrained symbols.** The
[SNFG reference](https://www.ncbi.nlm.nih.gov/glycans/snfg.html) specifies chemical
meanings for colour/shape pairs and provides vector symbols (opened 2026-09-09).
Do not recolour them to a house palette. Add textual identities for accessibility.
If only composition is known, show the composition or a composition-level glyph;
do not draw an unsupported linkage or branching topology. A fractional glycoform
change is not absolute production, and an abundance ratio is not site occupancy
without the appropriate measured denominator.

## Plotting recipe

```python
# Feature effects and intervals already use the approved biological unit and model.
for row, effect in enumerate(effects):
    ax.errorbar(effect.estimate, row,
                xerr=[[effect.estimate - effect.low], [effect.high - effect.estimate]],
                fmt="o", capsize=2)
ax.axvline(0, color="0.6", linestyle=":")
ax.set_yticks(range(len(effects)), [effect.full_label for effect in effects])
# Annotate complete-pair n for each row, including features lost to missingness.
```

Use comparable scales only for the same normalization and measurement. A shared
within-feature z-score map compares patterns, not abundance across metabolites.
Different ionization responses do not become comparable concentrations by sharing a
colourbar. Relative compositions should state the total and retain per-sample
variation, not just a mean stacked bar.

The [synthetic example](../examples/multimodal-18-panel/README.md), panels h–k,
combines detection, complete-pair effect intervals, fractional values and a stick
spectrum. It deliberately makes no metabolite identification or glycan-structure claim.
