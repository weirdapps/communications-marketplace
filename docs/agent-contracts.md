# Agent Contracts

Cross-plugin API contracts for the communications marketplace. Each agent documents its input format, output format, side effects, and dependencies.

---

## Presentation Maker Pipeline

### Storyline Architect

| Field | Value |
|-------|-------|
| **Plugin** | presentation-maker |
| **Path** | `agents/storyline-architect/SKILL.md` |
| **Input** | Raw content (text, data, bullets, existing presentation) |
| **Output** | YAML storyline with `presentation.slides[]` array. Each slide has: `slide_id`, `type`, `key_message`, `content`, `recommended_visual` |
| **Side Effects** | None (pure transformation) |
| **Dependencies** | None |

### Storyboard Designer

| Field | Value |
|-------|-------|
| **Plugin** | presentation-maker |
| **Path** | `agents/storyboard-designer/SKILL.md` |
| **Input** | YAML storyline from Storyline Architect |
| **Output** | YAML storyboard with `storyboard.slides[]` array. Each slide has: `slide_id`, `layout`, `elements[]` with exact positions (x, y, w, h), styles, and content |
| **Side Effects** | None (pure transformation) |
| **Dependencies** | Storyline Architect output, `shared/nbg-brand-system/README.md` |

### Graphics Renderer

| Field | Value |
|-------|-------|
| **Plugin** | presentation-maker |
| **Path** | `agents/graphics-renderer/SKILL.md` |
| **Input** | YAML storyboard from Storyboard Designer |
| **Output** | `.pptx` file at specified output path |
| **Side Effects** | Creates PPTX file, may create temp files during build |
| **Dependencies** | Storyboard Designer output, `tools/nbg-presentation/nbg_build.py`, PPTX scripts (document-skills plugin), template files in `assets/templates/` |

### NBG Presenter (Orchestrator)

| Field | Value |
|-------|-------|
| **Plugin** | presentation-maker |
| **Path** | `orchestrator/nbg-presenter/SKILL.md` |
| **Input** | User request (brief, content, or existing deck) |
| **Output** | Completed `.pptx` presentation |
| **Side Effects** | Coordinates all pipeline agents, creates final PPTX |
| **Dependencies** | All pipeline agents, creative-toolkit agents (optional) |

---

## Creative Toolkit Agents

### Icon Designer

| Field | Value |
|-------|-------|
| **Plugin** | creative-toolkit |
| **Path** | `agents/icon-designer/SKILL.md` |
| **Input** | Icon concept description, optional brand/color context |
| **Output** | SVG code (64x64 viewBox, solid fill, monochrome) |
| **Side Effects** | Creates `.svg` file |
| **Dependencies** | None |

### Infographic Specialist

| Field | Value |
|-------|-------|
| **Plugin** | creative-toolkit |
| **Path** | `agents/infographic-specialist/SKILL.md` |
| **Input** | Data and context for visualization |
| **Output** | SVG or chart specification |
| **Side Effects** | Creates visualization files |
| **Dependencies** | None |

### Device Mockup

| Field | Value |
|-------|-------|
| **Plugin** | creative-toolkit |
| **Path** | `agents/device-mockup/SKILL.md` |
| **Input** | Screenshot path, optional frame key |
| **Output** | PNG mockup image |
| **Side Effects** | Creates `_mockup.png` file |
| **Dependencies** | `tools/device-mockup/iphone_mockup.py`, Pillow, numpy, device frame assets |

---

## Email Handler

### Email Handler Agent

| Field | Value |
|-------|-------|
| **Plugin** | email-handler |
| **Path** | `agents/email-handler/SKILL.md` |
| **Input** | Command arguments (folder, count, flags) |
| **Output** | Inbox briefing, draft replies, learning summary |
| **Side Effects** | Reads Apple Mail inbox, creates Outlook reply drafts, updates `~/.claude/drafts/inbox-state.json`, saves drafts to `~/.claude/drafts/pending/`, updates `shared/style-guide.md` |
| **Dependencies** | Apple Mail (reading), Microsoft Outlook (sending/replying), `shared/style-guide.md` |

---

## Cross-Plugin Dependencies

```
presentation-maker ──depends-on──> creative-toolkit
                   │
                   ├── icon-designer (custom icons for slides)
                   ├── infographic-specialist (data visualizations)
                   └── device-mockup (app screenshots in frames)
```

The `presentation-maker` orchestrator invokes creative-toolkit agents as needed during the pipeline. These are optional — presentations can be created without custom icons or infographics.
