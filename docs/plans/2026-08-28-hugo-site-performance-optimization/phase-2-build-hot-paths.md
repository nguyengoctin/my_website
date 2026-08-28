# Phase 2: Build Hot Paths

**Plan:** [README.md](./README.md)
**Type:** sequential

## Progress

| Status  | Task |
| ------- | ---- |
| ⬜ TODO | Short-circuit content transforms |
| ⬜ TODO | Remove syntax-guessing overhead |

## Tasks

1. Short-circuit the expensive content transform regexes so ruby, fraction, fontawesome, checkbox, and escape replacements only run when the input actually contains the relevant markers.
   - Files: `themes/LoveIt/layouts/_partials/function/content.html`, `themes/LoveIt/layouts/_partials/function/ruby.html`, `themes/LoveIt/layouts/_partials/function/fraction.html`, `themes/LoveIt/layouts/_partials/function/fontawesome.html`, `themes/LoveIt/layouts/_partials/function/checkbox.html`, `themes/LoveIt/layouts/_partials/function/escape.html`
   - Verify: rebuild and compare pages with and without the special markers; confirm unchanged output and lower cumulative time in `_partials/function/content.html`.

2. Inventory untyped code fences, annotate the small set that rely on fallback detection, and then disable `markup.highlight.guessSyntax`.
   - Files: `hugo.toml`, selected `content/**/*.md`
   - Verify: code-heavy pages still render correctly, and Hugo template metrics for code rendering improve without introducing broken highlighting.

