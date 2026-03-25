#!/usr/bin/env python3
"""Generate a self-contained HTML book from Zhang Xuefeng quote data."""

import base64
import json
from collections import OrderedDict
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
EXPORT_DIR = ROOT / "exports"
QR_WECHAT = ROOT.parent / "微信二维码.jpg"
QR_ZSXQ = ROOT.parent / "虾叔知识星球.jpg"

# ── Brand ──────────────────────────────────────────────────────────────
BRAND = {
    "name": "虾叔",
    "studio": "贺去病 AI 工作室",
    "wechat": "hecare888",
    "site1": "z-claw.net",
    "site2": "shuclaw.net",
    "slogan": "让每一分都不浪费，让每个家庭都有方向",
}

# ── Chapter order (matches categories.json) ────────────────────────────
CHAPTER_ORDER = ["zhuanye", "jiuye", "rensheng", "yuanxiao", "xuexi", "zhiyuan-celue"]

# ── Sentiment → border color ───────────────────────────────────────────
SENTIMENT_COLOR = {
    "encouraging": "#2e7d32",
    "cautionary": "#e8740c",
    "critical": "#c62828",
    "humorous": "#7b1fa2",
    "neutral": "#78909c",
}

# ── Xiashu commentary per chapter ──────────────────────────────────────
XIASHU_COMMENTARY = {
    "zhuanye": [
        ("zhuanye_1", "建议家长从高二起，和孩子一起看各专业的真实就业数据。教育部和各大招聘平台每年都会发布毕业生就业报告，这是最客观的参考依据。不要只听「热门」二字，要看数据说话。"),
        ("zhuanye_2", "专业选择的核心原则：先看就业市场需求，再看孩子兴趣和能力，最后看家庭能提供的资源支持。三者的交集，就是最适合的方向。"),
        ("zhuanye_3", "家长千万不要用自己年轻时的认知来判断现在的专业好坏。二十年前的'铁饭碗'可能早已生锈，而新兴行业的机会可能超出我们的想象。多听听年轻人的声音，多看看行业趋势报告。"),
        ("zhuanye_4", "如果孩子确实不知道自己喜欢什么，不妨先选择'宽口径'的专业——计算机、数学、经济学这类基础学科，未来转型空间大。千万别在迷茫时选一个太窄的方向。"),
    ],
    "jiuye": [
        ("jiuye_1", "建议家长关注目标行业的'天花板'和'地板'。一个行业的平均薪资不重要，重要的是中位数薪资和头部薪资之间的差距——差距越大，说明这个行业越看个人能力。"),
        ("jiuye_2", "就业不只看第一份工作的薪资，更要看职业发展的'斜率'。有些行业起薪低但增长快（如医疗、法律），有些起薪高但很快到顶。和孩子一起画一条十年的收入曲线，视野会完全不同。"),
        ("jiuye_3", "鼓励孩子在大学期间多实习。纸上谈兵永远不如亲身体验——很多学生在实习后才发现，自己想象中的'高大上'工作其实并不适合自己，越早发现越好。"),
    ],
    "rensheng": [
        ("rensheng_1", "张雪峰的话有时很扎心，但背后是对普通家庭的真诚关怀。作为家长，我们要做的不是焦虑，而是帮孩子看清现实后，一起找到最适合的路。"),
        ("rensheng_2", "家长自己也需要'志愿填报心理建设'。放下面子、放下攀比，回到孩子本身——他/她的性格、能力和热情才是最重要的决策依据。"),
    ],
    "yuanxiao": [
        ("yuanxiao_1", "不要只看排名，带孩子去目标城市和学校实地考察。感受一个城市的生活节奏和产业氛围，可能比任何排行榜都有用。条件允许的话，高二暑假就可以安排。"),
        ("yuanxiao_2", "选学校也是选城市。一线城市的实习机会、行业资源、眼界开阔程度，是很多二三线城市学校无法比拟的。如果分数够，优先考虑在目标就业城市上学。"),
    ],
    "xuexi": [
        ("xuexi_1", "学习方法因人而异，但有一条是通用的：让孩子在高中阶段就学会自主规划时间。这个能力到了大学和职场，比任何一门课的分数都重要。"),
        ("xuexi_2", "家长能做的最好的事，是营造一个稳定、支持的家庭环境。不是天天催孩子学习，而是让孩子知道——无论结果如何，家永远是他/她的后盾。"),
    ],
    "zhiyuan-celue": [
        ("zhiyuan_1", "建议全家开一次正式的'志愿讨论会'，把孩子的意愿、家庭条件、就业目标摆上台面，充分讨论。避免出分后仓促决定，那时压力太大，容易犯错。"),
        ("zhiyuan_2", "志愿填报是一门'技术活'：冲、稳、保的梯度一定要拉开。具体比例建议2:5:3——两个冲刺、五个稳妥、三个保底。每个层次里都要有真正愿意去读的学校和专业。"),
        ("zhiyuan_3", "千万记住：专业调剂是一把双刃剑。勾选'服从调剂'可以降低滑档风险，但也可能被调到完全不想读的专业。建议每个志愿的全部专业都仔细看过，确保没有完全不能接受的。"),
    ],
}


