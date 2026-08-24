# Installing VSC as a Claude Code skill

Two entry points exist, and they are deliberately different files:

| File | Who reads it | Paths |
|---|---|---|
| [`../SKILL.md`](../SKILL.md) | An agent already working **inside** this repo | Relative |
| [`claude-code/SKILL.md`](./claude-code/SKILL.md) | A globally installed skill, invoked from **any** directory | Absolute, points at your clone |

## Install

```bash
mkdir -p ~/.claude/skills/visual-skill-composer
cp install/claude-code/SKILL.md ~/.claude/skills/visual-skill-composer/SKILL.md
```

Windows (Git Bash) is the same command. Restart Claude Code so it picks up the new skill.

## After installing

Open `~/.claude/skills/visual-skill-composer/SKILL.md` and fix the clone path under
**資料位置 / Data location** if you did not clone to `C:/Users/user/visual-skill-composer/`.
The skill reads the packs from disk on every run, so `git pull` in your clone is all it
takes to get new packs — you do not reinstall the skill.

The installed copy is written in Traditional Chinese because its trigger phrases have to
match how its author actually asks. Translate the `description` frontmatter if you work in
another language; keep every id in it untouched.
