# Authoring packs

Every pack is a small YAML file. Adding one is a pull request, not a code change.

## A new skill

1. Add an entry to `registry/skills.json`: `id` (English kebab-case), `category`,
   bilingual `label`, bilingual `summary`, `outputs`, and `requires`.
2. Add a contract entry to `CONTRACT` in `tools/gen_skill_docs.py` — inputs and the
   quality bar in both languages.
3. Run `python tools/gen_skill_docs.py` to regenerate `skills/<id>.md`.
4. Reference the skill from at least one project pack, or it will never be recommended.

## A new project pack

Create `project-packs/<id>.yaml`:

```yaml
id: my-pack
label:   { en: "...", zh-TW: "..." }
icon: "📦"
summary: { en: "...", zh-TW: "..." }
recommended_skills: [ ... ]   # pre-selected
suggested_skills:   [ ... ]   # offered with a reason
default_style: minimal
default_qa: standard
```

Keep `recommended_skills` tight. A pack that recommends everything recommends nothing.

## A new style pack

Create `style-packs/<id>.yaml` with `principles`, `tokens`, and — the part people skip —
an `avoid` list. The avoid list is what makes the style enforceable by `vision-judge`.

## Rules

- Ids: English kebab-case, everywhere, always.
- Labels and summaries: both `en` and `zh-TW`. A missing `zh-TW` falls back to English,
  which is a bug, not a feature.
- Never commit a token, key, or credential. Brand packs carry references only.
- After any registry change, run both checks before opening the PR:

```bash
python tools/validate.py
python tools/check_consistency.py
```

`check_consistency.py` catches unreachable skills, unmet prerequisites, style packs with
no `avoid` list, broken doc links, and — the one that bites — ids that exist in a pack but
were never added to the UI's embedded copy of the same data.
