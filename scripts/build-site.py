#!/usr/bin/env python3
"""Generate the static site (site/index.html) from the JSON data.

Self-contained single page: no CDN, no build tooling. Re-run after changing data:

    python3 scripts/build-site.py

CI verifies that site/index.html is in sync with data/.
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT = ROOT / "site" / "index.html"

CONFIDENCE_LABEL = {
    "verified": ("可查证原话", "verified"),
    "attributed": ("广泛归于他", "attributed"),
    "paraphrased": ("转述 / 大意", "paraphrased"),
}

CATEGORY_LABEL = {
    "zhuanye": "专业选择",
    "yuanxiao": "院校推荐",
    "jiuye": "就业前景",
    "rensheng": "人生哲理",
    "xuexi": "学习建议",
    "zhiyuan-celue": "志愿填报策略",
}

CSS = """
:root {
  --blue: #1e5aa8;
  --blue-dark: #16395f;
  --ink: #1f2329;
  --muted: #6b7280;
  --line: #e5e7eb;
  --bg: #f5f6f8;
  --card: #ffffff;
  --red: #c62828;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 16px/1.7 -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
.wrap { max-width: 860px; margin: 0 auto; padding: 0 20px; }

header.top {
  background: var(--blue-dark);
  border-bottom: 4px solid var(--red);
  color: #fff;
  padding: 40px 0 30px;
}
header.top h1 { margin: 0; font-size: 30px; letter-spacing: 1px; }
header.top .sub { margin: 8px 0 0; color: #d6e2f2; font-size: 15px; }
header.top .meta { margin-top: 14px; font-size: 13px; color: #b9cbe4; }
header.top .meta span { margin-right: 14px; }

main { padding: 26px 0 40px; }
.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 20px 22px;
  margin-bottom: 18px;
}
.card h2 { margin: 0 0 10px; font-size: 18px; }
.card h2 .hint { font-weight: normal; font-size: 13px; color: var(--muted); margin-left: 8px; }
pre {
  margin: 10px 0;
  background: #0f2743;
  color: #eaf2ff;
  padding: 12px 14px;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 13.5px;
  line-height: 1.6;
}
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
.card p { margin: 8px 0 0; color: var(--muted); font-size: 14px; }

.stats { display: flex; flex-wrap: wrap; gap: 10px; padding: 16px 22px; }
.stat { flex: 1 1 120px; text-align: center; padding: 6px 0; }
.stat b { display: block; font-size: 22px; color: var(--blue); }
.stat span { font-size: 12.5px; color: var(--muted); }

.toolbar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 4px 0 16px; }
#search {
  flex: 1 1 220px;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  font-size: 14px;
  background: #fff;
}
#search:focus { outline: 2px solid #cfe0f5; border-color: var(--blue); }
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip-btn {
  border: 1px solid var(--line);
  background: #fff;
  color: var(--ink);
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 13px;
  cursor: pointer;
}
.chip-btn:hover { border-color: var(--blue); color: var(--blue); }
.chip-btn.active { background: var(--blue); border-color: var(--blue); color: #fff; }
#count { font-size: 13px; color: var(--muted); margin: 0 0 12px; }

.cat-title {
  font-size: 19px;
  color: var(--blue-dark);
  margin: 30px 0 12px;
  padding-left: 10px;
  border-left: 4px solid var(--blue);
}
.q {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 16px 18px;
  margin-bottom: 12px;
}
.q-head { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; font-size: 12px; }
.chip {
  background: #eef4fc;
  color: var(--blue);
  border-radius: 4px;
  padding: 2px 8px;
}
.id { color: var(--muted); font-size: 11.5px; }
.conf { border-radius: 4px; padding: 2px 8px; }
.conf.verified { background: #e7f5ec; color: #1b7a44; }
.conf.attributed { background: #fdf0e3; color: #a55a12; }
.conf.paraphrased { background: #f0f1f3; color: #5a6472; }
.q .zh { margin: 10px 0 4px; font-size: 16.5px; }
.q .en { margin: 0; color: var(--muted); font-size: 13.5px; }
.q-foot { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 12px; font-size: 12px; color: var(--muted); }
.q-foot .tags { color: #4b5563; }
.q:target { outline: 2px solid #cfe0f5; }

.note ul { margin: 8px 0 0; padding-left: 20px; color: #374151; font-size: 14px; }
.note li { margin: 4px 0; }
.links a { display: inline-block; margin: 4px 14px 4px 0; font-size: 14px; }

footer { border-top: 1px solid var(--line); padding: 22px 0 40px; color: var(--muted); font-size: 13px; }
footer p { margin: 6px 0; }
.empty { color: var(--muted); padding: 30px 0; text-align: center; }
@media (max-width: 600px) {
  pre { white-space: pre-wrap; word-break: break-all; }
  header.top { padding: 28px 0 22px; }
  header.top h1 { font-size: 23px; }
  .card { padding: 16px; }
}
"""

JS = """
(function () {
  var search = document.getElementById('search');
  var count = document.getElementById('count');
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.chip-btn'));
  var items = Array.prototype.slice.call(document.querySelectorAll('.q'));
  var active = 'all';

  function apply() {
    var q = (search.value || '').trim().toLowerCase();
    var shown = 0;
    items.forEach(function (el) {
      var okCat = active === 'all' || el.getAttribute('data-cat') === active;
      var okText = !q || el.getAttribute('data-text').indexOf(q) !== -1;
      var ok = okCat && okText;
      el.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    count.textContent = '显示 ' + shown + ' / ' + items.length + ' 条';
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      buttons.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      active = btn.getAttribute('data-cat');
      apply();
    });
  });
  search.addEventListener('input', apply);
  apply();
})();
"""


def esc(value):
    return html.escape(str(value), quote=True)


def load_quotes():
    quotes = []
    for path in sorted((DATA_DIR / "zhangxuefeng").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        cat = payload["category"]
        for quote in payload["quotes"]:
            quotes.append((cat, quote))
    return quotes


def build():
    categories = json.loads((DATA_DIR / "categories.json").read_text(encoding="utf-8"))["categories"]
    quotes = load_quotes()
    total = len(quotes)
    conf_counts = {"verified": 0, "attributed": 0, "paraphrased": 0}
    for _, quote in quotes:
        conf_counts[quote["confidence"]] = conf_counts.get(quote["confidence"], 0) + 1

    cat_meta = {c["id"]: c for c in categories}
    counts = {}
    for cat, _ in quotes:
        counts[cat] = counts.get(cat, 0) + 1

    chips = ['<button class="chip-btn active" data-cat="all">全部 ' + str(total) + '</button>']
    for cat in sorted(counts, key=lambda c: list(cat_meta).index(c) if c in cat_meta else 99):
        meta = cat_meta.get(cat, {})
        label = meta.get("icon", "") + " " + CATEGORY_LABEL.get(cat, meta.get("name_zh", cat))
        chips.append(
            '<button class="chip-btn" data-cat="' + esc(cat) + '">' + esc(label)
            + " " + str(counts[cat]) + "</button>"
        )

    blocks = []
    for cat in sorted(counts, key=lambda c: list(cat_meta).index(c) if c in cat_meta else 99):
        meta = cat_meta.get(cat, {})
        label = meta.get("icon", "") + " " + CATEGORY_LABEL.get(cat, meta.get("name_zh", cat))
        blocks.append('<h2 class="cat-title" id="cat-' + esc(cat) + '">' + esc(label) + "</h2>")
        for quote_id_cat, quote in quotes:
            if quote_id_cat != cat:
                continue
            conf_key = quote["confidence"]
            conf_label, conf_class = CONFIDENCE_LABEL.get(conf_key, (conf_key, "paraphrased"))
            tags = " ".join("#" + t for t in quote.get("tags", []))
            src = quote.get("source", {})
            src_text = " · ".join(x for x in [src.get("platform"), src.get("type")] if x)
            data_text = " ".join([
                quote.get("text", ""),
                quote.get("text_en", ""),
                " ".join(quote.get("tags", [])),
                " ".join(quote.get("related_majors", [])),
                quote.get("id", ""),
            ]).lower()
            en = quote.get("text_en", "")
            en_html = '<p class="en">' + esc(en) + "</p>" if en else ""
            blocks.append(
                '<article class="q" id="' + esc(quote["id"]) + '" data-cat="' + esc(cat)
                + '" data-text="' + esc(data_text) + '">'
                '<div class="q-head">'
                '<span class="chip">' + esc(label) + "</span>"
                '<code class="id">' + esc(quote["id"]) + "</code>"
                '<span class="conf ' + esc(conf_class) + '">' + esc(conf_label) + "</span>"
                "</div>"
                '<p class="zh">' + esc(quote.get("text", "")) + "</p>"
                + en_html
                + '<div class="q-foot"><span class="tags">' + esc(tags) + "</span>"
                "<span>" + esc(src_text) + "</span></div>"
                "</article>"
            )

    cat_summary = "、".join(
        CATEGORY_LABEL.get(c.get("id"), c.get("name_zh", "")) for c in categories if counts.get(c.get("id"))
    )
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>张雪峰语录大全 · 高考志愿填报指南（{total} 条结构化语料）</title>
<meta name="description" content="张雪峰公开言论的结构化语料 {total} 条：{cat_summary}。每条带出处与可信度标注，MIT 开源，可直接用于 AI 问答、检索与志愿咨询。">
<meta property="og:title" content="张雪峰语录大全 · 高考志愿填报指南">
<meta property="og:description" content="{total} 条结构化语料，含出处与可信度标注，MIT 开源。">
<meta property="og:type" content="website">
<meta property="og:image" content="https://dongsheng123132.github.io/gaokao-mentor-wisdom/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://dongsheng123132.github.io/gaokao-mentor-wisdom/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="张雪峰语录大全 · 高考志愿填报指南">
<meta name="twitter:image" content="https://dongsheng123132.github.io/gaokao-mentor-wisdom/og.png">
<link rel="canonical" href="https://dongsheng123132.github.io/gaokao-mentor-wisdom/">
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <h1>张雪峰语录大全</h1>
    <p class="sub">高考志愿填报 · 专业选择 · 就业现实 —— {total} 条结构化语料，每条带出处和可信度标注</p>
    <div class="meta">
      <span>六大分类</span><span>中英双语</span><span>MIT 开源</span><span>语料截止 2026-03-25</span>
    </div>
  </div>
</header>
<main class="wrap">
  <section class="card">
    <h2>一行装进 AI <span class="hint">Claude Code / Codex / Cursor / DSH 等 60+ agent</span></h2>
    <pre><code>npx skills add dongsheng123132/gaokao-mentor-wisdom</code></pre>
    <p>装完直接问「河南考生，物理方向，620 分，普通家庭，想学工科，报什么专业」。不做 skill 的话，直接取 <a href="https://github.com/dongsheng123132/gaokao-mentor-wisdom/tree/main/data/zhangxuefeng">JSON 语料</a> 或 <a href="https://github.com/dongsheng123132/gaokao-mentor-wisdom/blob/main/exports/rag_chunks.jsonl">RAG chunks</a> 也行。</p>
  </section>

  <section class="card stats">
    <div class="stat"><b>{total}</b><span>条语录</span></div>
    <div class="stat"><b>6</b><span>大分类</span></div>
    <div class="stat"><b>{conf_counts["verified"]}</b><span>可查证原话</span></div>
    <div class="stat"><b>{conf_counts["attributed"]}</b><span>广泛归于他</span></div>
    <div class="stat"><b>{conf_counts["paraphrased"]}</b><span>转述或大意</span></div>
  </section>

  <div class="toolbar">
    <input id="search" type="search" placeholder="搜专业 / 关键词，例如：计算机、调剂、985、家境" autocomplete="off">
  </div>
  <div class="chips">{"".join(chips)}</div>
  <p id="count"></p>

  <div id="list">
    {"".join(blocks)}
  </div>
  <noscript><p class="empty">搜索和分类筛选需要启用 JavaScript；直接往下翻也能看到全部 {total} 条。</p></noscript>

  <section class="card note">
    <h2>关于这些语录</h2>
    <ul>
      <li><b>可信度分三档</b>：可查证原话（当前 {conf_counts["verified"]} 条）、广泛归于他但无法定位具体出处（{conf_counts["attributed"]} 条）、转述或大意（{conf_counts["paraphrased"]} 条）。引用时请按档位措辞，转述内容不要当成逐字原话。</li>
      <li><b>语料截止 2026-03-25</b>。张雪峰（1984-11-28 — 2026-03-24）去世次日建仓；此后的政策与就业变化不在语料内。</li>
      <li><b>这里没有分数线</b>。分数线、位次、招生计划、选科要求一律以省考试院与学校招生章程为准。</li>
      <li><b>不冒充本人</b>。本页是公开言论的整理与标注，不做商业代言。</li>
    </ul>
  </section>

  <section class="card links">
    <h2>链接</h2>
    <a href="https://github.com/dongsheng123132/gaokao-mentor-wisdom">GitHub 仓库</a>
    <a href="https://github.com/dongsheng123132/gaokao-mentor-wisdom/blob/main/SKILL.md">SKILL.md（安装与用法）</a>
    <a href="https://github.com/dongsheng123132/gaokao-mentor-wisdom/blob/main/llms.txt">llms.txt</a>
    <a href="https://github.com/dongsheng123132/gaokao-mentor-wisdom/blob/main/CITATION.cff">引用格式</a>
  </section>
</main>
<footer class="wrap">
  <p>数据以 MIT License 开源 · 每条语录可在仓库 <code>data/zhangxuefeng/</code> 中按 id 回溯</p>
  <p>张雪峰（1984-11-28 — 2026-03-24）· 本站为公开言论整理，非官方站点</p>
</footer>
<script>{JS}</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {total} quotes, {len(page)} bytes")


if __name__ == "__main__":
    build()
