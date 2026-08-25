[English](./README.md) | **繁體中文**

# Visual Skill Composer（VSC）

**視覺化 AI 技能組裝系統**

> 讓使用者用「選、組、看」的方式，建立專案需要的 AI 技能組合。

選擇你要做什麼、看見這個專案真正需要哪些 AI 能力、挑好視覺風格與品牌系統、
決定品質控制要多嚴格——最後產生一份機器可讀的 **Project Manifest**，
交給任何 agent runtime 執行。

> 從「寫 Prompt 使用 AI」→「安裝 Skill 使用 AI」→ **「視覺化組裝 AI 能力」**。

---

## 為什麼需要這個東西

一般的 Skill Marketplace 給你一張清單。但清單不會告訴你：
哪些技能應該一起用、這個專案還缺什麼、做出來會長什麼樣子。

VSC 把打勾清單換成五個「用看的就能做」的決策：

| 層級 | 問題 | 產出 |
|---|---|---|
| ① 專案 | 你今天想完成什麼？ | `project.type` |
| ② 技能 | 這個專案需要哪些能力？ | `skills[]` |
| ③ 視覺 | 希望作品呈現什麼風格？ | `visual.style` |
| ④ 品牌 | 套用哪一套品牌系統？ | `brand.source` |
| ⑤ 品控 | 品質控制要到什麼程度？ | `quality.*` |

**每一層都會收斂下一層。** 選了「大學教學簡報」，系統會自動勾選
教學設計、故事敘事、資訊圖解，並額外建議加入文獻研究與 Vision Judge。

---

## 用一張漫畫看懂這條流程

**[技能包的五層漏斗](https://draiagent.github.io/visual-skill-composer/comic/)**
——八格漫畫筆記，一層一格走完五層。遮住文字，八格仍讀得出因果。

這張漫畫本身就是走完一次 VAD `VAC-COMIC-001` 標準卡的產物，
所以它同時是這個 repo 在講的那條交接流程的實作範例：先分鏡、依 rubric 評分、再動筆。
分鏡原始檔在 [`examples/vsc-flow-8panel.storyboard.json`](./examples/vsc-flow-8panel.storyboard.json)，
通過 VAD-Comic-Notes 的 storyboard schema 驗證。

---

## VSC 與 VAD 的關係

這兩個**刻意不合併**。

```text
             VSC
     Visual Skill Composer
       視覺化技能組裝器
              │
              │ 選擇 / 組合
              ↓
        Project Skill Pack   ← schemas/project-manifest.schema.json
              │
              ↓
             VAD
     Visual Agent Design
       視覺任務執行框架
              │
       ┌──────┼──────┐
       ↓      ↓      ↓
     Figma  Assets  Brand
       │
       ↓
   AI Generation
       │
       ↓
   Vision Judge
       │
       ↓
   Auto Repair
```

用費曼的講法：

> **VSC 決定「要帶哪些工具出門」；VAD 決定「這些工具怎麼完成工作」。**

VSC 本身不執行任何東西，它只負責組裝、驗證、交棒。
VAD 端用 `python tools/vac_runner.py vsc <manifest>` 把 manifest 讀進去，
編譯成標準 VAC 卡再執行，接口規格見
[VSC-INTERFACE.md](https://github.com/draiagent/Visual-Agent-Design/blob/main/docs/VSC-INTERFACE.md)。

這條交接背後對應到 VAD 的核心原則
[**High Intelligence for Discovery, Low Cost for Execution**](https://github.com/draiagent/Visual-Agent-Design#核心原則high-intelligence-for-discovery-low-cost-for-execution)：

> 第一次用高階 AI「學會」，之後讓低成本 Agent「重複做好」。

VSC 組裝出的 Project Skill Pack，正是「學會」之後被固化下來、可重複交給低成本 Agent 執行的規格——
探索階段的成本落在組裝與驗證，執行階段才輪到 VAD 用最省成本的方式規模化跑起來。

---

## 快速開始

**直接使用：**<https://draiagent.github.io/visual-skill-composer/> — 免安裝，
所有選擇都留在你的瀏覽器裡，不會送出去。

或在本機跑：

```bash
git clone https://github.com/draiagent/visual-skill-composer.git
cd visual-skill-composer
python -m http.server 4321 --directory ui
```

打開 <http://localhost:4321>，組好之後按「▶ 建立技能包」。
介面是單一自足的 HTML 檔，不需要打包、沒有相依套件。

驗證 manifest，以及檢查各個包之間的一致性：

```bash
python tools/validate.py examples/academic-presentation.vsc.yaml
python tools/check_consistency.py
```

### 安裝成 Claude Code 全域技能

```bash
mkdir -p ~/.claude/skills/visual-skill-composer
cp install/claude-code/SKILL.md ~/.claude/skills/visual-skill-composer/SKILL.md
```

裝完重開 Claude Code，之後在任何目錄說「幫我組一個技能包」就會觸發。
細節見 [install/README.md](./install/README.md)。

---

## 產出的 Manifest 長這樣

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

## 從第一天就雙語

這個 repo 裡的**所有 ID 一律英文 kebab-case，永遠不翻譯**。
中英文標籤是資料，在顯示的時候才解析。

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

**底層 ID 永遠英文，UI 可以繁體中文／英文切換。**
這樣 GitHub、Claude Code、Codex、Gemini CLI 都不受語言影響——
不管組裝的人用哪一種語言，讀到的都是同一份 manifest。

---

## 專案結構

```text
visual-skill-composer/
├── README.md              英文（預設首頁）
├── README.zh-TW.md        繁體中文
├── SKILL.md               給 agent 讀的進入點
├── docs/{en,zh-TW}/       概念、manifest 規格、撰寫指南
├── registry/skills.json   技能的唯一事實來源
├── skills/                每個技能一份契約文件
├── project-packs/         你要做什麼
├── style-packs/           長什麼樣子
├── brand-packs/           套誰的品牌
├── qa-packs/              檢查多嚴格
├── schemas/               Manifest 的 JSON Schema
├── install/               全域 Claude Code 技能
├── tools/                 validate.py、check_consistency.py、gen_skill_docs.py
├── index.html             GitHub Pages 入口，導向 ui/
├── comic/                 解釋流程的八格漫畫筆記
├── ui/index.html          組裝介面（單一檔案、免打包）
└── examples/              範例 manifest
```

---

## 安全性說明

VSC **只存參照，不存金鑰**。Figma 品牌包記錄的是 file key 與環境變數名稱，
token 本身不進版控，實際解析由執行端在執行階段完成。

---

## 授權

MIT，見 [LICENSE](./LICENSE)。
