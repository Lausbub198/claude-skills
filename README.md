# claude-skills

A collection of Claude Code skills for spec-driven development workflows.

Each skill is a self-contained directory you can install independently.

---

## Skills

| Skill | Description |
|-------|-------------|
| [spec2opsx](./spec2opsx/) | Convert a spec document into OpenSpec changes — vertical slices, full artifact set, skill-aware |

---

## Installation

### Install a single skill

```bash
cp -r spec2opsx ~/.claude/skills/
```

### Install all skills

```bash
cp -r */ ~/.claude/skills/
```

Claude Code picks up new skills automatically on the next session.

---

## Usage

Once installed, invoke a skill by name in Claude Code:

```
/spec2opsx path/to/your-spec.md
```

See each skill's `README.md` for full usage details and flags.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI

Some skills have additional dependencies — check the individual `README.md`.
