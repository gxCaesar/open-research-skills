<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/branding/open-research-skills-logo-dark.png" />
  <img src="assets/branding/open-research-skills-logo.png" width="820" alt="Open Research Skills" />
</picture>

# Open Research Skills

### Turn research material into a clear argument, an editable figure, and a reusable result.

[Choose a skill](#choose-a-skill) · [Install](#install) · [The ten skills](#the-ten-skills) · [What this does not do](#what-this-does-not-do) · [Evidence](#evidence)

**English** · [中文（完整版）](README.md)

</div>

An agent skill toolbox for everyday research work. Ten complete skills are maintained in
one repository and every one of them installs and runs on its own. You can start from a
single figure, one Results paragraph, or a research question, without first entering a
whole pipeline.

## Install, two lines

```bash
claude plugin marketplace add gxCaesar/open-research-skills
claude plugin install open-research-skills@open-research-skills
```

Any other runtime: copy the whole `skills/<name>/` directory. See [Install](#install).

## What you get

<div align="center">
<img src="skills/build-scientific-visualizations/examples/advanced-method-diagrams/nature-spatial-mechanism.png" width="49%" alt="Nature-style spatial mechanism diagram" />
<img src="skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.png" width="49%" alt="Conference-style conditioning model architecture" />
</div>

Left: a Nature-style mechanism diagram. Right: a conference-style model architecture.
**Both are native editable PPTX and vector PDF, not a raster screenshot** — labels,
colours and block positions can be edited directly.
[mechanism PPTX](skills/build-scientific-visualizations/examples/advanced-method-diagrams/nature-spatial-mechanism.pptx) ·
[architecture PPTX](skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.pptx) ·
[how to edit them](skills/build-scientific-visualizations/examples/advanced-method-diagrams/README.md)

One real invocation looks like this:

```text
Use build-scientific-visualizations. Draw the method architecture from notes/method.md,
two columns, and export an editable PPTX plus a vector PDF.
```

The tutorials are written around AI and biology — single-cell, perturbation prediction,
spatial multi-omics — and the way they organise material, argue in writing, and hand work
over transfers to other fields. The detailed manuals are in Chinese; this page is the
English entry point to the same ten skills.

<a id="choose-a-skill"></a>

## Choose a skill

| What you are doing now | Skill | Manual |
|---|---|---|
| Make a method, mechanism, or multi-omics result legible | `build-scientific-visualizations` | [中文](docs/scientific-visualizations.md) |
| Draft or revise a conference paper | `prepare-conference-manuscripts` | [中文](docs/conference-manuscripts.md) |
| Organise a journal submission and its revision | `prepare-journal-manuscripts` | [中文](docs/journal-manuscripts.md) |
| Write a research funding proposal | `writing-funding-proposals` | [中文](docs/research-funding-proposals.md) |
| Judge a topic and carry it through experiments to delivery | `research-publication-pipeline` | [中文](docs/research-publication-workflow.md) |
| Decide what to change when the method loses to its baseline | `develop-method-to-sota` | [中文](docs/method-development.md) |
| Decide whether a research direction is still open | `survey-and-audit-novelty` | [中文](docs/survey-and-novelty.md) |
| Have strangers attack your own unsubmitted paper | `run-cold-review-panel` | [中文](docs/cold-review-panel.md) |
| Write a referee report on someone else's submission | `review-others-manuscripts` | [中文](docs/peer-review.md) |
| Build and verify the code and data package a reader downloads | `release-research-artifacts` | [中文](docs/artifact-release.md) |

Pick by what you have to deliver this time. The manuscript skills handle the figures a
paper needs on their own, and the pipeline skill can organise a draft on its own; the
visualization skill offers more design support but is not a required dependency of the
others.

<a id="install"></a>

## Install

### Claude Code, two lines

```bash
claude plugin marketplace add gxCaesar/open-research-skills
claude plugin install open-research-skills@open-research-skills
```

The repository is both the marketplace and the plugin inside it, which is why both
commands name the same thing.

**Calling a skill after a plugin install.** Plugin skills are namespaced, so the form is
`/open-research-skills:<skill-name>` — for example
`/open-research-skills:build-scientific-visualizations`. The prefix is not decoration: it
means a skill of the same name already in your own `$HOME/.claude/skills/` **keeps working and
both load**, so installing this repository never requires renaming or removing yours.
Naming the skill in plain language works too.

### Any other runtime, copy the directory

Each skill is a self-contained directory. Copy the whole `skills/<name>/` — not just its
`SKILL.md`, and without nesting it inside another directory of the same name.

```bash
RESEARCH_PROJECT="$PWD/../research-demo"
SKILL_NAME=build-scientific-visualizations
SKILL_DEST="$RESEARCH_PROJECT/.agents/skills"     # Codex
# SKILL_DEST="$RESEARCH_PROJECT/.claude/skills"   # Claude Code
mkdir -p "$SKILL_DEST"
cp -R "skills/$SKILL_NAME" "$SKILL_DEST/"
test -f "$SKILL_DEST/$SKILL_NAME/SKILL.md"
```

`.agents/skills/` is read by **both Codex and Gemini CLI**, so one copy serves both.

| Scope | Codex / Gemini CLI | Claude Code |
|---|---|---|
| One project | `.agents/skills/` in the project | `.claude/skills/` in the project |
| Every local project | `$HOME/.agents/skills/` | `$HOME/.claude/skills/` |

### Installing and updating, per runtime

| Runtime | Install | Update |
|---|---|---|
| **Claude Code** (plugin, recommended) | the two commands above | `claude plugin marketplace update open-research-skills`, then `claude plugin update open-research-skills@open-research-skills` (restart to apply) |
| **Claude Code** (one or two skills only) | copy into `.claude/skills/` or `$HOME/.claude/skills/` | `git pull`, copy again |
| **Codex** | copy into `.agents/skills/` or `$HOME/.agents/skills/` | `git pull`, copy again |
| **Gemini CLI** | the same `.agents/skills/` (its own alias; `.gemini/skills/` also works), or `gemini skills install https://github.com/gxCaesar/open-research-skills` | install again; `/skills reload` in session, `/skills list` to see what loaded |
| **Any other runtime**, including harnesses driven by DeepSeek or another model | every skill is a self-contained directory: copy `skills/<name>/` to wherever that harness reads skills or project context. One that supports Anthropic-style skills reads `SKILL.md` directly | `git pull`, copy again |

The last row gives no specific command on purpose. Those harnesses load from different
places and this repository has not verified them one by one, and an unverified install
command is worse than none.

Some skills need Python packages; each declares its own in `skills/<name>/requirements.txt`
when it has any. Paths and discovery were checked against the
[Codex](https://developers.openai.com/codex/skills),
[Claude Code](https://code.claude.com/docs/en/skills) and
[Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md)
documentation, and the plugin install, update and namespaced invocation were run against
the published repository rather than read off a page.

<a id="the-ten-skills"></a>

## The ten skills

### build-scientific-visualizations

Organises scientific objects, method relationships, and source data into a figure a
reader can follow: a single mechanism or architecture diagram, one dense compound figure,
or a full main / Extended Data / Supplementary set. Concept diagrams may be composed with
image generation and then rebuilt as native editable vector output; evidence figures must
come from real input data.

> **The default route for a new diagram needs an interface that can generate the concept.**
> That route is *generate a GPT Image 2.5 concept → reconstruct it as a native editable
> PPTX → compare the real render and test editing*, and the generating step has to happen
> somewhere that exposes the model, which in practice means **Codex**. Every other step
> runs anywhere, Claude Code included: locking the scientific content, choosing the style,
> rebuilding as native objects, comparing the render, and checking that text, connectors
> and shapes really are editable. Without that interface the skill states two documented
> alternatives — **supply your own concept image**, or take the **direct vector workflow**
> (`references/image-concept-to-vector.md`). Figures made from data — plots, structures,
> microscopy — never take this route at all; they come from the source data or the
> original images.

```text
Use build-scientific-visualizations. Draw the method architecture from notes/method.md,
two columns, and export an editable PPTX plus a vector PDF.
```

### prepare-conference-manuscripts

AAAI, ICLR, ACL, CVPR, ICML, NeurIPS and ICCV. Drafting from existing material, whole-
paper revision, appendices and supplements, rebuttal, camera-ready, and the local
submission package. Each venue adapter is dated and records where every rule came from;
none of them substitutes for the target venue's current instructions.

```text
Use prepare-conference-manuscripts, targeting ICLR 2027 Main Conference, first submission.
Materials are in paper/ and results/. Do not change any reported number.
```

### prepare-journal-manuscripts

Nature-family article organisation, Methods, Results, Discussion, figure legends,
statistical reporting, data and code availability, cover letters, and revision responses.
Nature, Nature Methods, Nature Biotechnology and Nature Communications do not share one
set of requirements, so the journal, the article type, and the stage have to be named.

```text
Use prepare-journal-manuscripts, revision-response mode. The reviewer comments are in
reviews/, the current manuscript in paper/. Produce clean and marked versions.
```

### writing-funding-proposals

NSFC and provincial funds: the scientific question,
the evidence it needs, the research content, section briefs, the technical route, and a
pre-submission review. Guangdong is the bundled provincial example; other provinces are
adapted from their own current materials.

### research-publication-pipeline

Starting or resuming a real project: topic and survey, data feasibility, novelty, the
baseline and the headroom above it, a pilot, method development, the confirmatory run,
claim locking, and the reproducible release. It is a set of decision boundaries, not a
script that declares research finished when it exits zero.

```text
Use research-publication-pipeline, survey mode, over the papers in papers/.
```

### develop-method-to-sota

For the stretch where the pilot runs and the method still loses. It measures how much is
available to win and the noise floor of your own code before any component is designed,
reads the error by slice instead of as one number, tests one component at a time against
a control that could void it, and requires that stopping names one of three exits.

```text
Use develop-method-to-sota. My method is 1.8 points below the baseline on the dev split
after three hyperparameter sweeps. Run headroom-measure before designing anything.
```

### survey-and-audit-novelty

Turns a direction into a decision. The contribution lane is declared before the search
starts, because the lane decides what a collision means. It audits whether the variables
the hypothesis needs actually co-exist in one obtainable cohort, searches from several
independent framings including one whose job is to scoop the idea, and reports the scoop,
feasibility, and venue-fit verdicts separately so a venue doubt cannot be delivered as a
collision.

### run-cold-review-panel

A hostile read of your own unsubmitted manuscript by reviewers with no project context.
The isolation is proved from a directory listing rather than asserted by the reviewer,
five lenses read for different things, one of them executes the released artifact rather
than reading about it, and the meta review adjudicates rather than averages. It rehearses
objections; it does not predict a decision.

### review-others-manuscripts

Refereeing someone else's confidential submission: the confidentiality position first,
then claims against the evidence offered for them, defects with their consequence, and
requests the authors can actually execute. Its examples are synthetic. Real referee
reports are the authors' unpublished work and are not teaching material, which is also
why this skill carries no individual's reviewing voice.

### release-research-artifacts

The package a reader downloads, verified from outside the workspace that produced it. The
file set is resolved by allowlist rather than by exclusion, the staged tree is scanned for
identity byte by byte, and the project's own tests run inside a fresh unpack. Two modes:
anonymized for double-blind submission, and a named archive with a persistent identifier
for a journal.

```text
Use release-research-artifacts, anonymized-submission mode. Results are frozen at the
commit in notes/. Show me the allowlist before staging anything.
```

<a id="what-this-does-not-do"></a>

## What this does not do

**It does not decide that a result is true.** Every bundled validator checks a record for
completeness and internal consistency. None of them establishes that a number is correct,
that an identifier resolves, that a licence is yours to grant, or that code reproduces
anything. Running it is the only way to learn the last one.

**It does not replace a venue's current instructions.** Every venue adapter, policy note
and reporting rule in this repository is a dated snapshot. Conference and journal
requirements change between cycles. Open the target venue's own page before a real
submission; where an adapter could not verify a rule, it says so instead of inheriting a
plausible one from a sibling venue.

**It does not submit, train, upload, or pay for anything.** The examples generate their
own synthetic data. Nothing here reaches an external service on its own.

**It does not carry anyone's writing voice.** The transferable part is the method.

**It does not, on the evidence we have, make an agent's answers more correct.** We ran two
pre-registered before/after evaluations against a control arm, and both were ties on every
primary endpoint. See [Evidence](#evidence).

<a id="evidence"></a>

## Evidence: we measured this twice, and both times it was a tie

**[Full write-up of both cases](docs/evidence.md)** — design, results, defects on both
sides, and the flaws in our own evaluation.

The 447 tests and 197 validator rules in this repository show that the *validators* work.
They say nothing about whether using these skills produces better research. That second
claim is checkable, so we checked it, and we are publishing the result even though it does
not support the claim.

Design, both cases: the same task and material given to two agents that could not see each
other, one of them additionally given the skill under test; endpoints frozen before either
arm ran, with both publishable statements written in advance; blind review from a different
model family, with the mapping held outside the reviewer's input. The control arm's null is
*not doing X*, never *doing X badly*.

| | Case 1: package a project so a stranger can reproduce it | Case 2: decide whether a direction has the data |
|---|---|---|
| Primary | **Tie** — both packages reproduced the target figure from an isolated copy, with zero intervention | **Tie** — both arms reported 0 jointly-measured samples out of 7050, both avoided the "both columns are present" trap |
| Blind review | Core question a tie; 4 confirmed defects, all in the arm without the skill | Core question a tie; 6 confirmed defects, split across both arms |

**On these two tasks a capable general agent reached the same correct answer without the
skills.** What the skills demonstrably add is structure — separately recorded verdicts, a
named kill layer, a repair table run before reporting a kill. **In case 2 that structure
was itself filled in wrongly**, which is the sharpest thing either case found: an auditable
shape can hold the wrong content, and is then harder to catch because it looks compliant.

None of this shows that using the skills produces better papers; neither case tested
manuscript quality. It does not generalise from agents to people. Each case is n=1 on
synthetic material.

## Testing and contributing

```bash
python3 -B scripts/run_tests.py
python3 scripts/check_public_content.py .
python3 scripts/check_rule_coverage.py
find skills -type l -print
```

The first command runs the root suite and every per-skill suite in separate processes.
The second scans the tree for machine paths, private account names, internal control
files and other material that must not be published. The third reports which of the
project validator's rules still have a witness that makes them fire, because a rule that
nothing can make fire could stop working without any test noticing. The fourth must print
nothing.

See [CONTRIBUTING.md](CONTRIBUTING.md) for what a change needs before it opens, including
the clean and known-bad fixture pair required of any validator change, and
[MAINTAINERS.md](MAINTAINERS.md) for who reviews what. Tests run locally; this repository
configures no hosted CI.

## Licence

Apache-2.0. See [LICENSE](LICENSE), [NOTICE](NOTICE), and [THIRD_PARTY.md](THIRD_PARTY.md).
