# Project Manifest specification

Schema: [`schemas/project-manifest.schema.json`](../../schemas/project-manifest.schema.json)

Validate with:

```bash
python tools/validate.py path/to/manifest.yaml
```

## Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `vsc_version` | string | yes | Manifest format version, e.g. `0.1.0`. |
| `project.type` | string | yes | A `project-packs/` id. |
| `project.title` | string | no | Free text, max 200 chars. |
| `project.language` | string | no | BCP-47 tag for the **deliverable**. Defaults to the composer UI language. |
| `project.audience` | string | no | Who the work is for. |
| `project.notes` | string | no | Anything the executor should know. |
| `skills[]` | string[] | yes | Ids from `registry/skills.json`. Unique, at least one. |
| `visual.style` | string | no | A `style-packs/` id. |
| `visual.overrides` | object | no | Token-level overrides applied on top of the style pack. |
| `brand.source` | enum | no | `none`, `local`, `figma`, `github`, `upload`. |
| `brand.ref` | string | no | Path, repo slug, or file key. **Never a secret.** |
| `quality.pack` | string | no | A `qa-packs/` id. |
| `quality.vision_judge` | bool | no | Render and score the output. |
| `quality.text_check` | bool | no | Overflow, orphans, CJK breaking, typos. |
| `quality.brand_check` | bool | no | Tokens resolve back to the brand pack. |
| `quality.auto_repair` | bool | no | Re-render until the threshold clears. |
| `quality.threshold` | int 0-100 | no | Pass mark for the QA score. |
| `quality.max_repair_rounds` | int 0-10 | no | Repair attempt ceiling. |
| `runtime.target` | enum | no | `vad`, `claude-code`, `codex`, `gemini-cli`, `generic`. |
| `runtime.created` | date string | no | `YYYY-MM-DD`. Quote it in YAML. |

`additionalProperties` is `false` at every level: an unknown key is an error, not a
silently ignored hint.

## Executor contract

VAD implements this contract. A manifest is compiled onto a Standard VAC Five-Pack card
and executed from there:

```bash
git clone https://github.com/draiagent/Visual-Agent-Design.git
cd Visual-Agent-Design
python tools/vac_runner.py vsc <manifest> --packs ../visual-skill-composer
```

`--packs` points the adapter at this repo so it can resolve the style pack's `avoid`
list. Without it the card still compiles, but carries an explicit unresolved-style
constraint. Only the five project types with a Standard VAC compile today
(`academic-presentation`, `website`, `video`, `dashboard`, `report`); the rest are
refused rather than guessed. See
[VSC-INTERFACE.md](https://github.com/draiagent/Visual-Agent-Design/blob/main/docs/VSC-INTERFACE.md).

Any executor that claims VSC support must:

1. Reject any manifest that fails schema validation.
2. Honour the style pack's `avoid` list, not just its tokens.
3. Resolve `brand.ref` itself, from its own credentials. The manifest never carries them.
4. Run every `quality.*` flag set to `true`, and report the score it reached.
5. Stop at `max_repair_rounds` and say so, rather than looping.
