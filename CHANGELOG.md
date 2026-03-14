# Changelog

All notable changes to the Communications Marketplace are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.0] - 2026-03-15

### Added
- **presentation-maker**: Bumper pill pattern — rounded rect (1.3x0.3), fill `007B85`, 9pt Bold white ALL CAPS
- **presentation-maker**: Greek systemic bank logo colors documented (NBG `003841`, Alpha `0D3B70`, Piraeus `FFD900`, Eurobank `EA002A`)
- **presentation-maker**: No-shadow rule enforced on all shapes (pills, boxes, cards)
- **presentation-maker**: Native chart requirement — proper python-pptx/Excel charts only
- **marketplace**: JSON Schema for plugin.json validation (`schemas/plugin.schema.json`)
- **marketplace**: Cross-plugin agent contracts documentation (`docs/agent-contracts.md`)
- **marketplace**: CI validation workflow (`.github/workflows/validate.yml`)
- **marketplace**: Plugin settings system in plugin.json manifests

### Changed
- **presentation-maker**: Metric card sizing — value 50pt Bold `003841`, label 16pt `5A5F5A` (was 18pt/9pt)
- **presentation-maker**: Content slide title at y=0.75" with bumper, y=0.5" without (dynamic positioning)
- **presentation-maker**: Brand spec duplication reduced — agent SKILL.md files now reference shared specs
- **presentation-maker**: `nbg_validate.py` uses `defusedxml` instead of `xml.etree.ElementTree` (security)
- **marketplace**: `install.sh` — fixed stale email-drafter references, added dependency resolution

### Removed
- Temporary bank investor presentation PDFs from `docs/` (17MB of tracked binaries)

## [2.0.0] - 2026-03-12

### Added
- **email-handler**: Hybrid Apple Mail + Outlook architecture (replaced Playwright browser automation)
- **email-handler**: New `/send-mail` command for composing new emails via Outlook AppleScript
- **email-handler**: Self-learning style guide system with draft-vs-actual comparison
- **email-handler**: Per-recipient tone profiles in style guide
- **creative-toolkit**: Device Mockup agent for pixel-perfect iPhone mockups
- **presentation-maker**: v3.1 — improved slide type normalization and accessibility colors

### Changed
- **Breaking**: email-drafter plugin renamed to email-handler
- **Breaking**: Playwright browser automation replaced with native Apple Mail + Outlook AppleScript
- **email-handler**: `/draft` command replaced by `/mail-review` (expanded with briefing and insights)

### Removed
- Playwright MCP server dependency for email reading
- Outlook Web (outlook.office.com) requirement

## [1.1.0] - 2026-03-11

### Added
- **email-handler**: New `/inbox-briefing` command — read-only inbox scan with summaries, action recommendations, and insights. No drafting or reply composition. Faster and more reliable than `/mail-review` for quick inbox triage.

## [1.0.0] - 2026-02-23

### Added
- CHANGELOG.md for proper version tracking
- Enhanced GitHub Actions validation workflow
- Icon workflow decision guidance in asset-library.md
- Improved plugin template with comprehensive examples

### Changed
- **Breaking**: Fixed marketplace.json structure documentation (array format, not object)
- Updated install.sh to correctly validate marketplace.json (was checking for plugin.json)
- Fixed "Thank You" slide contradictions in Storyline Architect (now consistently uses "Back Cover")
- Synchronized version numbers across all files to v3.0.0
- Updated creating-plugins.md with correct marketplace.json format
- Improved README.md documentation accuracy

### Fixed
- Install script validation bug checking wrong file path
- Documentation inconsistencies between actual file structure and docs
- Storyline Architect structure patterns that contradicted "No Thank You" rule

## [0.9.0] - 2026-02-18 (Marketplace Launch)

### Added
- Restructured as a marketplace for multiple plugins
- NBG Presentations plugin moved to `plugins/nbg-presentations/`
- Plugin template and documentation in `plugins/_template/`
- Plugin categories and discovery system
- Install/uninstall scripts for easy deployment

### NBG Presentations Plugin v3.0.0

#### Added
- Multi-agent architecture with specialized agents
- Orchestrator pattern for coordinating agent workflow
- McKinsey-quality standards (Pyramid Principle, SCQA, MECE)
- Comprehensive brand system documentation
- Asset library with 338 icons, 21 illustrations, 117 screenshots
- Pillar Design System integration
- OOXML chart editing reference

#### Agents
- **NBG Presenter**: Master orchestrator
- **Storyline Architect**: Narrative structure design
- **Storyboard Designer**: Visual layout planning
- **Graphics Renderer**: PPTX generation
- **Infographic Specialist**: Data visualization
- **Icon Designer**: Custom SVG icon creation

#### Commands
- `/create-presentation`: Create new NBG presentation
- `/redesign-deck`: Redesign existing presentation
- `/create-infographic`: Generate data visualization
- `/create-icon`: Create NBG-compliant SVG icon
- `/polish-slides`: Quick formatting fix

## Previous Versions (NBG-only, before marketplace)

### v2.0.0
- Multi-agent architecture introduced
- Separated concerns into specialist agents

### v1.0.0
- Initial monolithic plugin for NBG presentations
