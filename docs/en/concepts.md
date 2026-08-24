# Concepts

## The five layers

VSC asks five questions in a fixed order, because each answer narrows the next.

1. **Project pack** — what you are making. Sets the defaults for every layer below.
2. **Skills** — the capabilities the work needs. Seeded from the project pack, edited by you.
3. **Style pack** — colour, type, radius, and an explicit *avoid* list.
4. **Brand pack** — a reference to whose identity applies. Never the identity itself.
5. **QA pack** — which checks run, the pass threshold, and how many repair rounds are allowed.

Reversing the order does not work. You cannot sensibly choose a QA threshold before you
know whether you are making a dashboard or a comic.

## Packs, not settings

A pack is a small file that carries a defensible opinion. `style-packs/swiss-editorial.yaml`
does not merely list colours — it also lists what that style forbids (gradients, drop
shadows, decorative icons). An executor that honours the avoid list produces work that
looks Swiss. One that ignores it produces work that looks like everything else.

## Recommendation, not automation

A project pack marks skills as `recommended_skills` or `suggested_skills`. Recommended
skills are pre-selected; suggested ones are offered with a reason. Nothing is silently
added, and every selection stays editable. The user always leaves with a set they chose.

## Dependencies

`registry/skills.json` gives each skill a `requires` list. `brand-check` requires
`brand-system`, because you cannot check against a brand you never loaded. `auto-repair`
requires `vision-judge`, because repair needs something to repair against. A composer that
emits a set with unmet dependencies has produced a manifest that cannot run.

## Ids are English, labels are data

Every id is English kebab-case and is never translated. Labels are bilingual fields
resolved at display time. This is what lets a person compose entirely in Traditional
Chinese and still hand the result to a runtime, a CI job, or a collaborator who reads
only English.

## Composition is not execution

VSC produces a manifest and stops. It renders nothing, calls no model, and writes no
asset. Execution belongs to VAD or any other runtime that can read the manifest schema.
Keeping the two apart is what makes the manifest portable across Claude Code, Codex,
Gemini CLI, and CI.
