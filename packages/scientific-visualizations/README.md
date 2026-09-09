# Scientific Visualizations

This package exposes one public skill: `build-scientific-visualizations`.

Its five internal modes cover progressively larger deliverables:

| Mode | Responsibility |
|---|---|
| `layout-sketch` | Disposable hierarchy and reading-order exploration |
| `flowchart` | One workflow, mechanism, method, or architecture diagram |
| `compound-figure` | One complete multi-panel figure or graphical abstract |
| `conference-figure-set` | A coordinated compact figure set for a conference paper |
| `journal-figure-set` | Main, Extended Data, and Supplementary figures for a journal manuscript |

The exact skill directory keeps non-triggering mode guides under `components/` and one
implementation under `shared/figure-core/` for initialization, schema validation, rendering,
vector composition, PDF geometry checks, visual QA, and clean deliverables.

New or redesigned flowchart, architecture, motivation, method and mechanism schematics
default to GPT Image 2.5 concept generation followed by native editable PPTX
reconstruction in the corresponding conference or journal style. This also applies to
schematic panels within compound figures. See the
[authoring route](skills/build-scientific-visualizations/references/image-concept-to-vector.md)
for model-identity reporting and small-edit exceptions. Quantitative plots
and measured images remain source-derived; PPTX does not replace required PDF/SVG exports.

Schema 1.2 makes page-first design executable. Each final figure has a dated venue contract,
whole-page blueprint and proof, inspectable geometry receipt, matching layout review, per-panel
source-data map, and optional semantic flowchart graph. Detailed panels are drawn only after the
page hierarchy is reviewed at final physical width. Reviewer packaging copies declared
audience-safe data, plotting scripts, source-bound assets, and explicitly authorized rendered
outputs, not an entire working directory or every author composite. Mixed-access reviewer/public
views are restricted to source-bound quantitative PDF/SVG outputs, omit the full proof/composite,
and are scanned for local locators, embedded image objects, and internal metadata before delivery.

## Install and invoke

Copy the independently installable skill directory and register that copied directory with the
agent runtime:

```bash
cp -R packages/scientific-visualizations/skills/build-scientific-visualizations \
  /path/to/skills/build-scientific-visualizations
```

Set `SKILL_DIR` to the copied directory before following command examples:

```bash
SKILL_DIR=/path/to/skills/build-scientific-visualizations
python3 "$SKILL_DIR/shared/figure-core/scripts/init_figure_project.py" --help
```

The shared data/vector renderer uses this two-phase build; these commands alone do not
perform image generation or native PPTX reconstruction:

```bash
python3 "$SKILL_DIR/shared/figure-core/scripts/init_figure_project.py" <project> \
  --figure-id <id> --mode compound-figure \
  --layout-profile nature-figure-guide-2026-09-double
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase layout
# Inspect the proof and complete qa/layout_review.json.
python3 "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" <project> --phase final
```

```text
Use $build-scientific-visualizations in flowchart mode to turn this method description into a
source-grounded vector diagram.
```

```text
Use $build-scientific-visualizations in journal-figure-set mode to coordinate all main, Extended
Data, and Supplementary figures and inspect them at final size.
```

Runtime requirements are Python 3.9 or later, Matplotlib, Pillow, pypdf, and Poppler commands for
conversion and font inspection. NumPy is optional for the deuteranopia preview. The default
schematic route additionally requires an image-generation capability and a compatible
native presentation capability; the Python tools do not provide either. Prefer GPT
Image 2.5 where selectable. A built-in tool without backend identity can still complete
an authorized default-route request, but its model version must be reported as unverified.

The [design library](skills/build-scientific-visualizations/references/design-template-library.md)
provides original native-editable examples. Its
[two diagram styles and six palettes](skills/build-scientific-visualizations/references/diagram-style-profiles.md)
support open, object-led Nature-inspired schematics and structured top-CS-inspired
architectures. New projects can select `--diagram-style` and `--palette`; these are
design presets, not official venue styles or an automatic finished-diagram generator.

Install the tested Python dependencies from the copied skill directory with
`python3 -m pip install -r "$SKILL_DIR/requirements.txt"`. Poppler and the optional NumPy preview
remain system- or environment-level additions and are not installed by that file.

## Test

From the repository root:

```bash
python3 -B -m unittest discover -s packages/scientific-visualizations/tests -p 'test_*.py'
python3 scripts/check_public_content.py .
find packages/scientific-visualizations -type l -print
```

An empty `find` result is expected. Dated geometry profiles are stage-specific engineering
snapshots; current official instructions for the exact journal, article type, and stage take
precedence. Original instructions and code are covered by the repository's Apache-2.0 licence.
