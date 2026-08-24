---
name: visual-skill-composer
description: VSC 視覺化 AI 技能組裝系統（全域可用）。當使用者要開始一個新的視覺／內容專案，需要決定「這個專案要用哪些 AI 技能、什麼視覺風格、套哪套品牌、品質檢查要多嚴」時，使用此技能組出一份 Project Manifest。務必在下列情境觸發：使用者說「幫我組一個技能包」「這個專案需要哪些能力／技能」「開一個新專案要用哪些 skill」「產一份 VSC manifest」「用 VSC 組」「Project Skill Pack」；或是使用者說要做「簡報／網站／短影音／儀表板／資訊圖卡／報告／漫畫筆記／品牌系統／社群貼文」但還沒決定要用哪些能力與風格，需要先把規格談清楚再動手。產出是通過 schema 驗證的 manifest，交給 VAD 或任何 agent runtime 執行。VSC 只組裝、不執行。
---

# Visual Skill Composer（VSC）

把一句模糊的需求（「幫我做一份課程簡報」）變成一份明確、可驗證的 Project Manifest：
專案類型、技能清單、視覺風格、品牌來源、品質門檻。

**這個技能負責組裝，不負責執行。** 不渲染、不呼叫生圖模型、不寫出任何素材——
那是 VAD（`draiagent/Visual-Agent-Design`）或其他 runtime 的工作。

## 資料位置

本機 clone：`C:/Users/user/visual-skill-composer/`

| 路徑 | 用途 |
|---|---|
| `registry/skills.json` | 所有技能：id、分類、雙語標籤、`requires` 相依 |
| `project-packs/*.yaml` | 專案類型與各自的推薦／建議技能組 |
| `style-packs/*.yaml` | 視覺 token 與 `avoid` 清單 |
| `brand-packs/*.yaml` | 品牌來源參照 |
| `qa-packs/*.yaml` | 檢查項目、通過門檻、修正重跑次數 |
| `schemas/project-manifest.schema.json` | 產出的契約 |

**每次都要實際讀檔，不要憑記憶列技能。** 這些包會持續新增。
若本機沒有 clone，先 `git clone https://github.com/draiagent/visual-skill-composer.git`，
或請使用者直接開 <https://draiagent.github.io/visual-skill-composer/> 自己點選。

## 流程

1. **判定專案類型。** 把需求對到 `project-packs/` 裡的一個檔案。
   對不到就問，**不要自己發明 pack id**。
2. **帶入技能。** 用該 pack 的 `recommended_skills` 當預設，
   再把 `suggested_skills` 逐一提出來，並說明「為什麼這個專案需要它」。
3. **補齊相依。** `registry/skills.json` 裡每個技能都有 `requires`：
   `brand-check` 需要 `brand-system`、`auto-repair` 需要 `vision-judge`。
   缺的就補上，或是把依賴它的技能拿掉——**絕不產出跑不起來的組合**。
4. **選風格包。** 預設用 pack 的 `default_style`，除非使用者另有指定。
   要一併把該風格的 `avoid` 清單講給使用者聽，那是風格能被執行的關鍵。
5. **選品牌來源。** 只記錄參照。**永遠不要把 token、金鑰、憑證寫進 manifest。**
   若使用者選 `none`，`brand_check` 就必須是 `false`——不能叫執行端去比對一套沒載入的品牌。
6. **選品控包。** 預設用 pack 的 `default_qa`。
7. **產出 manifest**（預設 YAML），然後驗證：
   ```bash
   python tools/validate.py <檔案>
   ```
8. **交棒。** 說明應該由誰執行（`runtime.target`，預設 `vad`）。

## 規則

- **技能 ID 一律英文 kebab-case，永遠不翻譯**，就算整段對話都是繁體中文也一樣。
  要翻譯的是標籤，不是 ID。
- `project.language` 是**成品**的語言，不是對話的語言。分不清楚就問。
- 不要擅自加入使用者沒選、專案包也沒推薦的技能。要建議就用講的。
- 使用者若要求 VSC 直接把成品做出來，直說：**VSC 組裝、VAD 執行**，
  然後把 manifest 交出去，或改用對應的產出技能（例如 `draw`、`claude-design`）。
- 動過本機 repo 裡的任何包之後，要跑 `python tools/check_consistency.py`——
  `ui/index.html` 為了零相依內嵌了一份同樣的資料，那是最容易走鐘的地方。

## 產出範例

```yaml
vsc_version: 0.1.0
project:
  type: academic-presentation
  language: zh-TW
  title: 生成式 AI 教學導論
skills:
  - instructional-design
  - storytelling
  - presentation-design
  - infographic
  - data-visualization
  - research
visual:
  style: swiss-editorial
brand:
  source: github
  ref: draiagent/Enterprise-Brand-Style-AI-Design-System
quality:
  pack: standard
  vision_judge: true
  text_check: true
  brand_check: true
  auto_repair: false
  threshold: 80
  max_repair_rounds: 2
runtime:
  target: vad
  created: "2026-08-24"
```

## 與其他技能的關係

```text
Promptless Skill  →  VSC（決定帶哪些工具出門）  →  VAD（決定工具怎麼完成工作）
```

- 品牌視覺細節：`infographic-brand-style`、`dual-brand-glassmorphism` 等品牌 skill
- 實際生圖：`draw`
- 實際做網頁／簡報：`claude-design`
