# Publication project workspace

This workspace separates scientific decisions that are often blurred together.

1. Register sources in `evidence/source-register.json`.
2. Complete feasibility, lane-specific prior-art, venue fit, and the falsifiable hypothesis in
   `intake/intake.json`.
3. Freeze the benchmark and development rules in `protocol/protocol.json` before controlled
   iteration.
4. Measure practical headroom in `development/headroom.json` before adding complexity.
5. Register causal candidates and every development cycle in
   `development/iteration-ledger.json`. Keep the locked test sealed.
6. Lock result claims in `claims/claim-register.json` and record the terminal route in
   `handoff/handoff.json`.
7. Put only reviewer- or public-facing materials in `public-release/`.

Run the validator at the next intended boundary:

```bash
python3 /path/to/research-publication-pipeline/scripts/validate_publication_project.py \
  /path/to/this/project --target working
```

Change `working` to `pilot`, `development`, `handoff`, or `public-release` when checking that
boundary. A passing validator confirms the recorded contract, not scientific truth, compute
authorization, venue acceptance, or permission to publish.
