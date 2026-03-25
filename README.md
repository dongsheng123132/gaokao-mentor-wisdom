# 高考名师语录知识库 | Gaokao Mentor Wisdom

> 系统化整理高考名师的智慧语录，为考生和家长提供结构化的备考决策参考。
>
> A structured knowledge base of wisdom from China's top gaokao (college entrance exam) mentors.

## Why / 为什么做这个项目

每年高考季，数百万考生和家长面临专业选择、院校填报的焦虑。张雪峰等名师的建议散落在各个平台的短视频和直播中，难以系统查找。

本项目将这些智慧**结构化**为 JSON 数据，支持：

- 按分类浏览（专业选择、就业前景、人生哲理等）
- 关键词搜索和标签过滤
- AI 应用集成（RAG、Fine-tuning、数字分身）
- 社区协作贡献

## Quick Start / 快速开始

```bash
# Clone
git clone https://github.com/dongsheng123132/gaokao-mentor-wisdom.git
cd gaokao-mentor-wisdom

# Validate data
python scripts/validate.py

# Generate readable docs
python scripts/json2md.py

# Export for AI training
python scripts/export-training.py
```

## Data Structure / 数据结构

```
data/
├── mentors.json              # 名师档案
├── categories.json           # 6 大分类
├── zhangxuefeng/             # 张雪峰语录
│   ├── zhuanye.json          # 🎯 专业选择 (12 quotes)
│   ├── jiuye.json            # 💼 就业前景 (6 quotes)
│   ├── rensheng.json         # 💡 人生哲理 (6 quotes)
│   ├── yuanxiao.json         # 🏫 院校推荐 (2 quotes)
│   ├── xuexi.json            # 📚 学习建议 (2 quotes)
│   └── zhiyuan-celue.json    # 📋 志愿填报策略 (2 quotes)
└── _template/
    └── example.json          # 新名师模板
```

## Categories / 分类

| ID | 中文 | English | Scope |
|---|---|---|---|
| zhuanye | 专业选择 🎯 | Major Selection | 选什么专业、避什么坑 |
| yuanxiao | 院校推荐 🏫 | University Recs | 985/211评价、学校特色 |
| jiuye | 就业前景 💼 | Career Prospects | 行业分析、薪资现实 |
| rensheng | 人生哲理 💡 | Life Philosophy | 阶层、价值观 |
| xuexi | 学习建议 📚 | Study Advice | 学习方法、备考策略 |
| zhiyuan-celue | 志愿填报策略 📋 | Application Strategy | 冲稳保、平行志愿技巧 |

## Quote Format / 数据格式

每条语录 (JSON):

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

Schema: [`schema/quote.schema.json`](schema/quote.schema.json)

## AI Integration / AI 集成

### RAG (Retrieval-Augmented Generation)

```bash
python scripts/export-training.py
# Outputs: exports/rag_chunks.jsonl
```

### Fine-tuning

```bash
python scripts/export-training.py --format fine-tune
# Outputs: exports/fine_tune.jsonl (Q&A pairs)
```

## Confidence Levels / 可信度

| Level | 含义 |
|---|---|
| `verified` | 有原始视频/文章来源可查证 |
| `attributed` | 广泛归属于该名师，但无法定位具体出处 |
| `paraphrased` | 经过转述或总结，非原话 |

## Contributing / 贡献

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

欢迎贡献更多名师语录！参考 `data/_template/example.json` 创建新数据。

## Mentors / 名师

- **张雪峰** (Zhang Xuefeng) — 高考志愿填报咨询师，30 条语录

更多名师持续添加中...

## License

MIT License - See [LICENSE](LICENSE)

---

> "高考是普通人改变命运成本最低的方式，没有之一。" — 张雪峰
