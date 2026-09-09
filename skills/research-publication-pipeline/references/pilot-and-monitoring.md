# Pilot and monitoring

## Pilot the load-bearing premise

The pilot is the smallest real-data check that can invalidate feasibility or the
central mechanism before expensive development. Freeze its input version, independent
unit, split, comparator, endpoint, direction, uncertainty summary, expected failure
signature, and go or no-go rule before observing the result.

Prefer a vertically complete slice over a large partial build. It should exercise data
loading, preprocessing, model or analysis execution, evaluation, and artifact writing.
Use a tiny synthetic case only for engineering; use a representative real-data subset
for a scientific pilot. A pilot GO supports the tested premise only. It does not prove
novelty, generalization, final headroom, or venue readiness.

Include a retrainability check for any baseline whose reproduction is essential. Record
the exact recipe, resource use, output, deviation from the reported result, and whether
the discrepancy blocks comparison.

## Separate authorization from preparation

Prepare configuration, output locations, logging, termination criteria, resource
estimates, and recovery steps locally. Remote mutation, paid services, locked-test
access, and compute launches remain separate authorization boundaries. A prepared run
is `not_run` until execution evidence exists.

## Monitor evidence, not process existence

After an authorized launch, monitor the intended output directory, terminal log, exit
status, finite early metrics or loss, resource anomalies, and expected completion
artifact. A running shell, session name, stale completion marker, or service dashboard
does not prove that the intended run started or finished.

Normal progress does not require repeated scientific decisions. Resume analysis only
when the run completes, a registered intermediate decision point is reached, or an
anomaly appears.

Stop and preserve evidence on:

- non-finite loss, gradient or numerical explosion;
- impossible metrics or unexpected leakage-like performance;
- split, label, scorer, baseline, or protocol mismatch;
- missing, overwritten, or inconsistent output artifacts;
- deviation from the authorized command or frozen configuration.

Do not silently retry a scientific anomaly. Engineering failures may be repaired only
when the frozen scientific contract remains unchanged; record the failed attempt and
the repair.

## Completion report

Report the observed command or run identifier, environment and configuration, exact
output paths, exit status, registered metrics, uncertainty unit, failed or not-run work,
and any inference. Completion of a job is not the same as passage of its scientific
decision rule.
