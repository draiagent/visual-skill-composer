---
name: visual-skill-composer
description: >
  Compose a Project Skill Pack for a visual deliverable — presentation, website, video,
  dashboard, infographic card, report, comic, brand kit, or social post. Use when a user
  is starting a new visual/content project and needs to decide which AI skills, visual
  style, brand system, and quality checks apply, or when they ask for a VSC manifest.
  Emits a manifest validated against schemas/project-manifest.schema.json for VAD or any
  agent runtime to execute. Bilingual: ids are English, labels are zh-TW / en.
---

# Visual Skill Composer

## What this skill does

Turns a vague request ("make me a course deck") into an explicit, validated Project
Manifest: project type, skill list, visual style, brand source, and quality thresholds.

It **composes**. It does not render, generate, or publish — that is the executor's job.

## Procedure

1. **Identify the project type.** Match the request to one file in `project-packs/`.
   If nothing matches, ask; do not invent a pack id.
2. **Seed the skills** from that pack's `recommended_skills`. Offer `suggested_skills`
   as additions and say why each one helps this specific project.
3. **Resolve dependencies.** Every skill in `registry/skills.json` has a `requires` list.
   `brand-check` requires `brand-system`; `auto-repair` requires `vision-judge`.
   Add missing prerequisites, or drop the dependent skill — never emit a broken set.
4. **Pick a style pack** from `style-packs/`. Default to the project pack's
   `default_style` unless the user states otherwise. Honour the pack's `avoid` list.
5. **Pick a brand source** from `brand-packs/`. Record a reference only.
   Never write a token, key, or credential into the manifest.
6. **Pick a QA pack** from `qa-packs/`. Default to the project pack's `default_qa`.
7. **Emit the manifest** as YAML (default) or JSON, then validate:
   `python tools/validate.py <file>`
8. **Hand off.** State which runtime should execute it (`runtime.target`, default `vad`).

## Rules

- Skill ids are English kebab-case, always. Never localise an id, not even in a
  zh-TW conversation. Localise labels only.
- `project.language` is the language of the **deliverable**, not of the conversation.
  Ask if it is ambiguous.
- Do not add a skill the user did not choose and was not recommended by the project pack.
  Suggest it in prose instead.
- If the user asks VSC to actually build the deliverable, say plainly that VSC composes
  and VAD executes, then offer to hand the manifest over.

## Files

| Path | Role |
|---|---|
| `registry/skills.json` | Every skill: id, category, bilingual label, requires |
| `project-packs/*.yaml` | Deliverable types and their recommended skill sets |
| `style-packs/*.yaml` | Visual token sets and anti-patterns |
| `brand-packs/*.yaml` | Brand source references |
| `qa-packs/*.yaml` | Check sets, thresholds, repair rounds |
| `schemas/project-manifest.schema.json` | The output contract |
| `ui/index.html` | Human-facing composer, same data, zero build |
