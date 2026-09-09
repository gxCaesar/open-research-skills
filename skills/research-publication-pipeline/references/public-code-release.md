# Public code release

Use this reference to prepare a local public artifact. It does not authorize repository
creation, upload, publication, or announcement.

## Build from an allowlist

Create a dedicated `public-release/` tree and copy only files a new user needs:

- useful source code and public configuration;
- pinned dependency versions and supported environment instructions;
- one small synthetic or redistributable example;
- data acquisition and preprocessing instructions;
- exact runnable training or analysis and evaluation commands;
- expected outputs and interpretation;
- focused tests;
- licence, citation, contribution notes, and honest limitations.

Do not export the research workspace or experiment parent. Exclude credentials, private
or restricted data, real user identifiers, machine-specific paths, editor or reviewer
material, unpublished evidence, hidden prompts, agent instructions, approval records,
execution traces, pipeline state, and internal provenance records. Rely on the hosting
service for service-managed integrity metadata rather than adding author-created side
records to the public artifact.

## Inspect content and permissions

Scan filenames and readable text for secrets, identities, private paths, internal
workflow terms, stale repository URLs, and accidental large artifacts. Confirm licence
compatibility for every bundled dependency, model, dataset fragment, template, image,
and third-party file. A citation does not grant redistribution rights.

Review generated examples and expected outputs for scientific overclaiming. A synthetic
fixture must be labelled synthetic and must not be presented as a reproduced result.

The validator checks named private machine-path patterns, inline workflow records in
documentation/configuration, and author-created integrity side records or verification
commands, including readable extensionless files. Ordinary source-code identifiers,
scholarly URLs, and service-managed dependency lock metadata are not such records.
Findings report the file and risk class, not the matched text. Its scope is
`records_and_local_artifact_checks`, not universal privacy protection, policy truth, or
independent reproduction; the human content and permission inspection remains necessary.

## Rehearse as a new user

Package the allowlisted tree, create a fresh unpack in a clean temporary directory, and
follow the public README exactly. Install only the documented dependencies, run the
small example and focused tests, and compare the produced file names, shapes, and
meaning with the documented expected outputs.

Fix the release copy or documentation when the rehearsal needs an undocumented path,
environment variable, file, manual edit, or private context. Rehearse the exact final
candidate again after material changes.

For a small worked example, run the installed skill's
`examples/run_demo.py OUTPUT_DIRECTORY --with-public-release`; see
[the synthetic demonstration](../examples/README.md). It actually packages, unpacks,
and executes its bundled example with the current interpreter. It is not a general
runner for commands stored in project records, and the ordinary validator never
executes those commands. A real project's rehearsal still needs its own observed run.

## Report readiness without publishing

Keep the audit record in `handoff/handoff.json.public_release`, outside the curated tree.
The record must contain:

- `allowlist`: every file below the selected `public-release/` path, with no extras;
- `artifact_paths`: non-empty path lists for `source`, `dependency_spec`, `example`,
  `data_instructions`, `run_instructions`, `expected_outputs`, `tests`, `license`,
  `citation`, and `limitations`; their union must classify every allowlisted file, and
  source, dependency, example, tests, licence, citation, and limitations must be
  distinct artifacts whose paths match those roles; use the optional `configuration`
  category for public JSON, YAML, or TOML configuration files rather than labelling
  them as source;
- `rehearsal`: `status: PASS`, an ISO `checked_on` date, the clean environment, and at
  least one exact command with observed exit code zero and non-empty observed outputs;
- `not_run`: an explicit list, including any documented command or environment that was
  not actually exercised.

Do not copy this audit record into the curated public tree. `status: AUDITED` is a summary,
not evidence, and cannot pass without the allowlist, artifact map, and rehearsal record.
Record what was included, which documented commands were run, the clean-environment
limitations, licence or data constraints, and what remains not run.
Local release readiness, remote repository state, tagged release state, manuscript code
statement, and actual public availability are separate facts.
