# zjtskills

Personal skill repository for storing and maintaining reusable AI skills.

## Layout

- `*/SKILL.md`: skill entry file
- `*/scripts/`: helper scripts bundled with a skill
- `*/references/`: optional reference material loaded only when needed
- `*/assets/`: optional output assets or templates
- `scripts/import_claude_skill.sh`: import an existing Claude skill into this repo
- `scripts/import_codex_skill.sh`: import an existing Codex skill into this repo
- `codex-skills/`: Codex skill collection kept in this repository

## Current skills

- `docx-to-mermaid`

## Conventions

- One skill per top-level directory
- Directory name should match the skill name when possible
- Keep `SKILL.md` concise and task-oriented
- Put repeatable logic in `scripts/`
- Avoid extra docs unless they help maintain the skills

## Import a Claude skill

```bash
./scripts/import_claude_skill.sh /path/to/source-skill
```

This copies the source skill into a same-named directory in this repo and refuses to import if the source does not contain `SKILL.md`.

## Import a Codex skill

```bash
./scripts/import_codex_skill.sh /path/to/source-skill
```

This copies the source skill into `codex-skills/<skill-name>/` and refuses to import if the source does not contain `SKILL.md`.