# ── Data loading ───────────────────────────────────────────────────────
def load_categories() -> dict:
    with open(DATA_DIR / "categories.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["id"]: c for c in data["categories"]}


def load_quotes_by_category() -> OrderedDict:
    result = OrderedDict()
    for cat_id in CHAPTER_ORDER:
        fpath = DATA_DIR / "zhangxuefeng" / f"{cat_id}.json"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        result[cat_id] = data["quotes"]
    return result


def encode_image_base64(path: Path) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    suffix = path.suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png"}.get(suffix, "jpeg")
    return f"data:image/{mime};base64,{b64}"


# ── CSS ────────────────────────────────────────────────────────────────
def get_css() -> str:
    return """
@page {
    size: A4;
    margin: 0;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 17px; }
body {
    font-family: "Songti SC", "SimSun", "Noto Serif CJK SC", serif;
    color: #1a1a1a;
    line-height: 1.8;
    max-width: 210mm;
    margin: 0 auto;
    padding: 1.2cm 1.5cm;
    background: #fff;
}
h1, h2, h3, h4 {
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
    color: #1a3a5c;
}
a { color: #e8740c; text-decoration: none; }
a:hover { text-decoration: underline; }

/* ── Cover ── */
.cover-page {
    page-break-after: always;
    text-align: center;
    padding: 8cm 0 0 0;
}
.cover-page h1 {
    font-size: 2.4rem; margin-bottom: 0.5rem;
    color: #1a3a5c;
}
.cover-page .subtitle { font-size: 1.3rem; color: #555; margin-bottom: 0.4rem; }
.cover-page .edition { font-size: 1rem; color: #e8740c; margin-bottom: 2rem; }
.cover-page .brand-line { font-size: 0.95rem; color: #78909c; margin-top: 1rem; }
.cover-divider {
    width: 120px; height: 4px; margin: 1.5rem auto;
    background: linear-gradient(90deg, #1a3a5c, #e8740c);
    border-radius: 2px;
}

/* ── Copyright ── */
.copyright-page {
    page-break-after: always;
    text-align: center;
    padding: 6cm 0 0 0;
}
.copyright-page .inner {
    max-width: 480px; padding: 2rem;
    border: 1px solid #ddd; border-radius: 12px; background: #fafafa;
}
.copyright-page p { font-size: 0.85rem; color: #666; margin-bottom: 0.6rem; line-height: 1.7; }

/* ── TOC ── */
.toc-page { page-break-after: always; padding-top: 3rem; }
.toc-page h2 { font-size: 1.8rem; margin-bottom: 1.5rem; text-align: center; }
.toc-list { list-style: none; padding: 0; }
.toc-list li {
    padding: 0.6rem 0; border-bottom: 1px dotted #ccc;
    display: flex; justify-content: space-between; align-items: baseline;
}
.toc-list li a { color: #1a3a5c; font-size: 1.1rem; }
.toc-list li .toc-count { color: #999; font-size: 0.9rem; }

/* ── Preface ── */
.preface { page-break-after: always; padding-top: 2rem; }
.preface h2 { font-size: 1.6rem; margin-bottom: 1.2rem; }
.preface p { margin-bottom: 1rem; text-indent: 2em; }

/* ── Chapter ── */
.chapter { page-break-before: always; padding-top: 2rem; }
.chapter-header {
    text-align: center; margin-bottom: 2rem;
    padding-bottom: 1rem; border-bottom: 3px solid #1a3a5c;
}
.chapter-header h2 { font-size: 1.8rem; }
.chapter-header .ch-desc { color: #666; font-size: 0.95rem; margin-top: 0.3rem; }

/* ── Quote card ── */
.quote-card {
    break-inside: avoid; page-break-inside: avoid;
    margin: 1.5rem 0; padding: 1.2rem 1.2rem 1rem 1.5rem;
    border-left: 5px solid #78909c; border-radius: 0 8px 8px 0;
    background: #f8fafc; position: relative;
}
.quote-card::before {
    content: "\\201C"; position: absolute; top: -0.2rem; left: 0.4rem;
    font-size: 3.5rem; color: rgba(26,58,92,0.12);
    font-family: Georgia, serif; line-height: 1;
}
.quote-card .quote-number {
    position: absolute; top: 0.6rem; right: 0.8rem;
    font-size: 0.75rem; color: #aaa;
    font-family: "PingFang SC", sans-serif;
}
.quote-text {
    font-size: 1.2rem; font-weight: 600; color: #1a3a5c;
    margin-bottom: 0.6rem; padding-left: 0.5rem; line-height: 1.9;
}
.quote-context {
    font-size: 0.88rem; color: #666; margin-bottom: 0.5rem;
    padding-left: 0.5rem; font-style: italic;
}
.quote-tags { margin-top: 0.5rem; padding-left: 0.5rem; }
.tag {
    display: inline-block; font-size: 0.75rem; color: #3a6a9c;
    background: #e3edf7; padding: 0.15rem 0.6rem;
    border-radius: 20px; margin: 0.15rem 0.2rem;
}
.quote-majors {
    font-size: 0.82rem; color: #555; margin-top: 0.4rem; padding-left: 0.5rem;
}
.quote-majors strong { color: #1a3a5c; }
.quote-schools {
    font-size: 0.82rem; color: #555; margin-top: 0.3rem; padding-left: 0.5rem;
}

/* ── Xiashu commentary ── */
.xiashu-box {
    break-inside: avoid; page-break-inside: avoid;
    margin: 1.8rem 0; padding: 1.2rem 1.4rem;
    border: 2px solid #e8740c; border-radius: 10px;
    background: linear-gradient(135deg, #fff8f0, #fff3e6);
}
.xiashu-box .box-title {
    font-family: "PingFang SC", sans-serif;
    font-size: 1rem; font-weight: 700; color: #e8740c;
    margin-bottom: 0.5rem;
}
.xiashu-box .box-title::before { content: "🦐 "; }
.xiashu-box p { font-size: 0.92rem; color: #444; text-indent: 2em; line-height: 1.8; }

/* ── Chapter CTA ── */
.chapter-cta {
    break-inside: avoid; page-break-inside: avoid;
    margin: 2rem 0; padding: 1.2rem;
    border: 2px solid #e8740c; border-radius: 10px;
    background: #fff8f0; text-align: center;
}
.chapter-cta p { font-size: 0.95rem; color: #333; margin-bottom: 0.5rem; }
.chapter-cta .cta-wechat { font-weight: 700; color: #e8740c; font-size: 1rem; }
.chapter-cta img { width: 100px; height: 100px; margin-top: 0.5rem; border-radius: 8px; }

/* ── Appendix ── */
.appendix { page-break-before: always; padding-top: 2rem; }
.appendix h2 { font-size: 1.6rem; margin-bottom: 1rem; text-align: center; }
.appendix h3 { font-size: 1.2rem; margin: 1.5rem 0 0.8rem; color: #1a3a5c; }
.major-table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; font-size: 0.88rem; }
.major-table th {
    background: #1a3a5c; color: #fff; padding: 0.5rem 0.8rem;
    text-align: left; font-family: "PingFang SC", sans-serif;
}
.major-table td { padding: 0.4rem 0.8rem; border-bottom: 1px solid #e0e0e0; }
.major-table tr:nth-child(even) { background: #f5f8fb; }
.major-recommend { color: #2e7d32; }
.major-caution { color: #c62828; }

/* ── About page ── */
.about-page {
    page-break-before: always; padding-top: 2rem; text-align: center;
}
.about-page h2 { font-size: 1.8rem; margin-bottom: 0.5rem; }
.about-page .studio-name { font-size: 1.1rem; color: #666; margin-bottom: 2rem; }
.about-intro { max-width: 520px; margin: 0 auto 2rem; text-align: left; }
.about-intro p { font-size: 0.95rem; color: #444; margin-bottom: 0.8rem; text-indent: 2em; }
.about-services {
    max-width: 520px; margin: 0 auto 2rem; text-align: left;
    background: #f5f8fb; padding: 1.2rem; border-radius: 10px;
}
.about-services h3 { font-size: 1.1rem; margin-bottom: 0.6rem; color: #1a3a5c; }
.about-services ul { padding-left: 1.5rem; }
.about-services li { font-size: 0.92rem; color: #444; margin-bottom: 0.3rem; }
.qr-section { display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin: 2rem 0; }
.qr-item { text-align: center; }
.qr-item img { width: 160px; height: 160px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.qr-item .qr-label {
    font-family: "PingFang SC", sans-serif;
    font-size: 0.9rem; color: #555; margin-top: 0.5rem;
}
.about-urls { margin-top: 1.5rem; }
.about-urls p { font-size: 0.95rem; color: #666; margin-bottom: 0.3rem; }
.about-urls a { font-weight: 700; }

/* ── Founder card ── */
.founder-card {
    text-align: center; max-width: 480px; margin: 0 auto 1.5rem;
    background: #f5f8fb; padding: 1.2rem; border-radius: 10px;
}
.founder-card h3 {
    font-size: 1.2rem; color: #1a3a5c; margin-bottom: 0.8rem; text-align: center;
}
.founder-titles span {
    display: inline-block; background: #e3edf7; color: #3a6a9c;
    padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.85rem; margin: 0.2rem;
}

/* ── Back cover ── */
.back-cover {
    page-break-before: always;
    text-align: center;
    padding: 8cm 0 0 0;
}
.back-cover .slogan {
    font-size: 1.4rem; color: #1a3a5c; font-weight: 700; margin-bottom: 1.5rem;
}
.back-cover img { width: 120px; height: 120px; border-radius: 10px; }
.back-cover .back-brand { font-size: 0.85rem; color: #999; margin-top: 1rem; }

/* ── Footer ── */
.page-footer {
    text-align: center; font-size: 0.72rem; color: #aaa;
    padding-top: 1rem; margin-top: 2rem; border-top: 1px solid #eee;
}

"""


MOBILE_CSS = """
@page {
    size: 95mm 170mm;
    margin: 0;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 14px; }
body {
    font-family: "PingFang SC", "Songti SC", "Noto Sans CJK SC", sans-serif;
    color: #1a1a1a;
    line-height: 1.75;
    max-width: 100%;
    margin: 0;
    padding: 0.8rem 0.7rem;
    background: #fff;
}
h1, h2, h3, h4 {
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
    color: #1a3a5c;
}
a { color: #e8740c; text-decoration: none; }

/* ── Cover ── */
.cover-page {
    page-break-after: always;
    text-align: center;
    padding: 2.5rem 0.5rem 0;
}
.cover-page h1 { font-size: 1.6rem; margin-bottom: 0.4rem; color: #1a3a5c; }
.cover-page .subtitle { font-size: 0.95rem; color: #555; margin-bottom: 0.3rem; }
.cover-page .edition { font-size: 0.85rem; color: #e8740c; margin-bottom: 1rem; }
.cover-page .brand-line { font-size: 0.75rem; color: #78909c; margin-top: 0.5rem; }
.cover-divider {
    width: 80px; height: 3px; margin: 0.8rem auto;
    background: linear-gradient(90deg, #1a3a5c, #e8740c);
    border-radius: 2px;
}

/* ── Copyright ── */
.copyright-page {
    page-break-after: always;
    text-align: center;
    padding: 1.5rem 0.3rem 0;
}
.copyright-page .inner {
    max-width: 100%; padding: 0.8rem;
    border: 1px solid #ddd; border-radius: 8px; background: #fafafa;
}
.copyright-page p { font-size: 0.72rem; color: #666; margin-bottom: 0.4rem; line-height: 1.6; }

/* ── TOC ── */
.toc-page { page-break-after: always; padding-top: 1.2rem; }
.toc-page h2 { font-size: 1.3rem; margin-bottom: 0.8rem; text-align: center; }
.toc-list { list-style: none; padding: 0; }
.toc-list li {
    padding: 0.4rem 0; border-bottom: 1px dotted #ccc;
    display: flex; justify-content: space-between; align-items: baseline;
}
.toc-list li a { color: #1a3a5c; font-size: 0.88rem; }
.toc-list li .toc-count { color: #999; font-size: 0.75rem; }

/* ── Preface ── */
.preface { page-break-after: always; padding-top: 1rem; }
.preface h2 { font-size: 1.2rem; margin-bottom: 0.8rem; }
.preface p { margin-bottom: 0.7rem; text-indent: 2em; font-size: 0.88rem; }

/* ── Chapter ── */
.chapter { page-break-before: always; padding-top: 1rem; }
.chapter-header {
    text-align: center; margin-bottom: 1rem;
    padding-bottom: 0.6rem; border-bottom: 2px solid #1a3a5c;
}
.chapter-header h2 { font-size: 1.3rem; }
.chapter-header .ch-desc { color: #666; font-size: 0.78rem; margin-top: 0.2rem; }

/* ── Quote card ── */
.quote-card {
    break-inside: avoid; page-break-inside: avoid;
    margin: 0.8rem 0; padding: 0.7rem 0.6rem 0.6rem 0.9rem;
    border-left: 4px solid #78909c; border-radius: 0 6px 6px 0;
    background: #f8fafc; position: relative;
}
.quote-card::before {
    content: "\\201C"; position: absolute; top: -0.1rem; left: 0.2rem;
    font-size: 2.2rem; color: rgba(26,58,92,0.12);
    font-family: Georgia, serif; line-height: 1;
}
.quote-card .quote-number {
    position: absolute; top: 0.3rem; right: 0.5rem;
    font-size: 0.65rem; color: #aaa;
    font-family: "PingFang SC", sans-serif;
}
.quote-text {
    font-size: 0.95rem; font-weight: 600; color: #1a3a5c;
    margin-bottom: 0.4rem; padding-left: 0.3rem; line-height: 1.75;
}
.quote-context {
    font-size: 0.75rem; color: #666; margin-bottom: 0.3rem;
    padding-left: 0.3rem; font-style: italic;
}
.quote-tags { margin-top: 0.3rem; padding-left: 0.3rem; }
.tag {
    display: inline-block; font-size: 0.65rem; color: #3a6a9c;
    background: #e3edf7; padding: 0.1rem 0.45rem;
    border-radius: 20px; margin: 0.1rem 0.15rem;
}
.quote-majors {
    font-size: 0.72rem; color: #555; margin-top: 0.3rem; padding-left: 0.3rem;
}
.quote-majors strong { color: #1a3a5c; }
.quote-schools {
    font-size: 0.72rem; color: #555; margin-top: 0.2rem; padding-left: 0.3rem;
}

/* ── Xiashu commentary ── */
.xiashu-box {
    break-inside: avoid; page-break-inside: avoid;
    margin: 1rem 0; padding: 0.8rem 0.7rem;
    border: 2px solid #e8740c; border-radius: 8px;
    background: linear-gradient(135deg, #fff8f0, #fff3e6);
}
.xiashu-box .box-title {
    font-family: "PingFang SC", sans-serif;
    font-size: 0.85rem; font-weight: 700; color: #e8740c;
    margin-bottom: 0.3rem;
}
.xiashu-box .box-title::before { content: "🦐 "; }
.xiashu-box p { font-size: 0.82rem; color: #444; text-indent: 2em; line-height: 1.7; }

/* ── Chapter CTA ── */
.chapter-cta {
    break-inside: avoid; page-break-inside: avoid;
    margin: 1rem 0; padding: 0.7rem;
    border: 2px solid #e8740c; border-radius: 8px;
    background: #fff8f0; text-align: center;
}
.chapter-cta p { font-size: 0.78rem; color: #333; margin-bottom: 0.3rem; }
.chapter-cta .cta-wechat { font-weight: 700; color: #e8740c; font-size: 0.85rem; }
.chapter-cta img { width: 65px; height: 65px; margin-top: 0.3rem; border-radius: 6px; }

/* ── Appendix ── */
.appendix { page-break-before: always; padding-top: 1rem; }
.appendix h2 { font-size: 1.2rem; margin-bottom: 0.8rem; text-align: center; }
.appendix h3 { font-size: 1rem; margin: 1rem 0 0.5rem; color: #1a3a5c; }
.major-table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.75rem; }
.major-table th {
    background: #1a3a5c; color: #fff; padding: 0.3rem 0.4rem;
    text-align: left; font-family: "PingFang SC", sans-serif;
}
.major-table td { padding: 0.25rem 0.4rem; border-bottom: 1px solid #e0e0e0; }
.major-table tr:nth-child(even) { background: #f5f8fb; }
.major-recommend { color: #2e7d32; }
.major-caution { color: #c62828; }

/* ── About page ── */
.about-page {
    page-break-before: always; padding-top: 1rem; text-align: center;
}
.about-page h2 { font-size: 1.3rem; margin-bottom: 0.3rem; }
.about-page .studio-name { font-size: 0.9rem; color: #666; margin-bottom: 1rem; }
.about-intro { max-width: 100%; margin: 0 auto 1rem; text-align: left; }
.about-intro p { font-size: 0.82rem; color: #444; margin-bottom: 0.5rem; text-indent: 2em; }
.about-services {
    max-width: 100%; margin: 0 auto 1rem; text-align: left;
    background: #f5f8fb; padding: 0.8rem; border-radius: 8px;
}
.about-services h3 { font-size: 0.95rem; margin-bottom: 0.4rem; color: #1a3a5c; }
.about-services ul { padding-left: 1.2rem; }
.about-services li { font-size: 0.78rem; color: #444; margin-bottom: 0.2rem; }
.qr-section { display: flex; justify-content: center; gap: 1.2rem; flex-wrap: wrap; margin: 1rem 0; }
.qr-item { text-align: center; }
.qr-item img { width: 100px; height: 100px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
.qr-item .qr-label {
    font-family: "PingFang SC", sans-serif;
    font-size: 0.75rem; color: #555; margin-top: 0.3rem;
}
.about-urls { margin-top: 1rem; }
.about-urls p { font-size: 0.78rem; color: #666; margin-bottom: 0.2rem; }
.about-urls a { font-weight: 700; }

/* ── Founder card ── */
.founder-card {
    text-align: center; max-width: 100%; margin: 0 auto 1rem;
    background: #f5f8fb; padding: 0.8rem; border-radius: 8px;
}
.founder-card h3 { font-size: 1rem; color: #1a3a5c; margin-bottom: 0.5rem; text-align: center; }
.founder-titles span {
    display: inline-block; background: #e3edf7; color: #3a6a9c;
    padding: 0.15rem 0.5rem; border-radius: 20px; font-size: 0.7rem; margin: 0.15rem;
}

/* ── Back cover ── */
.back-cover {
    page-break-before: always;
    text-align: center;
    padding: 2.5rem 0.5rem 0;
}
.back-cover .slogan { font-size: 1.1rem; color: #1a3a5c; font-weight: 700; margin-bottom: 1rem; }
.back-cover img { width: 80px; height: 80px; border-radius: 8px; }
.back-cover .back-brand { font-size: 0.72rem; color: #999; margin-top: 0.8rem; }

/* ── Footer ── */
.page-footer {
    text-align: center; font-size: 0.6rem; color: #aaa;
    padding-top: 0.6rem; margin-top: 1rem; border-top: 1px solid #eee;
}
"""


# ── HTML Renderers ─────────────────────────────────────────────────────
def render_cover() -> str:
    return """
<div class="cover-page">
    <h1>张雪峰说高考</h1>
    <div class="subtitle">105条志愿填报金句</div>
    <div class="cover-divider"></div>
    <div class="subtitle">家长必读版 · 虾叔精选</div>
    <div class="edition">2026年版</div>
    <div class="brand-line">志愿虾 z-claw.net ｜ 虾叔 shuclaw.net</div>
</div>
"""


def render_copyright() -> str:
    return """
<div class="copyright-page">
    <div class="inner">
        <p><strong>《张雪峰说高考：105条志愿填报金句》</strong></p>
        <p>家长必读版 · 虾叔精选 · 2026年版</p>
        <p style="margin-top:1rem;">
            <strong>免责声明</strong><br>
            本书语录内容源自张雪峰老师公开发表的直播、短视频及演讲内容。<br>
            由虾叔团队（贺去病 AI 工作室）精选编辑整理，非官方出版物。<br>
            仅供学习参考，不构成专业志愿填报建议。<br>
            如有侵权请联系 hecare888 处理。
        </p>
        <p style="margin-top:1rem;">
            编辑：虾叔团队<br>
            网站：志愿虾 z-claw.net ｜ 虾叔 shuclaw.net<br>
            微信：hecare888
        </p>
    </div>
</div>
"""


def render_toc(categories: dict, quotes_by_cat: OrderedDict) -> str:
    items = ""
    for i, (cat_id, quotes) in enumerate(quotes_by_cat.items(), 1):
        cat = categories[cat_id]
        items += f"""
        <li>
            <a href="#{cat_id}">{cat['icon']} 第{_cn_num(i)}章：{cat['name_zh']}</a>
            <span class="toc-count">{len(quotes)} 条</span>
        </li>"""
    items += """
        <li>
            <a href="#appendix">📊 附录：专业速查表</a>
            <span class="toc-count"></span>
        </li>
        <li>
            <a href="#about">🦐 关于虾叔</a>
            <span class="toc-count"></span>
        </li>"""

    return f"""
<div class="toc-page">
    <h2>目 录</h2>
    <ul class="toc-list">{items}
    </ul>
</div>
"""


def render_quote_card(q: dict, idx: int) -> str:
    sentiment = q.get("sentiment", "neutral")
    border_color = SENTIMENT_COLOR.get(sentiment, "#78909c")
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in q.get("tags", []))
    majors_html = ""
    if q.get("related_majors"):
        majors_html = f'<div class="quote-majors"><strong>相关专业：</strong>{" / ".join(q["related_majors"])}</div>'
    # For yuanxiao, show recommended schools if in context
    context_html = ""
    if q.get("context"):
        context_html = f'<div class="quote-context">📌 {q["context"]}</div>'

    return f"""
<div class="quote-card" style="border-left-color:{border_color}">
    <span class="quote-number">#{idx}</span>
    <div class="quote-text">{q["text"]}</div>
    {context_html}
    <div class="quote-tags">{tags_html}</div>
    {majors_html}
</div>
"""


