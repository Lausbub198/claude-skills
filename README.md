# claude-skills

My personal collection of Claude Code skills for BUILT — KI für den Mittelstand.

Each skill is a self-contained directory. Copy any skill into `~/.claude/skills/` and Claude Code picks it up automatically on the next session.

---

## Skills

| Skill | Description |
|-------|-------------|
| [advanced-prompt-builder](./advanced-prompt-builder/) | Interaktiver Prompt Builder nach dem Least-to-Most + Multi-Rollen + RICK Framework — für komplexe, mehrstufige Prompts mit mehreren Experten-Perspektiven |
| [prompt-builder](./prompt-builder/) | Interaktiver Prompt Builder nach dem 5-Pillar Framework (Rolle, Kontext, Auftrag, Constraints, Format) — schlankerer Ansatz für einzelne, fokussierte Prompts |
| [scroll-deck](./scroll-deck/) | Builds a polished, single-file HTML scroll-deck — zero dependencies, dark techy aesthetic, content reveals as the user scrolls |
| [spec-creator](./spec-creator/) | Creates publication-grade end-to-end software specifications in BUILT-Spec-Standard format — Greenfield dialogue or Upgrade gap-analysis |
| [spec2opsx](./spec2opsx/) | Converts a spec document into OpenSpec (opsx) changes — splits into logical units, creates full artifact set (proposal, specs, design, tasks) per change |
| [telepro-script](./telepro-script/) | Erstellt fertige TelePro-Teleprompter-Skripte im korrekten TelePro-Markdown-Format für BUILT YouTube-Videos |
| [youtube-production](./youtube-production/) | Konsolidierter YouTube-Produktions-Skill für alle BUILT-Videoformate (Sonne, Planet-Demo, Planet-Explainer) — produziert 8 Artefakte (A1–A8) im interaktiven oder autonomen Modus |
| [youtube-strategy](./youtube-strategy/) | Full pre-production strategy pipeline: Topic Research → Competitive Analysis → SEO & Metadata → Retention Script → A/B Testing → Demo Pack |
| [youtube-thumbnail](./youtube-thumbnail/) | Generates YouTube thumbnails via Gemini Flash based on video scripts and the BUILT Brandbook — 4 background variations per run |
| [mittelstands-usecase-analyser](./mittelstands-usecase-analyser/) | Analysiert deutsche Mittelstandsberufe (Handwerk, KMU, Dienstleistung) und erstellt KI-Transformationskonzepte mit 7-Punkte-Analyse, Mermaid-Diagrammen, SaaS-Vision, ROI-Metriken sowie Short/Long-Form-Videoskripten und Tech-Stack-Roadmaps |

---

## Installation

```bash
# Install a single skill
cp -r spec2opsx ~/.claude/skills/

# Install all skills
for d in */; do [ -f "$d/SKILL.md" ] && cp -r "$d" ~/.claude/skills/; done
```

---

## Usage

Invoke a skill by name in Claude Code:

```
/youtube-strategy
/spec-creator path/to/idea.md
/prompt-builder
```

See each skill's `SKILL.md` for full usage details and trigger phrases.

---

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Some skills require additional setup — check the individual `SKILL.md`
