# 撰寫新的包

每一個包都是一份小小的 YAML。新增一個包是送 PR，不是改程式。

## 新增一個技能

1. 在 `registry/skills.json` 加一筆：`id`（英文 kebab-case）、`category`、
   雙語 `label`、雙語 `summary`、`outputs`、`requires`。
2. 在 `tools/gen_skill_docs.py` 的 `CONTRACT` 加對應內容——輸入項目與雙語品質標準。
3. 執行 `python tools/gen_skill_docs.py` 重新產生 `skills/<id>.md`。
4. 至少讓一個專案包引用它，否則它永遠不會被推薦到。

## 新增一個專案包

建立 `project-packs/<id>.yaml`：

```yaml
id: my-pack
label:   { en: "...", zh-TW: "..." }
icon: "📦"
summary: { en: "...", zh-TW: "..." }
recommended_skills: [ ... ]   # 預先勾選
suggested_skills:   [ ... ]   # 附理由供選擇
default_style: minimal
default_qa: standard
```

`recommended_skills` 要克制。什麼都推薦，等於什麼都沒推薦。

## 新增一個風格包

建立 `style-packs/<id>.yaml`，要有 `principles`、`tokens`，
還有大家最常省略的 `avoid` 清單。
有了 avoid 清單，`vision-judge` 才有辦法真的把風格「執行」起來。

## 規則

- ID：一律英文 kebab-case，沒有例外。
- 標籤與摘要：`en` 與 `zh-TW` 都要有。缺 `zh-TW` 會退回英文，那是 bug，不是設計。
- 絕不提交任何 token、金鑰或憑證。品牌包只放參照。
- 動過 registry 之後，開 PR 前兩個檢查都要跑：

```bash
python tools/validate.py
python tools/check_consistency.py
```

`check_consistency.py` 會抓到：沒有任何專案包引用到的技能、沒補齊的相依、
沒寫 `avoid` 清單的風格包、失效的文件連結，以及最常出事的那一種——
包裡有這個 id，但忘了加進 UI 內嵌的那份資料。
