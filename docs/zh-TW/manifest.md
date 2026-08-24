# Project Manifest 規格

Schema：[`schemas/project-manifest.schema.json`](../../schemas/project-manifest.schema.json)

驗證方式：

```bash
python tools/validate.py path/to/manifest.yaml
```

## 欄位

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `vsc_version` | string | 是 | Manifest 格式版本，例如 `0.1.0`。 |
| `project.type` | string | 是 | `project-packs/` 裡的 id。 |
| `project.title` | string | 否 | 自由文字，上限 200 字。 |
| `project.language` | string | 否 | **成品**的語言（BCP-47），預設跟隨組裝當下的介面語言。 |
| `project.audience` | string | 否 | 這份東西給誰看。 |
| `project.notes` | string | 否 | 執行端需要知道的其他事。 |
| `skills[]` | string[] | 是 | 來自 `registry/skills.json` 的 id，不可重複，至少一個。 |
| `visual.style` | string | 否 | `style-packs/` 裡的 id。 |
| `visual.overrides` | object | 否 | 疊加在風格包之上的 token 覆寫。 |
| `brand.source` | enum | 否 | `none`、`local`、`figma`、`github`、`upload`。 |
| `brand.ref` | string | 否 | 路徑、repo 名稱或 file key。**絕不可以是金鑰。** |
| `quality.pack` | string | 否 | `qa-packs/` 裡的 id。 |
| `quality.vision_judge` | bool | 否 | 渲染出來實際看過並評分。 |
| `quality.text_check` | bool | 否 | 溢出、孤行、中文斷行、錯字。 |
| `quality.brand_check` | bool | 否 | token 能不能對回品牌包。 |
| `quality.auto_repair` | bool | 否 | 重新產製直到通過門檻。 |
| `quality.threshold` | int 0-100 | 否 | 品質分數的及格線。 |
| `quality.max_repair_rounds` | int 0-10 | 否 | 修正重跑次數上限。 |
| `runtime.target` | enum | 否 | `vad`、`claude-code`、`codex`、`gemini-cli`、`generic`。 |
| `runtime.created` | date string | 否 | `YYYY-MM-DD`，在 YAML 裡要加引號。 |

每一層的 `additionalProperties` 都是 `false`：
不認識的欄位是錯誤，不是「安靜忽略的提示」。

## 執行端契約

VAD 已經實作這份契約。manifest 會被編譯到 Standard VAC Five-Pack 的標準卡上再執行：

```bash
git clone https://github.com/draiagent/Visual-Agent-Design.git
cd Visual-Agent-Design
python tools/vac_runner.py vsc <manifest> --packs ../visual-skill-composer
```

`--packs` 是讓接口指回本 repo，才能解析風格包的 `avoid` 清單。
不給也能編譯出合法的卡，但卡上會明確帶一條「風格包未解析」的約束。
目前只有五種有標準卡的專案類型能編譯（`academic-presentation`、`website`、`video`、
`dashboard`、`report`），其餘會被拒絕而不是硬猜一張最接近的卡。接口規格見
[VSC-INTERFACE.md](https://github.com/draiagent/Visual-Agent-Design/blob/main/docs/VSC-INTERFACE.md)。

宣稱支援 VSC 的執行端必須做到：

1. 驗證失敗的 manifest 一律拒絕執行。
2. 遵守風格包的 `avoid` 清單，而不是只讀 token。
3. 自己用自己的憑證去解析 `brand.ref`；manifest 永遠不帶憑證。
4. 每一個設為 `true` 的 `quality.*` 都要真的跑，並回報實際分數。
5. 到 `max_repair_rounds` 就停並說明，不要無限迴圈。
