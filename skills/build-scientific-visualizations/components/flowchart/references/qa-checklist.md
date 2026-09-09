# Flowchart QA checklist

## Scientific

- Compare every stage, arrow, symbol, label, and number with the ledger and source.
- Keep observed, predicted, prospective, training-only, and schematic content distinct.
- Confirm each arrow direction and causal implication is supported.

## Layout

- Render at the final physical width and inspect the complete page.
- Check text size, clipping, overlap, whitespace, formulas, arrowheads, and crossings.
- Verify that the reading path works without relying on colour.
- Compare the previous and revised versions at identical width.

## Files

- Confirm one-page PDF geometry with `pdfinfo` or the package validator.
- Confirm fonts are embedded with `pdffonts`.
- Confirm schematic line art remains vector and source bitmaps retain adequate native
  resolution.
- Extract visible text to catch missing labels, then use the render for layout review.

## Delivery

- Keep the prior accepted file unchanged.
- Include the scene specification, semantic flowchart specification, content ledger,
  editable source, vector PDF/SVG, and QA note.
- Exclude scratch renders and internal drafting records from public handoffs.
