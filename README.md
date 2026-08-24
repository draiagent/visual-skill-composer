**English** | [繁體中文](./README.zh-TW.md)

# Visual Skill Composer (VSC)

**A visual, composable skill system for AI agents.**

Pick what you are making, see which AI capabilities that actually needs, choose a visual
style and a brand system, set how strict quality control should be — and get a
machine-readable **Project Manifest** any agent runtime can execute.

> From *writing prompts to use AI* → *installing skills to use AI* → **composing AI
> capabilities visually**.

---

## Why this exists

Skill marketplaces show you a list. A list does not tell you which skills belong together,
which ones a project is missing, or what the result will look like.

VSC replaces the checkbox list with five decisions a person can actually make by looking:

| Layer | Question | Output |
|---|---|---|
| 1. Project | What are you making? | `project.type` |
| 2. Skills | Which capabilities does it need? | `skills[]` |
| 3. Visual | How should it look? | `visual.style` |
| 4. Brand | Whose identity applies? | `brand.source` |
| 5. Quality | How strict is the check? | `quality.*` |

Each layer narrows the next. Choosing *Course Presentation* pre-selects instructional
design, storytelling, and infographic — and suggests research and Vision Judge on top.

---

## VSC and VAD

These are deliberately **two projects, not one**.

```text
             VSC
     Visual Skill Composer
              |
              |  select / compose
              v
       Project Skill Pack   <-- schemas/project-manifest.schema.json
              |
              v
             VAD
      Visual Agent Design
              |
      +-------+-------+
      v       v       v
    Figma   Assets   Brand
      |
      v
  AI Generation
      |
      v
  Vision Judge
      |
      v
   Auto Repair
```

**VSC decides which tools you take with you. VAD decides how those tools get the job done.**

VSC never executes anything. It composes, validates, and hands off.

---

## Quick start

```bash
git clone https://github.com/draiagent/visual-skill-composer.git
cd visual-skill-composer
python -m http.server 4321 --directory ui
```

Open <http://localhost:4321>, compose a pack, and hit **Build skill pack**.
The UI is a single self-contained HTML file — no build step, no dependencies.

Validate a manifest:

```bash
python tools/validate.py examples/academic-presentation.vsc.yaml
```

---

## What a manifest looks like

```yaml
vsc_version: 0.1.0
project:
  type: academic-presentation
  language: zh-TW
skills:
  - instructional-design
  - storytelling
  - infographic
  - data-visualization
  - research
visual:
  style: swiss-editorial
brand:
  source: figma
quality:
  vision_judge: true
  text_check: true
  brand_check: true
  auto_repair: true
  threshold: 80
```

---

## Bilingual by design

Every id in this repo is **English kebab-case and never localised**. Labels are bilingual
data, resolved at display time.

| Skill ID | 繁體中文 | English |
|---|---|---|
| `presentation-design` | 簡報設計 | Presentation Design |
| `storytelling` | 故事敘事 | Storytelling |
| `data-visualization` | 資料視覺化 | Data Visualization |
| `infographic` | 資訊圖解 | Infographic |
| `instructional-design` | 教學設計 | Instructional Design |
| `research` | 研究分析 | Research |
| `brand-system` | 品牌系統 | Brand System |
| `vision-judge` | 視覺品質評估 | Vision Judge |
| `auto-repair` | 自動修正 | Auto Repair |

This is why GitHub, Claude Code, Codex, and Gemini CLI all read the same manifest
regardless of which language the person composing it was using.

---

## Repository layout

```text
visual-skill-composer/
├── README.md              English (default)
├── README.zh-TW.md        繁體中文
├── SKILL.md               Agent-facing entry point
├── docs/{en,zh-TW}/       Concepts, manifest spec, authoring guide
├── registry/skills.json   Single source of truth for skills
├── skills/                One file per skill contract
├── project-packs/         What you are making
├── style-packs/           How it looks
├── brand-packs/           Whose identity applies
├── qa-packs/              How strictly it is checked
├── schemas/               JSON Schema for the manifest
├── tools/validate.py      Manifest validator
├── ui/index.html          The composer (single file, no build)
└── examples/              Sample manifests
```

---

## Security note

VSC stores **references, never secrets**. A Figma brand pack records a file key and an
environment-variable name; the token itself stays out of version control and is resolved
at run time by the executor.

---

## Licence

MIT — see [LICENSE](./LICENSE).
