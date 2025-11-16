# IBDM Documentation Index

**Last Updated**: 2025-11-15

Quick navigation to all IBDM documentation, organized by purpose and currency.

---

## 🚀 Start Here

| Document | Purpose |
|----------|---------|
| [README.md](../README.md) | Project overview, quick start, key features |
| [GETTING_STARTED.md](../GETTING_STARTED.md) | Comprehensive tutorial on IBDM concepts |
| [CLAUDE.md](../CLAUDE.md) | **Development guide** - Policies, workflow, tooling (read this first!) |

---

## 📋 Current Status & Planning

| Document | Purpose |
|----------|---------|
| [IBIS_PROGRESSION_GUIDE.md](../IBIS_PROGRESSION_GUIDE.md) | **IBiS1→2→3→4 roadmap** - How to progress through Larsson's stages (ESSENTIAL READ) |
| [IBIS_VARIANTS_PRIORITY.md](../IBIS_VARIANTS_PRIORITY.md) | **NEW: IBiS-2,3,4 completion plan** - 22-28 week roadmap to complete all variants (CURRENT PRIORITY) |
| [NEXT-TASK.md](../NEXT-TASK.md) | **Next recommended task** - Start here for immediate work |
| [LARSSON_TASK_MAPPING.md](../LARSSON_TASK_MAPPING.md) | Task-to-thesis mapping - All beads tasks mapped to thesis chapters |
| [LARSSON_PRIORITY_ROADMAP.md](../LARSSON_PRIORITY_ROADMAP.md) | Original priorities, tier-based task breakdown |
| [SYSTEM_ACHIEVEMENTS.md](../SYSTEM_ACHIEVEMENTS.md) | What's been built - 10,893 LOC, 527 tests, Phase 3.5 complete |

### Status Reports & Analysis

| Document | Purpose |
|----------|---------|
| [Project Status (2025-11-16)](../reports/project-status-2025-11-16.md) | Snapshot at IBD-1 completion - comprehensive status, gaps, demo readiness |
| [IBD-1 Completion Analysis](../reports/ibd-1-completion-analysis.md) | Detailed assessment vs. demonstration goals and Larsson thesis |

---

## 🏗️ Architecture & Design

### Core Architecture

| Document | Purpose |
|----------|---------|
| [architecture_principles.md](architecture_principles.md) | **Policy #0** - Clarity, simplicity, no fallbacks |
| [LARSSON_ALGORITHMS.md](LARSSON_ALGORITHMS.md) | **Authoritative reference** - IBiS1-4 algorithms, rules, state structures |
| [burr_state_refactoring.md](burr_state_refactoring.md) | Stateless engine design (ibdm-bsr epic) |
| [architecture_interpretation_accommodation.md](architecture_interpretation_accommodation.md) | Full analysis: accommodation phase separation |
| [interpretation-accommodation-quick-ref.md](interpretation-accommodation-quick-ref.md) | Quick reference: task accommodation phase boundaries |

### Domain & Semantics

