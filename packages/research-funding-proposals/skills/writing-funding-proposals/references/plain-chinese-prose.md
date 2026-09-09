# Direct Chinese research prose

Use this contract to audit applicant-authored Chinese proposal text. It is not a detector
of authorship and does not replace scientific or policy review.

## Preserve meaning first

- Keep every number, qualifier, comparison boundary, uncertainty, citation scope, and
  applicant-role limit.
- Separate observed results, supported inference, and planned work.
- Remove an unsupported promotional conclusion or turn it into the exact question and
  validation that could establish it.
- Keep the Q/C/V/O/CL/F dependency graph unchanged unless the scientific argument itself
  is being revised.

## Preferred form

- Put the scientific subject and main judgment early.
- Give one sentence one main claim and one paragraph one rhetorical job.
- Organize related work by capability and unresolved boundary, not publication chronology.
- State causal or evidential connections directly. Split independent claims rather than
  stacking them with decorative punctuation.
- Let novelty emerge from the precise gap, competing explanation, and conclusion-changing
  validation rather than adjectives.

Review formulaic transitions such as `首先/其次/最后`, `一方面/另一方面`, and
`第一/第二/第三`. Replace them only when scientific dependencies provide a clearer
transition. Review semicolons, repeated asides, nested colons, and long sentences in
context. Necessary official names and direct quotations are local exceptions.

Treat `全新`, `国际领先`, `国内首创`, `填补空白`, `颠覆性`, `系统性突破`, and
`重大突破` as unsupported until an opened comparison source establishes the exact scope.
The prose linter reports these cues but never supplies the missing evidence.

## Section review

- The title identifies the scientific object and problem without claiming an unestablished
  result.
- The abstract lets an adjacent-area reviewer recover the problem, precise gap, route,
  validation, and bounded significance.
- The rationale opens on the project-specific tension and treats prior work accurately.
- The contents expose scientific dependencies and failure criteria rather than three
  symmetric slogans.
- The foundation maps completed and transferable work to exact contents without turning
  resources into proof of a future result.

Run `scripts/audit_chinese_prose.py`, then inspect each finding. Record whether it was
revised, retained for a stated reason, or found outside proposal prose. A clean surface
report does not establish scientific correctness or compliance.
