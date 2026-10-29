# 张雪峰语录大全 | 高考志愿填报指南 | 专业选择避坑指南

[![语录数量](https://img.shields.io/badge/语录数量-105条-brightgreen)](data/zhangxuefeng/)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-可安装-brightgreen)](SKILL.md)
[![validate](https://github.com/dongsheng123132/gaokao-mentor-wisdom/actions/workflows/validate.yml/badge.svg)](https://github.com/dongsheng123132/gaokao-mentor-wisdom/actions/workflows/validate.yml)
[![数据截止](https://img.shields.io/badge/数据截止-2026--03--25-lightgrey)](.)
[![维护](https://img.shields.io/badge/维护-2026--10--29-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 最全的张雪峰高考志愿填报语录知识库 — 结构化 JSON 数据，覆盖专业选择、就业前景、院校推荐、人生哲理、学习建议、志愿填报策略六大分类，支持 AI 应用集成（RAG / Fine-tuning）。
>
> The most comprehensive structured knowledge base of Zhang Xuefeng's gaokao wisdom — 105 quotes in JSON format, ready for AI integration.

---

## 安装为 Agent Skill（30 秒）

```bash
# 任何认 skills 目录 / SKILL.md 的 agent（Claude Code、OpenClaw 等）
npx skills add dongsheng123132/gaokao-mentor-wisdom
```

装完直接问：**「河南考生，物理方向，620 分（位次约 15000），普通家庭，想学工科，报什么专业？」**

- 根目录的 [`SKILL.md`](SKILL.md) 写死了五步决策流程、语料检索方法、引用规则和硬边界——不是纯数据，是可执行口径
- 一条命令会同步装到 60+ 个 agent（Claude Code、Codex、Cursor、DSH…）；DSH 侧落在 `~/.agents/skills/zhangxuefeng-gaokao/`（跨 agent 共享根），装完新开会话即可。想装到 `~/.dsh/skills/` 就手工 clone，目录名用 `zhangxuefeng-gaokao`（与 frontmatter 的 `name` 一致）
- 只要数据不要 skill：直接用下面的 JSON / JSONL，路径与字段不变

**网页版（免安装）**：<https://dongsheng123132.github.io/gaokao-mentor-wisdom/> —— 105 条语录可直接搜索、按分类筛选，每条带出处与可信度标注。给 AI 抓取的入口是 [`llms.txt`](llms.txt)。

---

## 张雪峰经典语录精选

> "如果你家境一般，没有任何社会资源，不要学金融。" — 张雪峰

> "计算机专业是普通家庭孩子改变命运性价比最高的专业。" — 张雪峰

> "高考是普通人改变命运成本最低的方式，没有之一。" — 张雪峰

> "生化环材，四大天坑，能不碰就别碰。" — 张雪峰

> "你看到的那些说学历不重要的人，他们自己全是名校毕业。" — 张雪峰

> "考公考编，是当代年轻人最大的确定性。" — 张雪峰

> "选专业就是选赛道。你选错了赛道，再努力也是白搭。" — 张雪峰

> "填志愿的优先级：城市 > 学校 > 专业。" — 张雪峰

> "宁去大城市的211，不去小城市的985。" — 张雪峰

> "18岁选错了路，你可能要用一辈子来纠正。" — 张雪峰

---

## 张雪峰谈专业选择

共 **28 条**语录，覆盖金融、计算机、生化环材、医学、法学、新闻学、电气工程、土木工程、师范、护理、心理学、艺术设计、小语种、农学、会计、药学、自动化/AI、军校警校、建筑学、汉语言文学、公共管理、电子商务、统计学、兽医、体育、国际贸易等热门专业。

👉 [查看全部专业选择语录](data/zhangxuefeng/zhuanye.json) | [Markdown 版](docs/zhangxuefeng/zhuanye.md)

## 张雪峰谈就业前景

共 **18 条**语录，覆盖第一份工作重要性、薪资现实、国企优势、私企 vs 国企、自媒体风险、考研延迟就业、大城市 vs 小城市、行业周期、性别就业差距、起薪 vs 天花板、海归贬值、职业教育等话题。

👉 [查看全部就业前景语录](data/zhangxuefeng/jiuye.json) | [Markdown 版](docs/zhangxuefeng/jiuye.md)

## 张雪峰谈人生哲理

共 **18 条**语录，覆盖阶层固化、信息差、平台 vs 努力、婚姻与经济、普通人试错成本、代际传递、人脉本质、认清自己、先苦后甜、地区不平等、18岁选择等深度话题。

👉 [查看全部人生哲理语录](data/zhangxuefeng/rensheng.json) | [Markdown 版](docs/zhangxuefeng/rensheng.md)

## 张雪峰谈院校推荐

共 **16 条**语录，覆盖性价比985（哈工大威海、东北大学、西北农林、中国海洋、兰州大学）、宝藏211（上海大学、南京理工、合肥工大、苏州大学）、城市 vs 学校层次、双一流 vs 985/211、省会优势、独立学院/民办警告、高职 vs 烂本科等。

👉 [查看全部院校推荐语录](data/zhangxuefeng/yuanxiao.json) | [Markdown 版](docs/zhangxuefeng/yuanxiao.md)

## 张雪峰谈学习建议

共 **12 条**语录，覆盖感动自己式学习、数学拉差距、补短板策略、考场心态、模拟考态度、时间管理、错题本、身体健康、最后一个月冲刺、大学学习建议等。

👉 [查看全部学习建议语录](data/zhangxuefeng/xuexi.json) | [Markdown 版](docs/zhangxuefeng/xuexi.md)

## 张雪峰谈志愿填报策略

共 **13 条**语录，覆盖城市>学校>专业优先级、不浪费每一分、平行志愿排序逻辑、提前批机会、学校vs专业取舍、先进去再转专业、地理锁定效应、全家商量、看三年数据、专家咨询、提前准备时间窗等。

👉 [查看全部志愿填报策略语录](data/zhangxuefeng/zhiyuan-celue.json) | [Markdown 版](docs/zhangxuefeng/zhiyuan-celue.md)

---

## 常见问题（FAQ）

### 张雪峰推荐什么专业？

张雪峰最推荐普通家庭选择的专业包括：**计算机科学与技术**（性价比最高）、**电气工程**（国家电网就业）、**临床医学**（越老越值钱）、**师范教育**（铁饭碗）、**汉语言文学**（考公神器）、**统计学/数据科学**（就业面广）、**药学**（性价比高）、**自动化/AI**（未来趋势）。

### 张雪峰怎么看计算机专业？

张雪峰认为"计算机专业是普通家庭孩子改变命运性价比最高的专业"，但也提醒互联网行业存在35岁年龄危机。建议数学好的考生优先选择计算机或AI相关专业。

### 张雪峰怎么看金融专业？

张雪峰明确表示"如果你家境一般，没有任何社会资源，不要学金融"。金融行业高度依赖家庭背景和人脉资源，普通家庭毕业生大多只能去银行卖理财产品。

### 张雪峰怎么看医学专业？

张雪峰认为医学是"穷人家孩子的好选择"，但需要能吃苦。学制长、考试多，但一旦熬出来越老越值钱。药学是更短学制的替代选择。

### 普通家庭孩子怎么选专业？

张雪峰建议普通家庭孩子优先考虑：技术类（计算机、自动化）、体制类（师范、汉语言文学考公）、医疗类（临床医学、药学、护理），避开金融、艺术、新闻等高度依赖家庭资源的专业。

### 2026高考志愿填报建议

张雪峰的核心策略：填志愿优先级为"城市>学校>专业"；平行志愿按"冲稳保"排列；服从调剂一定要勾；参考三年录取数据；高二就开始准备。

### 张雪峰怎么看考公考编？

张雪峰认为"考公考编是当代年轻人最大的确定性"，推荐汉语言文学、法学（五院四系）等专业。国企优势是"旱涝保收、退休有保障"。

### 985和211怎么选？

张雪峰建议"能上985就别去211"，但也强调"宁去大城市211不去小城市985"。推荐性价比985：兰州大学、哈工大威海、东北大学、西北农林科技大学。

---

## 仓库结构

```
├── SKILL.md                   # 🤖 Agent Skill 入口（npx skills add 直接装）
├── llms.txt                   # AI 检索入口（llms.txt 约定）
├── CITATION.cff               # 引用信息（GitHub 侧栏「Cite this repository」）
├── CHANGELOG.md               # 版本记录
├── .github/workflows/         # CI：schema 校验 + docs/exports 同步检查
├── docs/COMPARISON.md         # 与下游 skillset 的口径对照（谁改了什么）
└── data/
    ├── mentors.json           # 名师档案
    ├── categories.json        # 6 大分类
    ├── zhangxuefeng/          # 张雪峰语录（105 条）
    │   ├── zhuanye.json       # 🎯 专业选择（28 条）
    │   ├── jiuye.json         # 💼 就业前景（18 条）
    │   ├── rensheng.json      # 💡 人生哲理（18 条）
    │   ├── yuanxiao.json      # 🏫 院校推荐（16 条）
    │   ├── xuexi.json         # 📚 学习建议（12 条）
    │   └── zhiyuan-celue.json # 📋 志愿填报策略（13 条）
    └── _template/
        └── example.json       # 新名师模板
```

## 快速开始

```bash
# Clone
git clone https://github.com/dongsheng123132/gaokao-mentor-wisdom.git
cd gaokao-mentor-wisdom

# 验证数据
python scripts/validate.py

# 生成 Markdown 文档
python scripts/json2md.py

# 导出 AI 训练数据
python scripts/export-training.py
```

## 语录数据格式

每条语录包含中英文双语、标签、来源、情感分析等结构化字段：

```json
{
  "id": "zxf-zhuanye-001",
  "text": "如果你家境一般，没有任何社会资源，不要学金融。",
  "text_en": "If your family is average with no connections, don't study finance.",
  "context": "直播中谈论金融专业就业门槛",
  "tags": ["金融", "家境", "专业选择"],
  "target_audience": ["高考生", "家长"],
  "source": { "platform": "抖音", "type": "直播" },
  "sentiment": "cautionary",
  "confidence": "attributed",
  "related_majors": ["金融学", "经济学"]
}
```

## 使用场景

- **Agent Skill**：`npx skills add` 一行装成可对话的高考志愿顾问，见上方安装说明
- **网页版**：<https://dongsheng123132.github.io/gaokao-mentor-wisdom/> 直接搜索/筛选 105 条，手机也能看
- **高考生/家长查阅**：按分类浏览张雪峰的专业建议和填报策略
- **AI Chatbot / RAG**：导入 `exports/rag_chunks.jsonl` 构建高考志愿问答机器人
- **Fine-tuning**：使用 `exports/fine_tune.jsonl` 微调大语言模型
- **教育研究**：结构化数据便于学术分析和统计
- **数字分身**：基于语录数据打造张雪峰风格 AI 助手

## AI 集成

### RAG (Retrieval-Augmented Generation)

```bash
python scripts/export-training.py --format rag
# 输出: exports/rag_chunks.jsonl
```

### Fine-tuning

```bash
python scripts/export-training.py --format fine-tune
# 输出: exports/fine_tune.jsonl（Q&A 对话对）
```

## 谁在用它

本仓的 105 条结构化语料被这些项目直接引用或作为数据源（欢迎提 PR 补充）：

| 项目 | 用法 |
|---|---|
| [Eric-Yibo-Shen/zhangxuefeng-skillset](https://github.com/Eric-Yibo-Shen/zhangxuefeng-skillset) | 决策框架 Skill（ClawHub/扣子上架）；README 说明六大分类框架参考本仓，知识内容为社区独立重述（CC BY 4.0） |
| [yhny1001/gaokao-advisor-skills](https://github.com/yhny1001/gaokao-advisor-skills) | Skill 的 `references/` 语料 |
| [JL-GUO/Agent-Skills-is-The-Future](https://github.com/JL-GUO/Agent-Skills-is-The-Future) | `skills/xuefeng-skill/` 语料 |
| [Atlas-did/Moirca](https://github.com/Atlas-did/Moirca) | 后端入库 105 条 JSON 作 RAG 语料 |
| [DCY6/Multimodal-End-to-End-Model-Intelligent-Customer-Service-System](https://github.com/DCY6/Multimodal-End-to-End-Model-Intelligent-Customer-Service-System) | 转成知识库文本 |
| [guxingzyj-stack/my-first-project](https://github.com/guxingzyj-stack/my-first-project) | 风格库外部参考 |

同赛道的其他项目（女娲 skill 版、ASR 语料源等）和**口径差异**见 [docs/COMPARISON.md](docs/COMPARISON.md)。

## 可信度说明

| Level | 含义 | 本仓条数 |
|---|---|---|
| `verified` | 有原始视频/文章来源可查证 | 0 |
| `attributed` | 广泛归属于张雪峰，但无法定位具体出处 | 34 |
| `paraphrased` | 经过转述或总结，非原话 | 71 |

**用之前请明白三件事：**

1. **语料截止 2026-03-25**。张雪峰（1984-11-28 — 2026-03-24）去世次日建仓，本仓收录的是那之前公开流传的言论。此后的政策与就业变化不在语料内，请单独标注。
2. **本仓只有「判断口径」，没有分数线数据**。分数线、位次、招生计划、选科要求、专业目录一律以省考试院与学校招生章程为准——这里不提供，也不会替你猜。
3. **引用时按 confidence 说话**：`attributed` 可写「他说过/他的判断是」，`paraphrased` 要写「他的大意是」，两者都不要加引号当逐字原话。每条 id 可在对应 JSON 中回溯。

## 引用本仓

仓库根目录的 [`CITATION.cff`](CITATION.cff) 会在 GitHub 侧栏生成「Cite this repository」。项目引用建议：

> dongsheng123132. (2026). *gaokao-mentor-wisdom: 张雪峰语录大全 · 高考志愿填报知识库* (v5.1.0) [Data set]. MIT License. https://github.com/dongsheng123132/gaokao-mentor-wisdom

## 贡献

欢迎贡献更多语录！参考 [CONTRIBUTING.md](CONTRIBUTING.md) 和 `data/_template/example.json`。若你的项目引用了本仓、或想补充下游项目，直接开 PR 改「谁在用它」一节。

## License

MIT License - See [LICENSE](LICENSE)

---

**关键词 / Keywords**: 张雪峰, 张雪峰语录, 高考志愿填报, 专业选择, 高考咨询, 志愿填报指南, 高考专业推荐, 985 211 选择, 就业前景分析, 高考生家长必看, Zhang Xuefeng, gaokao, college application, major selection, career guidance, Chinese education