*Domain layer documentation TBD - see src/ibdm/core/domain.py and src/ibdm/domains/*

---

## ⚙️ Configuration & Setup

| Document | Purpose |
|----------|---------|
| [environment_setup.md](environment_setup.md) | Environment variables, IBDM_API_KEY configuration |
| [llm_configuration.md](llm_configuration.md) | LiteLLM setup, Claude 4.5 Sonnet/Haiku usage |

---

## 📖 Reference Material

### Larsson Thesis

| Document | Purpose |
|----------|---------|
| [larsson_thesis/README.md](larsson_thesis/README.md) | Thesis chapter index |
| [larsson_thesis/chapter_*.md](larsson_thesis/) | Extracted thesis chapters (1-6) |
| [Larsson_Tesis_nopages.md](Larsson_Tesis_nopages.md) | Full thesis (single file) |

---

## 🗄️ Historical Documentation

See [archive/README.md](archive/README.md) for organization of historical docs.

### Archive Categories

| Directory | Contents |
|-----------|----------|
| [archive/design-discussions/](archive/design-discussions/) | Architectural analysis, framework critiques |
| [archive/refactoring-plans/](archive/refactoring-plans/) | Completed refactoring plans |
| [archive/planning/](archive/planning/) | Original planning documents (8-phase plan, demo plan, NLU plan, structure) |
| [archive/reviews/](archive/reviews/) | One-time reviews and assessments (API key verification, deprecated approaches) |

### Notable Archived Docs

| Document | Status | Location |
|----------|--------|----------|
| DEVELOPMENT_PLAN.md | 📋 HISTORICAL | archive/planning/ (original 8-phase plan) |
| DEMO_PLAN.md | ✅ COMPLETED | archive/planning/ (comprehensive demo strategy) |
| NLU_ENHANCEMENT_PLAN.md | ✅ COMPLETED | archive/planning/ (Phase 3.5 done) |
| PROJECT_STRUCTURE.md | 📋 HISTORICAL | archive/planning/ (ideal directory structure) |
| ibdm-64.14-review.md | ❌ DEPRECATED | archive/reviews/ (hybrid fallback review) |
| IBDM_API_KEY_VERIFICATION.md | 📖 REFERENCE | archive/reviews/ (initial setup validation) |
| PYTRINDIKIT_VERDICT.md | 📖 REFERENCE | archive/design-discussions/ |

---

## 📝 Status Markers Guide

Documents use these status markers in headers:

| Marker | Meaning |
|--------|---------|
| **✅ CURRENT** | Actively maintained, authoritative |
| **📋 HISTORICAL** | Original planning, evolved significantly |
| **✅ COMPLETED** | Implementation finished |
| **❌ DEPRECATED** | Approach superseded |
| **📖 REFERENCE** | Background material, still valid |

---

## 🔍 Finding Documentation

### By Task Type

**I want to...**

| Task | Read |
|------|------|
| **Start work NOW** | **[NEXT-TASK.md](../NEXT-TASK.md)** ← **Immediate next task** |
| **Complete IBiS variants** | **[IBIS_VARIANTS_PRIORITY.md](../IBIS_VARIANTS_PRIORITY.md)** ← **22-28 week roadmap** |
| Start development | [CLAUDE.md](../CLAUDE.md) → [GETTING_STARTED.md](../GETTING_STARTED.md) |
| Understand architecture | [architecture_principles.md](architecture_principles.md) → [LARSSON_ALGORITHMS.md](LARSSON_ALGORITHMS.md) |
| Understand IBiS progression | [IBIS_PROGRESSION_GUIDE.md](../IBIS_PROGRESSION_GUIDE.md) |
| Check IBD-1 status | [IBD-1 Completion Analysis](../reports/ibd-1-completion-analysis.md) |
| Check detailed status | [Project Status (2025-11-16)](../reports/project-status-2025-11-16.md) |
| Set up environment | [environment_setup.md](environment_setup.md) → [llm_configuration.md](llm_configuration.md) |
| See what's built | [SYSTEM_ACHIEVEMENTS.md](../SYSTEM_ACHIEVEMENTS.md) |
| Find original priorities | [LARSSON_PRIORITY_ROADMAP.md](../LARSSON_PRIORITY_ROADMAP.md) |
| Map tasks to thesis | [LARSSON_TASK_MAPPING.md](../LARSSON_TASK_MAPPING.md) |
| Understand Larsson | [LARSSON_ALGORITHMS.md](LARSSON_ALGORITHMS.md) → [larsson_thesis/](larsson_thesis/) |
| Understand phase boundaries | [interpretation-accommodation-quick-ref.md](interpretation-accommodation-quick-ref.md) |

### By Larsson System

| System | Docs |
|--------|------|
| **IBiS1** (Basic QUD) | LARSSON_ALGORITHMS.md §IBiS1, larsson_thesis/chapter_2.md |
| **IBiS2** (Grounding) | LARSSON_ALGORITHMS.md §IBiS2, larsson_thesis/chapter_3.md |
| **IBiS3** (Accommodation) | LARSSON_ALGORITHMS.md §IBiS3, larsson_thesis/chapter_4.md |
| **IBiS4** (Actions) | LARSSON_ALGORITHMS.md §IBiS4, larsson_thesis/chapter_5.md |

---

## 🔗 External Resources

- [Burr Documentation](https://burr.dagworks.io/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pyright Documentation](https://github.com/microsoft/pyright)

---

## 📊 Documentation Statistics

- **Total .md files**: 53 (before cleanup), 32+ (after archiving)
- **Current & authoritative**: 15 files (28%)
- **Archived historical**: 21 files (40%)
- **Reference material**: 12+ files (23%)

Last audit: 2025-11-15

---

## 💡 Documentation Policies

From [CLAUDE.md](../CLAUDE.md):

1. **Active docs**: Top-level + docs/{architecture,configuration,reference}
2. **Archive old docs**: docs/archive/ with status markers
3. **Single source of truth**: No duplicates (CLAUDE.md is canonical, AGENTS.md auto-synced)
4. **Status markers**: Always use in headers
5. **Keep INDEX current**: Update when adding/moving docs

---

**Questions or suggestions?** Open an issue or update this index!
