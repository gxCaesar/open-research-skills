# Archived synthetic demonstration

This example is a fictional, self-contained final-record-completeness demonstration. It is not a
current NSFC policy check, applicant approval, scientific finding, eligibility decision, or
funding assessment.

From the installed `writing-funding-proposals` skill directory, create a new output
directory outside that directory:

```bash
python3 examples/run_demo.py /tmp/funding-synthetic-demo
```

The script initializes the workspace, writes meaningful synthetic labels and evidence records,
then invokes the existing final-mode record-completeness check with the fixed archived
`--as-of 2024-02-29` snapshot. It prints the observed status and scope, and exits nonzero if
initialization or the final-mode check does not succeed. It refuses an existing output directory
and any output path inside the installed skill directory.

The output contains only synthetic fixtures. Its validator report uses
`validation_scope: record_completeness`: it demonstrates the local record contract, not file
format, rendering, visual quality, or manual verification of real sources or evidence. Do not
publish it, submit it, or present it as real applicant, policy, scientific, or funding evidence.
