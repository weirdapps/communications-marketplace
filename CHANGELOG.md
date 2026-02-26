# Changelog

All notable changes to the Communications Marketplace are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