def render_xiashu_box(title: str, content: str) -> str:
    return f"""
<div class="xiashu-box">
    <div class="box-title">{title}</div>
    <p>{content}</p>
</div>
"""


def render_chapter_cta(qr_wechat_b64: str) -> str:
    img_html = f'<br><img src="{qr_wechat_b64}" alt="微信二维码">' if qr_wechat_b64 else ""
    return f"""
<div class="chapter-cta">
    <p>需要针对性建议？</p>
    <p class="cta-wechat">扫码添加虾叔微信 hecare888</p>
    {img_html}
    <p style="font-size:0.82rem;color:#999;margin-top:0.5rem;">志愿虾 z-claw.net ｜ 虾叔 shuclaw.net</p>
</div>
"""


def render_chapter(cat_id: str, cat: dict, quotes: list, ch_num: int,
                   commentary: list, qr_wechat_b64: str) -> str:
    header = f"""
<div class="chapter" id="{cat_id}">
    <div class="chapter-header">
        <h2>{cat['icon']} 第{_cn_num(ch_num)}章：{cat['name_zh']}</h2>
        <div class="ch-desc">{cat.get('description', '')} · 共 {len(quotes)} 条</div>
    </div>
"""
    body = ""
    commentary_idx = 0
    for i, q in enumerate(quotes, 1):
        body += render_quote_card(q, i)
        # Insert commentary every ~7 quotes
        if i % 7 == 0 and commentary_idx < len(commentary):
            _, text = commentary[commentary_idx]
            body += render_xiashu_box("虾叔点评", text)
            commentary_idx += 1

    # Remaining commentary
    while commentary_idx < len(commentary):
        _, text = commentary[commentary_idx]
        body += render_xiashu_box("虾叔点评", text)
        commentary_idx += 1

    body += render_chapter_cta(qr_wechat_b64)
    footer = render_page_footer()
    return header + body + footer + "\n</div>"


