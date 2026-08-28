# Phase 4: Images and Cleanup

**Plan:** [README.md](./README.md)
**Type:** sequential

## Progress

| Status  | Task |
| ------- | ---- |
| ⬜ TODO | Reduce image variants |
| ⬜ TODO | Remove leftovers |

## Tasks

1. Reduce responsive image variant generation for large content images while preserving lazy loading and lightgallery behavior.
   - Files: `layouts/_partials/plugin/img.html`, `themes/LoveIt/layouts/_partials/plugin/img.html`
   - Verify: render pages with large and small images, confirm the markup still works, and compare processed-image counts plus total build time.

2. Re-audit any remaining global scripts and styles after the earlier phases and remove leftovers that are still loaded everywhere without a measurable benefit.
   - Files: `layouts/_partials/assets-default.html`, `themes/LoveIt/layouts/_partials/assets.html`
   - Verify: inspect generated HTML for home, posts, cheatsheets, and listen pages to ensure no dead global asset tags remain.

