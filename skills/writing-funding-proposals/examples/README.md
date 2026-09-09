# Synthetic demonstration: argument records, not an application

This example is a fictional, self-contained final-record-completeness demonstration. It is not a
current NSFC policy check, applicant approval, scientific finding, eligibility decision, or
funding assessment.

For a readable sample, open the [annotated section brief](section-brief-walkthrough.md).
It is a curated teaching document, not an exported workspace or an application written
by the demo. It shows how to connect the scientific question to a fair comparison,
bounded output and applicant writing task without inventing preliminary results.

## Run in five minutes

From the repository root, Python 3.9+ with no third-party packages is sufficient:

```bash
demo_root=$(mktemp -d)
python3 -B skills/writing-funding-proposals/examples/run_demo.py "$demo_root/funding-demo"
```

From the installed `writing-funding-proposals` skill directory, create a new output
directory outside that directory:

```bash
demo_root=$(mktemp -d)
python3 -B examples/run_demo.py "$demo_root/funding-demo"
```

Use the command appropriate to your current directory, not both. These shell examples
use macOS/Linux syntax; another shell can supply a new temporary path instead. The
script requires a non-existing child directory, which is why it does not write directly
into the already-created temporary parent.

The script initializes the workspace, writes meaningful synthetic labels and evidence records,
then invokes the existing final-mode record-completeness check with the fixed archived
`--as-of 2024-02-29` snapshot. It prints the observed status and scope, and exits nonzero if
initialization or the final-mode check does not succeed. It refuses an existing output directory
and any output path inside the installed skill directory.

Expected status lines, excluding the machine-specific output location:

```text
Observed validator status: PASS
Observed validator scope: record_completeness (record-only)
```

## What to inspect locally

| Generated path, relative to the output directory | What it illustrates |
|---|---|
| `START_HERE.md` | Navigation through the local workspace |
| `argument/argument-map.json` | A single synthetic question linked to content, comparison and output |
| `sections/rationale.md` | A one-sentence fixture, not usable proposal prose |
| `evidence/claim-ledger.csv` | The record shape for connecting a claim to its source |
| `commitments/commitment-records.json` | How bounded commitments are represented |
| `delivery/final.pdf` | A placeholder path used by the checker; not a real PDF |

Open the source files in an editor to understand the records. Do not use a PDF viewer
failure as evidence that a real proposal build failed: this demo intentionally does not
run a document renderer. The file contents are synthetic marker text.

## Interpretation and limits

The output contains only synthetic fixtures. Its validator report uses
`validation_scope: record_completeness`: it demonstrates the local record contract, not file
format, rendering, visual quality, or manual verification of real sources or evidence. Do not
publish it, submit it, or present it as real applicant, policy, scientific, or funding evidence.

The fixed historical date and the 2026 program label exercise a software contract; they
do not document a real source-access event. Source URLs and applicant labels are
fictional. In particular, a generated `VERIFIED` label is not independent verification.
No official form, current online policy check, actual applicant approval, full proposal,
AI image, editable PPTX or rendered submission candidate is produced.

To work on a real proposal, initialize a separate project, read the current official
and institutional sources and use the skill's allowed authoring mode. Do not rename
this fixture as your project or replace evidence gathering with its passing statuses.
Keep generated workspaces outside the public checkout; public-content scanning is
intended to reject accidental inclusion of those records.