def render_appendix(quotes_by_cat: OrderedDict) -> str:
    recommended = {}
    cautionary = {}

    for quotes in quotes_by_cat.values():
        for q in quotes:
            sentiment = q.get("sentiment", "neutral")
            for m in q.get("related_majors", []):
                if sentiment in ("encouraging",):
                    recommended[m] = recommended.get(m, 0) + 1
                elif sentiment in ("cautionary", "critical"):
                    cautionary[m] = cautionary.get(m, 0) + 1

    def make_table(data: dict, css_class: str) -> str:
        if not data:
            return "<p>暂无数据</p>"
        sorted_items = sorted(data.items(), key=lambda x: -x[1])
        rows = ""
        for major, count in sorted_items:
            rows += f'<tr><td class="{css_class}">{major}</td><td>{count} 次提及</td></tr>'
        return f"""
<table class="major-table">
    <tr><th>专业名称</th><th>提及次数</th></tr>
    {rows}
</table>"""

    return f"""
<div class="appendix" id="appendix">
    <h2>📊 附录：专业速查表</h2>
    <p style="text-align:center;color:#666;font-size:0.9rem;margin-bottom:1.5rem;">
        根据张雪峰语录中提及的专业，按推荐和警示分类汇总<br>
        <span style="color:#e8740c;">如需个性化推荐，使用志愿虾在线工具或联系虾叔</span>
    </p>

    <h3 style="color:#2e7d32;">✅ 推荐专业（语录中正面提及）</h3>
    {make_table(recommended, "major-recommend")}

    <h3 style="color:#c62828;">⚠️ 警示专业（语录中建议谨慎）</h3>
    {make_table(cautionary, "major-caution")}
</div>
{render_page_footer()}
"""


