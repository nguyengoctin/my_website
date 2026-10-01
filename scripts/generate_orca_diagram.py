import json
import subprocess
import os
import re

# Data definition for Orca Architecture & Workflow
data = {
  "schema_version": 1,
  "mode": "architecture",
  "template_type": "architecture",
  "style": 4,
  "width": 960,
  "height": 620,
  "title": "Kiến Trúc Orca: Agent Development Environment (ADE)",
  "subtitle": "Mô hình vận hành song song đa Agent trên từng Git Worktree độc lập",
  "containers": [
    {
      "id": "orchestration_layer",
      "x": 40,
      "y": 100,
      "width": 880,
      "height": 130,
      "label": "ORCHESTRATION & ENVIRONMENT (ORCA DESKTOP CORE)"
    },
    {
      "id": "worktree_layer",
      "x": 40,
      "y": 270,
      "width": 880,
      "height": 140,
      "label": "PARALLEL WORKTREES & CLI AGENTS (CÔ LẬP KHÔNG GIAN LÀM VIỆC)"
    },
    {
      "id": "feedback_layer",
      "x": 40,
      "y": 450,
      "width": 880,
      "height": 130,
      "label": "FEEDBACK & SHIP (ĐÁNH GIÁ, THỰC THI VÀ HOÀN TẤT)"
    }
  ],
  "nodes": [
    {
      "id": "orca_core", "kind": "rect", "x": 60, "y": 140, "width": 180, "height": 66,
      "type_label": "CORE", "label": "Orca ADE App", "sublabel": "Desktop / Remote SSH"
    },
    {
      "id": "worktree_mgr", "kind": "rect", "x": 280, "y": 140, "width": 180, "height": 66,
      "type_label": "STORAGE", "label": "Worktree Manager", "sublabel": "Tự động phân nhánh Git"
    },
    {
      "id": "terminal_mux", "kind": "rect", "x": 500, "y": 140, "width": 180, "height": 66,
      "type_label": "TERMINAL", "label": "Ghostty Terminal", "sublabel": "Infinite Split Panes"
    },
    {
      "id": "embedded_browser", "kind": "rect", "x": 720, "y": 140, "width": 180, "height": 66,
      "type_label": "BROWSER", "label": "Per-tree Browser", "sublabel": "Design Mode và View"
    },
    {
      "id": "wt_agent_1", "kind": "rect", "x": 60, "y": 310, "width": 260, "height": 72,
      "type_label": "WORKTREE A", "label": "Worktree: Auth Flow", "sublabel": "Claude Code (Refactor Token)"
    },
    {
      "id": "wt_agent_2", "kind": "rect", "x": 350, "y": 310, "width": 260, "height": 72,
      "type_label": "WORKTREE B", "label": "Worktree: API Cache", "sublabel": "Codex CLI (Redis Optimization)"
    },
    {
      "id": "wt_agent_3", "kind": "rect", "x": 640, "y": 310, "width": 260, "height": 72,
      "type_label": "WORKTREE C", "label": "Worktree: UI Fix", "sublabel": "Cursor CLI (Responsive Layout)"
    },
    {
      "id": "diff_review", "kind": "rect", "x": 100, "y": 490, "width": 220, "height": 66,
      "type_label": "REVIEW", "label": "AI Diff Reviewer", "sublabel": "Annotate & AI fix"
    },
    {
      "id": "test_verify", "kind": "rect", "x": 370, "y": 490, "width": 220, "height": 66,
      "type_label": "VERIFY", "label": "CI / Local Checks", "sublabel": "Build và Run Tests"
    },
    {
      "id": "git_ship", "kind": "rect", "x": 640, "y": 490, "width": 220, "height": 66,
      "type_label": "MERGE", "label": "Clean Commit & PR", "sublabel": "Merge vào Main Branch"
    }
  ],
  "edges": [
    {"from": "worktree_mgr", "to": "wt_agent_1"},
    {"from": "worktree_mgr", "to": "wt_agent_2"},
    {"from": "worktree_mgr", "to": "wt_agent_3"},
    {"from": "wt_agent_1", "to": "diff_review"},
    {"from": "wt_agent_2", "to": "diff_review"},
    {"from": "wt_agent_3", "to": "diff_review"},
    {"from": "diff_review", "to": "test_verify"},
    {"from": "test_verify", "to": "git_ship"}
  ]
}

os.makedirs("scratch", exist_ok=True)
json_path = "scratch/orca_diagram.json"
light_svg_path = "static/diagrams/orca-architecture.svg"
dark_svg_path = "static/diagrams/orca-architecture-dark.svg"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

subprocess.run([
    "python3",
    ".agents/skills/fireworks-tech-graph/scripts/fireworks.py",
    "render",
    "architecture",
    json_path,
    light_svg_path
], check=True)

with open(light_svg_path, "r", encoding="utf-8") as f:
    svg = f.read()

# Build dark version
dark_svg = svg
dark_svg = dark_svg.replace('fill="#ffffff"', 'fill="#18181b"')
dark_styles = """
    text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, 'PingFang SC', 'Noto Sans CJK SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .title { font-size: 18px; font-weight: 700; fill: #fafafa; }
    .subtitle { font-size: 13px; font-weight: 500; fill: #a1a1aa; }
    .section { font-size: 13px; font-weight: 700; fill: #9ca3af; letter-spacing: 1.4px; }
    .section-sub { font-size: 12px; font-weight: 500; fill: #9ca3af; }
    .node-title { font-weight: 700; fill: #fafafa; }
    .node-sub { font-weight: 500; fill: #d1d5db; }
    .node-type { font-size: 11px; font-weight: 700; fill: #9ca3af; letter-spacing: 0.08em; }
    .arrow-label { font-size: 12px; font-weight: 600; fill: #9ca3af; }
    .legend { font-size: 12px; font-weight: 500; fill: #9ca3af; }
    .footnote { font-size: 12px; font-weight: 500; fill: #71717a; }
    .metric-label { font-size: 8.5px; font-weight: 700; fill: #a1a1aa; text-transform: uppercase; }
    .metric-value { font-size: 9.5px; font-weight: 700; fill: #fafafa; }
"""
dark_svg = re.sub(r"<style>.*?</style>", f"<style>{dark_styles}</style>", dark_svg, flags=re.DOTALL)
dark_svg = dark_svg.replace('stroke="#e5e7eb"', 'stroke="#27272a"')
dark_svg = dark_svg.replace('fill="#f9fafb" stroke="#e5e7eb"', 'fill="#27272a" stroke="#3f3f46"')
dark_svg = dark_svg.replace('fill="#3b82f6"', 'fill="#60a5fa"')
dark_svg = dark_svg.replace('stroke="#3b82f6"', 'stroke="#60a5fa"')

with open(dark_svg_path, "w", encoding="utf-8") as f:
    f.write(dark_svg)

print("Orca Dual-theme SVGs generated successfully.")
