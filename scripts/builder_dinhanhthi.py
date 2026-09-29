import json
import os
import html

os.makedirs("static/diagrams", exist_ok=True)

THEMES = {
    "light": {
        "bg": "#ffffff",
        "primary_fill": "#ffffff",
        "primary_stroke": "#18181b",
        "secondary_fill": "#f4f6f8",
        "secondary_stroke": "#e2e8f0",
        "text_primary": "#18181b",
        "text_secondary": "#64748b",
        "arrow_main": "#18181b",
        "arrow_secondary": "#64748b",
        "arrow_accent": "#2563eb",
        "font_mono": 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "IBM Plex Mono", monospace'
    },
    "dark": {
        "bg": "#18181b",
        "primary_fill": "#27272a",
        "primary_stroke": "#fafafa",
        "secondary_fill": "#1f1f23",
        "secondary_stroke": "#3f3f46",
        "text_primary": "#fafafa",
        "text_secondary": "#a1a1aa",
        "arrow_main": "#fafafa",
        "arrow_secondary": "#a1a1aa",
        "arrow_accent": "#60a5fa",
        "font_mono": 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "IBM Plex Mono", monospace'
    }
}

def clean_txt(t):
    if not t: return ""
    return html.escape(str(t).strip().replace('&quot;', '"').replace('&amp;', 'và').replace('&', 'và'))

class DinhanhthiStyleSvgBuilder:
    def __init__(self, mode="light"):
        self.mode = mode
        self.c = THEMES[mode]

    def render_diagram(self, width, height, nodes, edges):
        c = self.c
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background-color: {c["bg"]}; border-radius: 8px;">']
        svg.append(f'''
  <defs>
    <marker id="arr-main-{self.mode}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="{c["arrow_main"]}"/>
    </marker>
    <marker id="arr-sec-{self.mode}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="{c["arrow_secondary"]}"/>
    </marker>
    <marker id="arr-acc-{self.mode}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto-start-reverse">
      <polygon points="0 0, 8 3, 0 6" fill="{c["arrow_accent"]}"/>
    </marker>
  </defs>
  <style>
    text {{ font-family: {c["font_mono"]}; }}
    .nm {{ font-size: 13px; font-weight: 600; fill: {c["text_primary"]}; }}
    .dt {{ font-size: 11px; fill: {c["text_secondary"]}; }}
    .al {{ font-size: 11px; fill: {c["text_secondary"]}; }}
  </style>
''')
        # Draw background
        svg.append(f'  <rect width="{width}" height="{height}" fill="{c["bg"]}"/>')

        # Draw edges
        for e in edges:
            d = e["d"]
            kind = e.get("kind", "main") # main, secondary, accent, accent_bidirectional
            label = e.get("label", "")
            lbl_pos = e.get("label_pos", None)
            
            stroke_color = c["arrow_main"] if kind == "main" else (c["arrow_accent"] if "accent" in kind else c["arrow_secondary"])
            marker_str = f'marker-end="url(#arr-main-{self.mode})"' if kind == "main" else (
                f'marker-start="url(#arr-acc-{self.mode})" marker-end="url(#arr-acc-{self.mode})"' if kind == "accent_bidirectional" else (
                    f'marker-end="url(#arr-acc-{self.mode})"' if kind == "accent" else f'marker-end="url(#arr-sec-{self.mode})"'
                )
            )
            dash_str = 'stroke-dasharray="4 3"' if ("dash" in e or kind != "main") else ""
            width_str = 'stroke-width="1.5"'
            
            svg.append(f'  <path d="{d}" fill="none" stroke="{stroke_color}" {width_str} {dash_str} {marker_str} />')
            
            if label and lbl_pos:
                lx, ly = lbl_pos
                align = e.get("align", "middle")
                svg.append(f'  <text x="{lx}" y="{ly}" text-anchor="{align}" class="al">{clean_txt(label)}</text>')

        # Draw nodes
        for n in nodes:
            x, y, w, h = n["x"], n["y"], n["w"], n["h"]
            is_primary = n.get("is_primary", False)
            fill_color = c["primary_fill"] if is_primary else c["secondary_fill"]
            stroke_color = c["primary_stroke"] if is_primary else c["secondary_stroke"]
            stroke_w = "1.5" if is_primary else "1.2"
            
            svg.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill_color}" stroke="{stroke_color}" stroke-width="{stroke_w}" />')
            
            title = clean_txt(n.get("title", ""))
            sub = clean_txt(n.get("sub", ""))
            
            if sub:
                svg.append(f'  <text x="{x + 14}" y="{y + 26}" class="nm">{title}</text>')
                svg.append(f'  <text x="{x + 14}" y="{y + 44}" class="dt">{sub}</text>')
            else:
                svg.append(f'  <text x="{x + 14}" y="{y + 35}" class="nm">{title}</text>')

        svg.append('</svg>')
        return "\n".join(svg)

print("DinhanhthiStyleSvgBuilder initialized.")
