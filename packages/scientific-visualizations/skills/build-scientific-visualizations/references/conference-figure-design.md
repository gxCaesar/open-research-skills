# Conference figures that explain the method

Use for a conference method schematic or coordinated figure set. Select the scientific
job before choosing boxes or panel count. This guide adds design judgment to the shared
construction workflow; it is not a separate renderer, venue rule or fixed template.

New or redesigned motivation, method and architecture schematics use the default
[image concept to editable PPTX route](image-concept-to-vector.md), including panels
inside a coordinated set. Generate the selected conference style before native
reconstruction. A data-bearing motivation or results panel still comes from real data.

## Choose what the reader needs to distinguish

- Task or motivation: show the actual missing capability or ambiguous setting. Do not
  fabricate a motivating distribution, failure example or performance gap.
- Method: show the operation that makes this method different. Use a graphical model
  for conditional dependencies, a computation graph for transformations, or a process
  diagram for chronological stages. Name that meaning in the caption.
- Comparison: use aligned views when the difference from a baseline is itself the
  explanation. Shared inputs and outputs should remain visibly comparable.
- Results: choose views for the actual comparison, tradeoff, ablation or failure
  boundary. A compact overview must not average away the setting that reverses a claim.

These jobs may share one figure or require different figures. Do not manufacture a
motivation–framework–results trio when one job is unsupported or redundant.

## Make method semantics visible

Keep the source's observed inputs, latent quantities, learned parameters and predictions
distinct. Label fitted or estimated structure as such; a schematic edge is not empirical
proof of a biological mechanism. Show the novel operation at a readable scale instead
of giving every boilerplate component equal visual weight.

When training and inference are both shown, identify what is fitted, what is frozen,
which information is unavailable at inference, and whether arrows mean data flow,
conditioning or optimization. Use labels and the shared arrow-role conventions. Do not
add an inference lane to a generative dependency diagram just to satisfy a layout habit.
Do not use a left-to-right arrangement to imply a causal or temporal order absent from
the source. Keep necessary equations native/editable and tied to their exact source.

## Inspected design cases

Checked 2026-09-09; actual figures and captions inspected, `FETCH_VERIFIED: true`.
These are observations about older papers, not current venue requirements or artwork
to copy. Printed page numbers are used. No third-party images are bundled.

- [GIM, ICML 2025, Figure 1, p. 5](https://raw.githubusercontent.com/mlresearch/v267/main/assets/schneider25a/schneider25a.pdf):
  observed perturbation features, latent atomic interventions and system response have
  separate identities; shared parameters sit outside the environment plate. The arrows
  encode generative dependencies, not training chronology. Figures 2–3, pp. 7–8,
  separate identification and predictive comparisons. Borrow the distinctions, not
  biological certainty from a learned graph.
- [DPO, NeurIPS 2023, Figures 1–2, pp. 2 and 7](https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf):
  aligned RLHF/DPO views expose the removed training stages. This is a training
  comparison, not a claim that deployment needs no sampling. The reward–KL frontier
  and temperature-dependent win rates answer different questions. Borrow aligned
  contrast and explicit axis meaning, not decorative colours or a generic speed claim.

## Fit the actual manuscript

Resolve insertion width from the manuscript and current venue authority; there is no
universal conference width or minimum type size in this guide. Allocate space to the
meaningful transformation first. Shorten redundant copy or change layout before
shrinking labels. Move secondary detail only if the main figure remains interpretable.

Inspect the standalone vector at the intended physical width, then the actual compiled
manuscript page with caption. Check effective label size after insertion, clipping,
arrow attachment, notation, line-style decoding and whether the figure can be read
without hunting through the appendix. A legible full-screen SVG may fail after TeX
scaling. If no manuscript is supplied, use a clearly labelled insertion-size preview
and report that the compiled-page check was not run; do not invent a compilation.

Read the caption against visible objects: define unusual symbols and arrow meanings,
say what the diagram represents, and keep observations separate from predictions.
Quantitative legends also need the comparison, units and uncertainty actually plotted.
Construction QA cannot validate an unsupported manuscript claim; return that issue to
the manuscript owner without changing the experiment.