def render_about(qr_wechat_b64: str, qr_zsxq_b64: str) -> str:
    wechat_img = f'<img src="{qr_wechat_b64}" alt="微信二维码">' if qr_wechat_b64 else "<p>微信：hecare888</p>"
    zsxq_img = f'<img src="{qr_zsxq_b64}" alt="知识星球">' if qr_zsxq_b64 else "<p>知识星球</p>"

    return f"""
<div class="about-page" id="about">
    <h2>🦐 关于虾叔</h2>
    <div class="studio-name">{BRAND['studio']}</div>

    <div class="founder-card">
        <h3>🦐 虾叔 · 贺东升</h3>
        <div class="founder-titles">
            <span>武汉理工大学 硕士</span>
            <span>挑战杯 2 次全国决赛选手</span>
            <span>连续创业者 · 50+ 产品</span>
            <span>深海 AI 技术研究院 创始人</span>
            <span>19 年从业经验</span>
            <span>U-Claw 886 Stars 开源作者</span>
        </div>
    </div>

    <div class="about-intro">
        <p>虾叔团队专注于高考志愿填报咨询服务，结合 AI 技术与资深教育经验，为每一个家庭提供科学、个性化的志愿填报指导。</p>
        <p>我们相信，每一分都不应该浪费，每个孩子都值得被认真对待。无论您的孩子是高分考生还是普通学子，我们都会用心为您规划最优方案。</p>
    </div>

    <div class="about-services">
        <h3>📋 服务内容</h3>
        <ul>
            <li>一对一志愿填报咨询（线上/线下）</li>
            <li>专业选择深度分析</li>
            <li>院校匹配与录取概率评估</li>
            <li>志愿方案制定与优化</li>
            <li>AI 智能选校选专业工具</li>
            <li>高考季全程跟踪服务</li>
        </ul>
    </div>

    <div class="qr-section">
        <div class="qr-item">
            {wechat_img}
            <div class="qr-label">微信咨询：{BRAND['wechat']}</div>
        </div>
        <div class="qr-item">
            {zsxq_img}
            <div class="qr-label">加入知识星球</div>
        </div>
    </div>

    <div class="about-urls">
        <p>🌐 志愿虾：<a href="https://{BRAND['site1']}" target="_blank">{BRAND['site1']}</a></p>
        <p>🌐 虾叔：<a href="https://{BRAND['site2']}" target="_blank">{BRAND['site2']}</a></p>
        <p>💬 微信号：<strong>{BRAND['wechat']}</strong></p>
    </div>
</div>
"""


