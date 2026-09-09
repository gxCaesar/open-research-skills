# Task-local venue-profile fields

The template is intentionally incomplete. Replace its placeholders with dated, opened
official facts before using it for a compliance conclusion. A generic profile is a
task-local fill-in aid, never current venue authority.

| Field | Required meaning |
|---|---|
| `venue`, `year`, `track`, `checked_on` | The exact scoped venue, year, track, and date its authority was checked |
| `rule_sources` | Non-empty source-ID lists for every official-rule finding that the configured TeX or PDF audit can emit; manuscript-fact findings such as `LAYOUT_OVERRIDE` need no authority source |
| `allowed_stages` | The closed list of stages supported by this dated profile |
| `tex_contract.document_class`, `style_package` | The official shell and package name, not a remembered convention |
| `tex_contract.style_rule_id` | A neutral or venue-specific finding ID emitted for an invalid style invocation |
| `tex_contract.required_document_class_options` | Optional list of options required on the configured `\\documentclass` at every supported stage |
| `tex_contract.required_options` | Optional stage-to-list map of style-package options required at that stage |
| `tex_contract.forbidden_options` | Optional stage-to-list map of style-package options forbidden at that stage |
| `tex_contract.anonymous_stages` | Review stages that use the configured anonymous-source behavior |
| `tex_contract.anonymous_source_author_mode` | `flag` to inspect configured source commands, or `render_hidden` when source commands are allowed but rendered anonymity still needs manual inspection |
| `tex_contract.anonymous_source_identity_commands` | Optional list of bare TeX control-word names inspected only in `flag` mode, such as `author`, `affiliation`, or a venue-specific identity command |
| `tex_contract.final_copy_command` | Optional bare TeX control-word name that selects final-copy behavior |
| `tex_contract.final_copy_rule_ids` | Required `{ "disabled": "RULE_ID", "enabled": "RULE_ID" }` mapping whenever `final_copy_command` is non-empty |
| `tex_contract.final_copy_required_stages` | Required stage list whenever `final_copy_command` is non-empty; the command is required only in these stages and forbidden in every other allowed stage |
| `tex_contract.required_headings`, `require_abstract` | Mandatory source elements for the selected stage |
| `pdf_contract` | Official page geometry, anonymous metadata stages, and verified page limits |
| `pdf_contract.max_file_size_mb` | Optional stage-to-positive-decimal-MB map; any emitted finding reports only MB values |

Every stage list and stage-keyed map must use only values in `allowed_stages`. Configured
lists contain non-empty strings; configured page limits are positive integers and configured
file-size limits are positive decimal MB values. `anonymous_source_author_mode` accepts only
`flag` and `render_hidden`. A non-empty final-copy command requires both generic rule IDs and
its required-stage list so a venue can retain its own finding names.
Bare TeX control-word names contain letters and `@` only, with no leading backslash or other punctuation.

The auditors are conservative static checks. They do not emulate TeX conditionals, certify
visible anonymity, establish semantic completeness of a required section, infer content versus
reference or appendix boundaries, or inspect submission-portal state. Recheck a completed
profile against current official instructions before any real submission.
