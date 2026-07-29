# Project Rules for Blog Writing

## Tone and Style (Huyen Chip "We" Mindset)
- Always write using inclusive "chúng ta" (we = writer + reader together as learning partners).
- Avoid preachy or distant tone.

## Conciseness & Information Density (Pham Huy Hoang Rule)
- "Nếu bạn có thể nói một vấn đề trong vòng một đoạn văn thì đừng nên dùng một trang A4 để giải thích cái vấn đề đó."
- Eliminate redundant introductions, intros, outros, and repeated explanations.
- Maximize information density using tables, lists, LaTeX formulas, and diagrams.

## Language Rule: No Inline Parenthetical Translations
- NEVER use parentheses `()` to translate terms inline (e.g. NEVER write `Spec-Driven Development (Phát triển dựa trên đặc tả)` or `hallucination (ảo giác)`).
- Use natural Vietnamese phrasing OR keep the English technical term cleanly without parenthetical translations.

## Prompt Formatting
- Always use the custom `prompt` shortcode:
  `{{< prompt title="Prompt Mẫu: [Title]" >}} Content... {{< /prompt >}}`
- Do NOT use double quotes `"..."`, code blocks ` ``` `, or blockquotes `>` inside prompt shortcodes.

## Quotes Formatting
- Format quotes using Markdown blockquote syntax: `> *"Quote text"* — **Author Name**`

## Mermaid Diagram Syntax
- Use standard fenced code block ```mermaid ... ```.
- Quote node labels containing numbers (e.g. `Step1["Bước 1: Text"]`) to avoid `Unsupported markdown: list` syntax errors.