def render_back_cover(qr_wechat_b64: str) -> str:
    img_html = f'<img src="{qr_wechat_b64}" alt="虾叔二维码">' if qr_wechat_b64 else ""
    return f"""
<div class="back-cover">
    <div class="slogan">{BRAND['slogan']}</div>
    {img_html}
    <div class="back-brand">
        {BRAND['name']} · {BRAND['studio']}<br>
        志愿虾 {BRAND['site1']} ｜ 虾叔 {BRAND['site2']} ｜ 微信 {BRAND['wechat']}
    </div>
</div>
"""


def render_preface() -> str:
    return """
<div class="preface">
    <h2>前 言</h2>
    <p>每年六月，千万家庭都会面临同一个问题：孩子考了 XXX 分，该报什么学校、什么专业？</p>
    <p>志愿填报，看似只是在表格上填几个代码，实际上却是一个家庭对孩子未来十年、二十年发展方向的一次重大决策。填对了，事半功倍；填错了，可能要用整个大学四年甚至更长时间来弥补。</p>
    <p>张雪峰老师用他独特的犀利风格和丰富的行业经验，把复杂的专业分析、就业前景、院校特点，讲得通俗易懂、直击要害。他的很多观点，虽然有时听着"扎心"，但背后是对无数普通家庭的真诚关怀。</p>
    <p>我们从张雪峰老师的公开内容中，精选了 105 条最具代表性的语录，按照专业选择、就业前景、人生哲理、院校推荐、学习建议和志愿填报策略六大主题进行分类整理，并配上背景注释和实用点评，希望能帮助每一位家长更高效地获取关键信息。</p>
    <p>这不是一本需要从头到尾通读的书——您完全可以根据自己最关心的问题，直接翻到对应的章节。每条语录都是独立的，随手翻阅、随时查看。</p>
    <p style="margin-top:1.5rem;color:#e8740c;">如需个性化志愿填报指导，虾叔团队随时为您服务。您可以通过微信（hecare888）或访问志愿虾 z-claw.net 获取一对一咨询。</p>
    <p style="text-align:right;color:#999;margin-top:2rem;">虾叔团队<br>2026 年 3 月</p>
</div>
"""


