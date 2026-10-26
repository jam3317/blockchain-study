"""시퀀스 다이어그램 PNG 생성기.

사용법:  python3 tools/make_diagram.py <spec.json> <out.png>

spec.json 예시:
{
  "title": "getAddress",                       # 제목 (코드 글꼴, 파란색)
  "subtitle": "test.js가 ... 채점한다.",
  "lanes": [["test.js", "출제 · 채점", "blue"], ["getAddress.js", "내가 작성", "orange"], ...],
  "active": 1,                                 # 노란 막대를 그릴 lane 번호 (없으면 null)
  "sections": [
    {"title": "getAddress 실행", "color": "orange", "steps": [
        ["call", 0, 1, "getAddress(publicKey)", "65바이트 공개키"],
        ["ret", 1, 0, "return 주소", "16bb6031…9705 (20바이트)"],
        ["self", 0, "toHex(주소) === 정답 ?", "✔ 같음 → 통과"],
        ["note", 1, "for 반복 · nonce++", "설명"]          # lane 옆에 글 상자
    ], "active": true}                         # 이 섹션 동안 노란 막대 표시
  ],
  "footer": "function getAddress(publicKey) { ... }"
}
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MONO = "'SF Mono','Menlo',monospace"
SANS = "'Pretendard','Pretendard Variable',sans-serif"

PALETTE = {  # 이름: (선 색, 배경색)
    "blue": ("#4f46e5", "#eef0fe"),
    "orange": ("#b45309", "#fff8e8"),
    "pink": ("#be185d", "#fdf0f6"),
    "teal": ("#0f766e", "#eefaf7"),
    "gray": ("#374151", "#f3f4f6"),
    "purple": ("#7c3aed", "#f5f0ff"),
    "green": ("#15803d", "#effaf2"),
}
SECTION = {
    "orange": ("#d97706", "#fffaf0"),
    "pink": ("#be185d", "#fdf4f8"),
    "gray": ("#4b5563", "#f6f7f9"),
    "green": ("#16a34a", "#f0f9f3"),
    "blue": ("#4f46e5", "#f5f5ff"),
    "teal": ("#0f766e", "#f0faf8"),
    "purple": ("#7c3aed", "#f8f5ff"),
}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(spec):
    W = 1600
    lanes = spec["lanes"]
    n = len(lanes)
    left, right = 230, W - 210
    LX = [left + (right - left) * i / max(n - 1, 1) for i in range(n)]
    box_w = min(230, (right - left) / max(n - 1, 1) - 30) if n > 1 else 230

    svg, sec_svg, act = [], [], []
    y = 330
    STEP = 70
    counter = [0]

    def badge(x, yy, dark=True):
        counter[0] += 1
        num = counter[0]
        fill = "#111827" if dark else "#9ca3af"
        svg.append(f'<circle cx="{x}" cy="{yy}" r="13" fill="{fill}"/>'
                   f'<text x="{x}" y="{yy+4.5}" font-size="12" font-weight="700" fill="#fff" '
                   f'text-anchor="middle" font-family="{SANS}">{num}</text>')

    def arrow(a, b, label, sub, dashed):
        nonlocal y
        x1, x2 = LX[a], LX[b]
        d = 1 if x2 > x1 else -1
        sx = x1 + 8 * d
        ex = x2 - 8 * d
        color = "#6b7280" if dashed else "#111827"
        dash = ' stroke-dasharray="7 6"' if dashed else ""
        svg.append(f'<line x1="{sx}" y1="{y}" x2="{ex - 16*d}" y2="{y}" stroke="{color}" stroke-width="2"{dash}/>')
        svg.append(f'<polygon points="{ex},{y} {ex-16*d},{y-8} {ex-16*d},{y+8}" fill="{color}"/>')
        tx = min(x1, x2) + (30 if dashed else 18)
        weight = "400" if dashed else "700"
        tcolor = "#374151" if dashed else "#111827"
        svg.append(f'<text x="{tx}" y="{y-12}" font-size="15" font-weight="{weight}" fill="{tcolor}" font-family="{MONO}">{esc(label)}</text>')
        if sub:
            svg.append(f'<text x="{tx}" y="{y+22}" font-size="13" fill="#9a3412" font-family="{MONO}">{esc(sub)}</text>')
        if dashed:
            badge(x1 + 34 * (-d), y, dark=False)
        else:
            badge(x1 - 34 * d, y)
        y += STEP

    def self_check(a, label, sub):
        nonlocal y
        x = LX[a]
        svg.append(f'<path d="M{x} {y-14} H{x+60} V{y+14} H{x+16}" fill="none" stroke="#16a34a" stroke-width="2"/>')
        svg.append(f'<polygon points="{x+2},{y+14} {x+18},{y+6} {x+18},{y+22}" fill="#16a34a"/>')
        svg.append(f'<text x="{x+76}" y="{y}" font-size="15" font-weight="700" fill="#111827" font-family="{MONO}">{esc(label)}</text>')
        if sub:
            svg.append(f'<text x="{x+76}" y="{y+20}" font-size="13" font-weight="700" fill="#16a34a" font-family="{MONO}">{esc(sub)}</text>')
        badge(x - 34, y - 14)
        y += STEP

    def note(a, label, sub):
        nonlocal y
        x = LX[a] + 22
        lines = [label] + ([sub] if sub else [])
        width = max(len(s) for s in lines) * 9 + 40
        h = 26 + 22 * len(lines)
        svg.append(f'<rect x="{x}" y="{y-22}" width="{width}" height="{h}" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-dasharray="4 3"/>')
        svg.append(f'<text x="{x+16}" y="{y}" font-size="14" font-weight="700" fill="#92400e" font-family="{MONO}">{esc(label)}</text>')
        if sub:
            svg.append(f'<text x="{x+16}" y="{y+22}" font-size="13" fill="#92400e" font-family="{SANS}">{esc(sub)}</text>')
        y += h + 24

    sections = []
    for sec in spec["sections"]:
        top = y - 66
        start = None
        for i, st in enumerate(sec["steps"]):
            kind = st[0]
            if i == 0 and sec.get("active"):
                start = y - 2
            if kind == "call":
                arrow(st[1], st[2], st[3], st[4] if len(st) > 4 else "", False)
            elif kind == "ret":
                arrow(st[1], st[2], st[3], st[4] if len(st) > 4 else "", True)
            elif kind == "self":
                self_check(st[1], st[2], st[3] if len(st) > 3 else "")
            elif kind == "note":
                note(st[1], st[2], st[3] if len(st) > 3 else "")
        if start is not None and spec.get("active") is not None:
            act.append((start, y - 50))
        bottom = y - 30
        c, bg = SECTION.get(sec.get("color", "gray"), SECTION["gray"])
        sec_svg.append(f'<rect x="60" y="{top}" width="{W-120}" height="{bottom-top}" rx="14" fill="{bg}" stroke="{c}" stroke-opacity=".45" stroke-dasharray="6 5"/>')
        sec_svg.append(f'<text x="80" y="{top+26}" font-size="15" font-weight="700" fill="{c}" font-family="{SANS}">{esc(sec["title"])}</text>')
        y += 58

    content_bottom = y - 30
    H = content_bottom + (140 if spec.get("footer") else 100)

    lines = []
    hdr = []
    for i, (name, sub, color) in enumerate(lanes):
        stroke, bg = PALETTE.get(color, PALETTE["gray"])
        x = LX[i]
        lines.append(f'<line x1="{x}" y1="250" x2="{x}" y2="{content_bottom}" stroke="{stroke}" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="3 5"/>')
        fs = 19 if len(name) <= 16 else 16
        hdr.append(f'<rect x="{x-box_w/2}" y="180" width="{box_w}" height="68" rx="10" fill="{bg}" stroke="{stroke}" stroke-width="2.2"/>')
        hdr.append(f'<text x="{x}" y="212" font-size="{fs}" font-weight="700" fill="{stroke}" text-anchor="middle" font-family="{MONO}">{esc(name)}</text>')
        hdr.append(f'<text x="{x}" y="236" font-size="13" fill="#4b5563" text-anchor="middle" font-family="{SANS}">{esc(sub)}</text>')

    a_svg = []
    if spec.get("active") is not None:
        ax = LX[spec["active"]]
        for a0, a1 in act:
            a_svg.append(f'<rect x="{ax-7}" y="{a0}" width="14" height="{max(a1-a0, 10)}" rx="4" fill="#fde68a" stroke="#d97706" stroke-width="1.2"/>')

    ly = content_bottom + 40
    active_name = spec.get("active_label") or (lanes[spec["active"]][0].replace(".js", "").replace(".sol", "") if spec.get("active") is not None else "")
    legend = f'''
<line x1="60" y1="{ly}" x2="110" y2="{ly}" stroke="#111827" stroke-width="2"/><polygon points="126,{ly} 110,{ly-8} 110,{ly+8}" fill="#111827"/>
<text x="138" y="{ly+5}" font-size="14" fill="#374151" font-family="{SANS}">함수 호출</text>
<line x1="250" y1="{ly}" x2="300" y2="{ly}" stroke="#6b7280" stroke-width="2" stroke-dasharray="7 6"/><polygon points="316,{ly} 300,{ly-8} 300,{ly+8}" fill="#6b7280"/>
<text x="328" y="{ly+5}" font-size="14" fill="#374151" font-family="{SANS}">return (돌려받는 값)</text>'''
    if active_name:
        legend += f'''
<rect x="510" y="{ly-11}" width="14" height="22" rx="4" fill="#fde68a" stroke="#d97706"/>
<text x="536" y="{ly+5}" font-size="14" fill="#374151" font-family="{SANS}">{esc(active_name)}가 실행 중인 구간</text>'''
    if spec.get("footer"):
        legend += f'\n<text x="60" y="{ly+50}" font-size="13" fill="#6b7280" font-family="{MONO}">{esc(spec["footer"])}</text>'

    title = spec["title"]
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#f4f5f8}}</style></head><body>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#f4f5f8"/>
<text x="60" y="78" font-size="38" font-weight="800" font-family="{MONO}" fill="#4f46e5">{esc(title)}<tspan fill="#111827" font-family="{SANS}"> 코드 흐름</tspan></text>
<text x="60" y="118" font-size="16" fill="#4b5563" font-family="{SANS}">{esc(spec.get("subtitle", ""))}</text>
<rect x="40" y="150" width="{W-80}" height="{H-180}" rx="22" fill="#fff" stroke="#e5e7eb"/>
{"".join(sec_svg)}{"".join(lines)}{"".join(hdr)}{"".join(a_svg)}{"".join(svg)}{legend}
</svg></body></html>'''
    return html, W, H


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2]).resolve()
    html, W, H = build(spec)
    with tempfile.TemporaryDirectory() as d:
        page = Path(d) / "diagram.html"
        page.write_text(html)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", f"--window-size={W},{H}",
                        f"--screenshot={out}", page.as_uri()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(out, W * 2, H * 2)


if __name__ == "__main__":
    main()
