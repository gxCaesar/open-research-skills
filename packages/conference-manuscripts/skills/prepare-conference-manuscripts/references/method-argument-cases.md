# From contribution to method and experiment

Use this guide when a method paper has sound evidence but its explanation is generic,
fragmented, or hard to connect to the main figures. These are writing choices, not a
mandatory section order, a venue policy, or a new experiment-design gate.

## Make the explanation carry the contribution

Start with the actual distinction the paper earns. At the end of the Introduction,
name what an existing approach cannot do under the stated setting, what changes in the
proposed method, and which evidence tests that change. A list of components or datasets
does not explain why the method should work. Do not force three contributions when one
precise advance is the paper's contribution.

In the Method, introduce the task's inputs, available supervision, desired output and
notation before relying on them. Follow the operation that matters to the claim: what
is transformed, conditioned on, optimized or estimated, and why. Put an equation next
to its explanatory job. Distinguish a model definition from its fitting approximation
and from the procedure used at test time. Use an existing toy example only if it
clarifies that distinction; never invent a successful experimental example.

In Experiments, make each paragraph answer a question rather than enumerate tables.
Identify the comparison and setting, state the observed result, then explain its scope.
Choose the strongest relevant comparison, not merely the easiest baseline to describe.
Separate task performance, mechanism evidence, generalization and cost when the
available evidence measures different things. An ablation changes a named ingredient;
its interpretation cannot outrun that intervention. Preserve mixed rankings and failure
cases. Missing measurements stay missing rather than becoming prose promises.

For revision, read the section without its headings: can a reader recover the question,
method change and decisive comparison? Then check it against the figures. Repair the
specific missing connection, not every paragraph into the same rhetorical template.

## Two inspected conference examples

Checked 2026-09-09. Links below are official proceedings sources; the actual main-paper
pages and named figures were read. `FETCH_VERIFIED: true`. Page numbers are the printed
paper pages. These older examples illustrate argument choices, not current submission
rules or a representative survey. Mathematical proofs and implementation correctness
were not audited.

### GIM — ICML 2025

[Paper record](https://proceedings.mlr.press/v267/schneider25a.html) ·
[Paper PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/schneider25a/schneider25a.pdf)

*Generative Intervention Models for Causal Perturbation Modeling*, Schneider et al.
Introduction, pp. 1–2, connects feature-conditioned prediction to unknown intervention
mechanisms. Sections 3.1–3.3, pp. 3–4, distinguish observed features, latent targets and
parameters, and the causal model; prediction uses a MAP approximation. Sections 5–6,
pp. 6–9, separate synthetic identification from real-data prediction. Figure 2,
p. 7, includes a missed target; Figure 5, p. 9, evaluates held-out dosages, not new
drugs. Borrow the separation of evidence jobs, not an unqualified causal-discovery or
universal-superiority claim. Source reading: main pp. 1–9; no appendix used here.

### DPO — NeurIPS 2023

[Paper record](https://proceedings.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html) ·
[Paper PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf)

*Direct Preference Optimization: Your Language Model is Secretly a Reward Model*,
Rafailov et al. Introduction, p. 2, identifies the optimization simplification.
Section 4, pp. 4–5, makes the policy/reference reparameterization explain the loss.
Section 6, pp. 7–8, separates controlled reward–KL evaluation from GPT-4-judged
task quality. Figure 2, p. 7, therefore supports distinct comparisons, not a measured
wall-clock speedup. Borrow the equation-to-experiment connection, not the claim that
no data generation is ever needed. Source reading: main pp. 1–8; no appendix used here.

## Pair prose with the visual artifact

Route construction to `build-scientific-visualizations` and its conference figure
design reference. Agree on the figure's question and use the same object names and
symbols in prose, diagram and caption. A graphical model need not become a chronological
training pipeline; a training comparison need not pretend to show deployed inference.
Keep essential qualifications in the main text or caption when their omission changes
what the figure appears to prove. Do not move a load-bearing definition to the appendix
merely to make the page look cleaner.