def render_page_footer() -> str:
    return f"""
<div class="page-footer">
    志愿虾 {BRAND['site1']} ｜ 虾叔 {BRAND['site2']} ｜ 微信 {BRAND['wechat']}
</div>
"""


# ── Helpers ────────────────────────────────────────────────────────────
CN_NUMS = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

def _cn_num(n: int) -> str:
    if 1 <= n <= 10:
        return CN_NUMS[n - 1]
    return str(n)


# ── PDF Export ─────────────────────────────────────────────────────────
def export_pdf(html_path: Path, output_path: Path,
               width: str = "210mm", height: str = "297mm",
               viewport_width: int = 1240):
    """用 playwright 将 HTML 转 PDF"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport_width, "height": 800})
        page.goto(f"file://{html_path.resolve()}")
        page.wait_for_load_state("networkidle")
        page.emulate_media(media='screen')
        page.pdf(
            path=str(output_path),
            width=width,
            height=height,
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        browser.close()
    size_kb = output_path.stat().st_size / 1024
    print(f"  📄 PDF：{output_path}（{size_kb:.0f} KB）")


# ── Main ───────────────────────────────────────────────────────────────
def build_html(css: str, categories: dict, quotes_by_cat, qr_wechat_b64: str, qr_zsxq_b64: str) -> str:
    """Build full HTML string with given CSS."""
    parts = [
        "<!DOCTYPE html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "<title>张雪峰说高考：105条志愿填报金句 — 虾叔精选</title>",
        f"<style>{css}</style>",
        "</head>",
        "<body>",
    ]
    parts.append(render_cover())
    parts.append(render_copyright())
    parts.append(render_toc(categories, quotes_by_cat))
    parts.append(render_preface())
    for i, (cat_id, quotes) in enumerate(quotes_by_cat.items(), 1):
        cat = categories[cat_id]
        commentary = XIASHU_COMMENTARY.get(cat_id, [])
        parts.append(render_chapter(cat_id, cat, quotes, i, commentary, qr_wechat_b64))
    parts.append(render_appendix(quotes_by_cat))
    parts.append(render_about(qr_wechat_b64, qr_zsxq_b64))
    parts.append(render_back_cover(qr_wechat_b64))
    parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts)


def main():
    print("📖 正在生成《张雪峰说高考》v5 电子书（桌面版 + 手机版）...")

    # Load data
    categories = load_categories()
    quotes_by_cat = load_quotes_by_category()
    total = sum(len(q) for q in quotes_by_cat.values())
    print(f"  ✅ 加载 {total} 条语录（{len(quotes_by_cat)} 个分类）")

    # Encode QR images
    qr_wechat_b64 = encode_image_base64(QR_WECHAT)
    qr_zsxq_b64 = encode_image_base64(QR_ZSXQ)
    print(f"  ✅ 微信二维码: {'已编码' if qr_wechat_b64 else '未找到'}")
    print(f"  ✅ 知识星球二维码: {'已编码' if qr_zsxq_b64 else '未找到'}")

    for i, (cat_id, quotes) in enumerate(quotes_by_cat.items(), 1):
        cat = categories[cat_id]
        print(f"  ✅ 第{_cn_num(i)}章：{cat['name_zh']}（{len(quotes)} 条）")

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # ── 1. Desktop version (A4) ──
    print("\n📐 生成桌面版（A4）...")
    desktop_html = build_html(get_css(), categories, quotes_by_cat, qr_wechat_b64, qr_zsxq_b64)
    desktop_html_path = EXPORT_DIR / "张雪峰语录-高考志愿填报指南-v5.html"
    desktop_html_path.write_text(desktop_html, encoding="utf-8")
    size_kb = desktop_html_path.stat().st_size / 1024
    print(f"  📄 HTML：{desktop_html_path.name}（{size_kb:.0f} KB）")

    desktop_pdf_path = EXPORT_DIR / "张雪峰语录-高考志愿填报指南-v5.pdf"
    export_pdf(desktop_html_path, desktop_pdf_path,
               width="210mm", height="297mm", viewport_width=1240)

    # ── 2. Mobile version (phone-sized) ──
    print("\n📱 生成手机版...")
    mobile_html = build_html(MOBILE_CSS, categories, quotes_by_cat, qr_wechat_b64, qr_zsxq_b64)
    mobile_html_path = EXPORT_DIR / "张雪峰语录-高考志愿填报指南-手机版-v5.html"
    mobile_html_path.write_text(mobile_html, encoding="utf-8")
    size_kb = mobile_html_path.stat().st_size / 1024
    print(f"  📄 HTML：{mobile_html_path.name}（{size_kb:.0f} KB）")

    mobile_pdf_path = EXPORT_DIR / "张雪峰语录-高考志愿填报指南-手机版-v5.pdf"
    export_pdf(mobile_html_path, mobile_pdf_path,
               width="95mm", height="170mm", viewport_width=390)

    print(f"\n🎉 全部完成！exports/ 目录下共 4 个 v5 文件")
    print(f"  📊 语录：{total} 条")


if __name__ == "__main__":
    main()
