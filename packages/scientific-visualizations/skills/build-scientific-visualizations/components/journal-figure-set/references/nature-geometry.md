# Dated Nature-family geometry profiles

Checked 2026-09-05. Confirm the current instructions for the exact journal, article type,
submission stage, and production request. The bundled records are engineering snapshots;
editorial or production instructions override them.

## Why one Nature width is not sufficient

Current first-party sources differ by workflow stage:

| Profile scope | Single or intermediate width | Double or full width | Height rule |
|---|---:|---:|---|
| Nature Research Figure Guide, figure preparation | 89 mm | 183 mm | maximum 170 mm |
| Nature initial submission | 90 mm | 180 mm | maximum 170 mm |
| Nature Research journals, final artwork | 88 mm | 180 mm | caption-length bands |
| Nature Protocols, final artwork | 135 mm | 180 mm | caption-length bands |

Sources:

- [Nature Research Figure Guide: Building and exporting figure panels](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)
- [Nature: Initial submission](https://www.nature.com/nature/for-authors/initial-submission)
- [Nature Research journals: Guide to preparing final artwork](https://www.nature.com/documents/NRJs-guide-to-preparing-final-artwork.pdf)
- [Nature Protocols: Guide to preparing final artwork](https://www.nature.com/documents/nprot-guide-to-preparing-final-artwork.pdf)

Do not average these values or select the most convenient width. Put the applicable
source and stage in `venue_contract.json`.

## Nature Research final-artwork height bands

| Caption length | 88 mm width | 180 mm width |
|---|---:|---:|
| fewer than 50 words | 220 mm | 225 mm |
| 50--149 words | 180 mm | 210 mm |
| 150--299 words | 130 mm | 185 mm |

The bundled profiles are `nature-research-final-artwork-2026-09-single` and
`nature-research-final-artwork-2026-09-double`.

## Nature Protocols final-artwork height bands

| Caption length | 135 mm width | 180 mm width |
|---|---:|---:|
| fewer than 50 words | 222 mm | 222 mm |
| 50--149 words | 210 mm | 214 mm |
| 150--299 words | 199 mm | 205 mm |

The bundled profiles are `nature-protocols-final-artwork-2026-09-single` and
`nature-protocols-final-artwork-2026-09-full`.

## Profile and validator behavior

`assets/venue-profiles.json` is the executable authority snapshot. Every verified
record names the journal, article type, stage, authority title and URL, checked date,
applicable scope, selected width, and available height rule. `figure_spec.json` stores
the selected width as a derived rendering value.

`validate_journal_pdf.py` reads the actual one-page PDF geometry and accepts either a
dated `--profile` or a project `--venue-contract`. Caption-dependent profiles require
the exact delivered caption. The validator removes common LaTeX references, citation
commands, commands, and inline mathematics before counting words. It uses a 0.2 mm
engineering tolerance.

Legacy aliases such as `nature-double` and `nature-research-double` remain readable for
old commands but emit an unverified warning. They do not establish final
journal-submission authority. A local PASS confirms consistency with the selected
snapshot; it is not a publisher acceptance certificate.
