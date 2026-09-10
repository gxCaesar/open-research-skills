#!/usr/bin/env python3
"""Draw the one-picture map of the ten skills, for the top of both READMEs.

WHY A GENERATOR. A hand-drawn diagram naming ten skills is a copy of skill-index.json that
nothing keeps honest: rename or add a skill and the picture is quietly wrong, which is worse
than having no picture, because a reader trusts it. So the names come from the index, and
tests/test_overview_diagram.py fails when this file's captions and the index disagree.

WHY SVG AND NOT THE VISUALISATION SKILL. That skill's default route ends in an editable
PPTX built from a generated concept, which is the right shape for a manuscript figure and
the wrong one for a README: this needs to scale to any width, stay small, diff line by line,
render in GitHub's light and dark themes, and be checkable against a JSON file.

WHY PRESENTATION ATTRIBUTES AND NO <style>. GitHub sanitises SVG it renders in Markdown and
drops <style> and <script>. A stylesheet-driven diagram looks right locally and arrives
unstyled, so every colour and font here is an attribute on its own element.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "skill-index.json"
OUT = ROOT / "assets" / "overview"

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', "
        "'Hiragino Sans GB', 'Microsoft YaHei', Roboto, sans-serif")

THEMES = {
    "light": dict(bg="#ffffff", card="#f6f8fa", edge="#d0d7de", ink="#1f2328",
                  mute="#59636e", rail="#ddf4ff", railedge="#54aeff", railink="#0550ae",
                  spine="#8250df", dot="#ffffff", side="#fff8c5", sideedge="#d4a72c"),
    "dark": dict(bg="#0d1117", card="#161b22", edge="#30363d", ink="#e6edf3",
                 mute="#9198a1", rail="#121d2f", railedge="#1f6feb", railink="#79c0ff",
                 spine="#a371f7", dot="#0d1117", side="#272115", sideedge="#9e6a03"),
}

W, H = 1280, 546

# The five stages of the spine, and which skill sits on each. Every name here is checked
# against skill-index.json; the captions are the only hand-written part.
STAGES = [
    dict(x=160, zh="选题", en="Direction",
         skills=[("survey-and-audit-novelty", "方向还开着吗？变量是否共存",
                                              "Is this direction still open?")]),
    dict(x=400, zh="方法", en="Method",
         skills=[("develop-method-to-sota", "打不过基线时，下一步改哪里",
                                            "Losing to the baseline: what next")]),
    dict(x=640, zh="成稿", en="Manuscript",
         skills=[("prepare-conference-manuscripts", "顶会：成稿、rebuttal、终稿",
                                                   "Conferences: draft to camera-ready"),
                 ("prepare-journal-manuscripts", "期刊：Nature-family 组织与投稿",
                                                 "Journals: Nature-family submission")]),
    dict(x=880, zh="投前", en="Before submitting",
         skills=[("run-cold-review-panel", "先让没看过项目的评审挑一遍",
                                           "A hostile read before submitting")]),
    dict(x=1120, zh="发布", en="Release",
         skills=[("release-research-artifacts", "别人真能下载并跑通的那个包",
                                                "A package a reader can run")]),
]

RAILS = [
    ("research-publication-pipeline", "贯穿全程 · 从选题到可复现发布的编排",
                                      "Across the whole arc: topic to reproducible release"),
    ("build-scientific-visualizations", "贯穿全程 · 架构图、多面板图、可编辑矢量成品",
                                        "Across the whole arc: diagrams, panels, editable vector"),
]

SIDE = [
    ("writing-funding-proposals", "基金 proposal 撰写", "Research funding proposals"),
    ("review-others-manuscripts", "受邀审别人的投稿", "Refereeing someone else's submission"),
]

TITLE = {"zh": "十个可独立安装的科研 skill —— 按你这次要交付的东西选一个",
         "en": "Ten independently installable research skills — pick by what you owe this week"}
FOOT = {"zh": "每个都能单独安装、独立使用，没有强制顺序。",
        "en": "Each installs and runs on its own. There is no required order."}
SIDE_LABEL = {"zh": "另外两条独立入口", "en": "Two further standalone entry points"}


def est_width(s: str, size: float, mono: bool = False) -> float:
    """Rough advance width. CJK is one em, monospace 0.60 em, Latin body about 0.52 em."""
    per = 0.60 if mono else 0.52
    return sum(size if ord(c) > 0x2E7F else size * per for c in s)


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, *, size, fill, weight="400", anchor="start", mono=False):
    family = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" if mono else FONT
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


def box(x, y, w, h, fill, stroke, r=10):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>')


def render(theme_name: str, lang: str) -> str:
    t = THEMES[theme_name]
    zh = lang == "zh"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" role="img" aria-label="{esc(TITLE[lang])}">',
           f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>']

    out.append(text(40, 46, TITLE[lang], size=21, fill=t["ink"], weight="600"))

    # Two rails, one above the spine and one below, because both skills apply at every stage.
    for i, (name, cz, ce) in enumerate(RAILS):
        y = 72 if i == 0 else 372
        out.append(box(40, y, W - 80, 46, t["rail"], t["railedge"], r=8))
        out.append(text(58, y + 21, name, size=15, fill=t["railink"], weight="600", mono=True))
        out.append(text(58, y + 38, cz if zh else ce, size=13, fill=t["mute"]))

    # The spine.
    spine_y = 192
    out.append(f'<line x1="60" y1="{spine_y}" x2="{W - 74}" y2="{spine_y}" '
               f'stroke="{t["spine"]}" stroke-width="2.5" stroke-linecap="round"/>')
    out.append(f'<path d="M {W - 74} {spine_y - 7} L {W - 52} {spine_y} L {W - 74} {spine_y + 7} Z" '
               f'fill="{t["spine"]}"/>')

    for stage in STAGES:
        x = stage["x"]
        out.append(f'<circle cx="{x}" cy="{spine_y}" r="7" fill="{t["dot"]}" '
                   f'stroke="{t["spine"]}" stroke-width="2.5"/>')
        out.append(text(x, spine_y - 20, stage["zh"] if zh else stage["en"],
                        size=15, fill=t["spine"], weight="600", anchor="middle"))
        top = spine_y + 24
        for skill_name, cz, ce in stage["skills"]:
            out.append(box(x - 112, top, 224, 60, t["card"], t["edge"]))
            out.append(text(x, top + 24, skill_name, size=11, fill=t["ink"],
                            weight="600", anchor="middle", mono=True))
            out.append(text(x, top + 44, cz if zh else ce, size=11,
                            fill=t["mute"], anchor="middle"))
            top += 70

    # Funding and refereeing are real research work that does not sit on this arc at all,
    # so they are drawn off it rather than forced onto a stage they do not belong to.
    y = 456
    out.append(text(40, y + 4, SIDE_LABEL[lang], size=13, fill=t["mute"], weight="600"))
    x = 40 + (146 if zh else 250)
    for name, cz, ce in SIDE:
        cap = cz if zh else ce
        # Monospace runs about 0.60 em, CJK a full em, Latin body text about 0.52 em.
        width = int(len(name) * 6.9 + len(cap) * (13.0 if zh else 6.4) + 44)
        out.append(box(x, y - 17, width, 32, t["side"], t["sideedge"], r=8))
        out.append(text(x + 15, y + 4, name, size=11.5, fill=t["ink"], weight="600", mono=True))
        out.append(text(x + 15 + len(name) * 6.9 + 13, y + 4, cap, size=12, fill=t["mute"]))
        x += width + 18

    out.append(text(40, 508, FOOT[lang], size=12.5, fill=t["mute"]))
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    declared = {s["name"] for s in json.loads(INDEX.read_text(encoding="utf-8"))["skills"]}
    drawn = ({n for st in STAGES for n, _, _ in st["skills"]}
             | {n for n, _, _ in RAILS} | {n for n, _, _ in SIDE})
    # Refuse rather than emit a diagram that disagrees with the index it claims to summarise.
    if drawn != declared:
        print(f"FAIL diagram/index disagree: only-in-diagram={sorted(drawn - declared)} "
              f"only-in-index={sorted(declared - drawn)}")
        return 1

    # A caption that overflows its card looks like a rendering bug to a reader and is
    # invisible to whoever edits the text. Measure it here rather than after the fact.
    CARD_INNER = 224 - 16
    too_wide = []
    for st in STAGES:
        for name, cz, ce in st["skills"]:
            for label, size, mono in ((name, 11, True), (cz, 11, False), (ce, 11, False)):
                w = est_width(label, size, mono)
                if w > CARD_INNER:
                    too_wide.append(f"{label!r} ~{w:.0f}px > {CARD_INNER}px")
    if too_wide:
        print("FAIL caption overflows its card:")
        for line in too_wide:
            print("  " + line)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for lang in ("zh", "en"):
        for theme in ("light", "dark"):
            path = OUT / f"skill-map-{lang}{'-dark' if theme == 'dark' else ''}.svg"
            path.write_text(render(theme, lang), encoding="utf-8")
            written.append(path.name)
    print(f"skills={len(declared)} written={len(written)} files={' '.join(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
