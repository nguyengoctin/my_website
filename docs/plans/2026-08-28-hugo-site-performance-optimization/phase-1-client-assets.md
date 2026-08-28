# Phase 1: Client Assets

**Plan:** [README.md](./README.md)
**Type:** sequential

## Progress

| Status  | Task |
| ------- | ---- |
| ⬜ TODO | Gate page-specific assets |
| ⬜ TODO | Reduce head payload |

## Tasks

1. Gate page-specific client assets so gallery, share, clipboard, lazysizes, and instant page logic only load on pages that actually need them.
   - Files: `hugo.toml`, `layouts/_partials/assets-default.html`, `layouts/_partials/assets.html`, `layouts/_partials/plugin/img.html`, `layouts/partials/header.html`, `layouts/partials/footer.html`
   - Verify: build the site and inspect home, article, and cheatsheet output to confirm only the needed asset tags are present; rerun `hugo --gc --minify --templateMetrics --templateMetricsHints --quiet` and compare the asset-template totals.

2. Reduce the head payload by trimming unnecessary font preconnect/preload duplication and keeping only the resource hints that still matter after asset gating.
   - Files: `layouts/_partials/head/link.html`
   - Verify: compare generated `<head>` output before and after on a normal content page and confirm typography still loads correctly.

