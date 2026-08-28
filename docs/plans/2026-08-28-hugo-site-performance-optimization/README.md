---
slug: 2026-08-28-hugo-site-performance-optimization
auto: false
status: in-progress
---

# Plan: Hugo Site Performance Optimization

**Mode:** normal
**Created:** 2026-08-28
**Status:** IN PROGRESS

## Overview

The site is already reasonably fast, but the audit showed repeated cost from global assets, RSS generation, content transforms, and responsive image processing. This plan reduces those costs in phases so each improvement can be measured in isolation and rolled back cleanly if needed.

## Not Building

- No redesign of the site visual language.
- No content migration or rewrite of posts.
- No new search provider or analytics platform.
- No broad architecture changes outside the Hugo theme and templates already in use.

## Progress

| Status  | Phase                         | File                                                                 | Tasks   |
| ------- | ----------------------------- | -------------------------------------------------------------------- | ------- |
| ✅ DONE | Phase 1: Client Assets        | [phase-1-client-assets.md](./phase-1-client-assets.md)             | 2 tasks |
| ✅ DONE | Phase 2: Build Hot Paths      | [phase-2-build-hot-paths.md](./phase-2-build-hot-paths.md)         | 2 tasks |
| ✅ DONE | Phase 3: RSS and SEO          | [phase-3-rss-and-seo.md](./phase-3-rss-and-seo.md)                 | 2 tasks |
| ⬜ TODO | Phase 4: Images and Cleanup   | [phase-4-images-and-cleanup.md](./phase-4-images-and-cleanup.md)   | 2 tasks |

## Assumptions

- Search stays enabled site-wide because it is part of the current navigation flow and user experience.
- Taxonomy RSS feeds can be removed if no external consumer depends on them; the audit did not find in-repo links to those feeds.
- The current typography and overall look should stay unless a performance change has a clear measurable benefit.

## Risks

- Gating page-specific assets too aggressively can break gallery, share, or code-copy behavior on pages that need them.
- Disabling syntax guessing can expose unannotated code fences that currently rely on Hugo's fallback detection.
- Trimming RSS outputs can break outside subscribers if a feed URL is already in use.
- Reducing image variants can lower visual quality on some screens if the breakpoints are chosen too narrowly.

## Next Steps

After implementation: `$cf-review` -> `$cf-commit`
