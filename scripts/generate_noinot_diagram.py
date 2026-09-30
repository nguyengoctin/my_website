import json
import subprocess
import os
import re

data = {
  "schema_version": 1,
  "mode": "architecture",
  "template_type": "architecture",
  "style": 4,
  "width": 960,
  "height": 720,
  "title": "Nối Nốt: Kiến Trúc Nền Tảng Context Chung",
  "subtitle": "Mô hình phân tầng từ Core Apps, Domain Apps đến Shared Context Layer",
  "containers": [
    {
      "id": "core_apps",
      "x": 40,
      "y": 100,
      "width": 880,
      "height": 130,
      "label": "CORE APPS (TẦNG ỨNG DỤNG NỀN TẢNG)"
    },
    {
      "id": "domain_apps",
      "x": 40,
      "y": 280,
      "width": 880,
      "height": 130,
      "label": "DOMAIN APPS VÀ TOOLS (TẦNG ỨNG DỤNG CHUYÊN BIỆT)"
    },
    {
      "id": "context_layer",
      "x": 40,
      "y": 460,
      "width": 880,
      "height": 140,
      "label": "SHARED CONTEXT LAYER (TẦNG NGỮ CẢNH HỢP NHẤT)"
    }
  ],
  "nodes": [
    {
      "id": "inbox", "kind": "rect", "x": 60, "y": 140, "width": 170, "height": 66,
      "type_label": "CAPTURE", "label": "Inbox", "sublabel": "Tiếp nhận thông tin"
    },
    {
      "id": "today", "kind": "rect", "x": 280, "y": 140, "width": 170, "height": 66,
      "type_label": "VIEW", "label": "Today và Focus", "sublabel": "Hội tụ trong ngày"
    },
    {
      "id": "tasks_cal", "kind": "rect", "x": 500, "y": 140, "width": 170, "height": 66,
      "type_label": "SCHEDULE", "label": "Tasks và Calendar", "sublabel": "Hành động và tiến độ"
    },
    {
      "id": "search_act", "kind": "rect", "x": 720, "y": 140, "width": 170, "height": 66,
      "type_label": "AUDIT", "label": "Search và Activity", "sublabel": "Tra cứu và nhật ký"
    },
    {
      "id": "contacts", "kind": "rect", "x": 60, "y": 320, "width": 170, "height": 66,
      "type_label": "DOMAIN", "label": "Contacts và Org", "sublabel": "Con người và quan hệ"
    },
    {
      "id": "finance", "kind": "rect", "x": 280, "y": 320, "width": 170, "height": 66,
      "type_label": "DOMAIN", "label": "Finance và Budget", "sublabel": "Giao dịch và tài sản"
    },
    {
      "id": "health", "kind": "rect", "x": 500, "y": 320, "width": 170, "height": 66,
      "type_label": "DOMAIN", "label": "Health và Care", "sublabel": "Hồ sơ và lịch khám"
    },
    {
      "id": "projects", "kind": "rect", "x": 720, "y": 320, "width": 170, "height": 66,
      "type_label": "DOMAIN", "label": "Projects và Tools", "sublabel": "Mục tiêu và tài liệu"
    },
    {
      "id": "entities", "kind": "rect", "x": 60, "y": 500, "width": 170, "height": 76,
      "type_label": "PRIMITIVE", "label": "Entities và Items", "sublabel": "Định danh thực thể"
    },
    {
      "id": "relationships", "kind": "rect", "x": 280, "y": 500, "width": 170, "height": 76,
      "type_label": "GRAPH", "label": "Relationships", "sublabel": "Cạnh nối ngữ nghĩa"
    },
    {
      "id": "events", "kind": "rect", "x": 500, "y": 500, "width": 170, "height": 76,
      "type_label": "MUTATION", "label": "Events và Actions", "sublabel": "Biến động trạng thái"
    },
    {
      "id": "time_sync", "kind": "rect", "x": 720, "y": 500, "width": 170, "height": 76,
      "type_label": "FOUNDATION", "label": "Time và Resources", "sublabel": "Trục thời gian chung"
    }
  ],
  "arrows": [
    { "id": "a1", "source": "inbox", "target": "contacts", "source_port": "bottom", "target_port": "top", "label": "phân bổ" },
    { "id": "a2", "source": "today", "target": "finance", "source_port": "bottom", "target_port": "top", "label": "theo dõi" },
    { "id": "a3", "source": "tasks_cal", "target": "health", "source_port": "bottom", "target_port": "top", "label": "nhắc lịch" },
    { "id": "a4", "source": "search_act", "target": "projects", "source_port": "bottom", "target_port": "top", "label": "truy xuất" },
    { "id": "a5", "source": "contacts", "target": "entities", "source_port": "bottom", "target_port": "top", "label": "gắn thực thể" },
    { "id": "a6", "source": "finance", "target": "relationships", "source_port": "bottom", "target_port": "top", "label": "nối ngữ cảnh" },
    { "id": "a7", "source": "health", "target": "events", "source_port": "bottom", "target_port": "top", "label": "lưu sự kiện" },
    { "id": "a8", "source": "projects", "target": "time_sync", "source_port": "bottom", "target_port": "top", "label": "đồng bộ mốc" }
  ],
  "legend_orientation": "horizontal",
  "legend_x": 48,
  "legend_y": 635,
  "legend_locked": True,
  "legend": [
    { "flow": "read", "label": "luồng điều phối / truy vấn" },
    { "flow": "write", "label": "đồng bộ ngữ cảnh chung" }
  ],
  "footer": "Nối Nốt Platform Architecture · Style 4 Notion Clean",
  "footer_x": 48,
  "footer_y": 690
}

os.makedirs("static/diagrams", exist_ok=True)
json_path = "/tmp/noinot-style4-prod.json"
light_svg_path = "static/diagrams/noi-not-shared-context-platform-1.svg"
dark_svg_path = "static/diagrams/noi-not-shared-context-platform-1-dark.svg"

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

print("Dual-theme SVGs generated successfully.")
