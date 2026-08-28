# Phase 3: RSS and SEO

**Plan:** [README.md](./README.md)
**Type:** sequential

## Progress

| Status  | Task |
| ------- | ---- |
| ⬜ TODO | Trim RSS outputs |
| ⬜ TODO | Simplify metadata lookups |

## Tasks

1. Remove RSS outputs that are not externally consumed, starting with taxonomy feeds, and keep only the feeds the site actually advertises.
   - Files: `hugo.toml`, `themes/LoveIt/layouts/term.rss.xml`, `themes/LoveIt/layouts/_partials/rss/item.html`
   - Verify: confirm `index.xml` and the remaining section feeds still render, and verify the RSS template metrics drop.

2. Simplify metadata lookup in the head and Open Graph templates by avoiding repeated resource resolution when explicit page metadata already exists.
   - Files: `layouts/partials/head/meta.html`, `layouts/partials/opengraph.html`
   - Verify: compare the generated metadata on the home page and on a post page, and confirm the head-template totals decrease in Hugo metrics.

