# 贡献指南 | Contributing Guide

感谢你对本项目的兴趣！以下是贡献的方式和规范。

## 如何贡献语录

### 1. Fork 本仓库

### 2. 添加语录数据

在 `data/<mentor_name>/` 目录下对应的 JSON 文件中添加新语录。

**语录字段说明：**

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 格式: `{mentor_prefix}-{category}-{number}`，如 `zxf-zhuanye-013` |
| `text` | 是 | 中文原文 |
| `text_en` | 否 | 英文翻译 |
| `context` | 否 | 语录背景和场景 |
| `tags` | 是 | 相关标签数组，至少 1 个 |
| `target_audience` | 否 | 目标受众 |
| `source.platform` | 否 | 来源平台 |
| `source.date` | 否 | 日期 (YYYY-MM-DD) |
| `source.type` | 是 | 内容类型: 直播/短视频/讲座/访谈/文章/书籍 |
| `sentiment` | 否 | 语气: cautionary/encouraging/neutral/humorous/critical |
| `confidence` | 是 | verified/attributed/paraphrased |
| `related_majors` | 否 | 相关专业 |

### 3. 验证数据

```bash
python scripts/validate.py
```

确保所有 JSON 格式正确且符合 schema。

### 4. 提交 PR

- PR 标题简洁描述改动
- 在 PR 描述中说明语录来源

## 添加新名师

1. 在 `data/mentors.json` 中添加名师信息
2. 创建 `data/<mentor_name>/` 目录
3. 参考 `data/_template/example.json` 创建数据文件
4. 至少提供 5 条语录

## 规范

- **准确性**：语录应尽量准确，标注 `confidence` 级别
- **来源**：如有原始来源链接，请在 PR 中注明
- **中立性**：如实记录，不做主观评价
- **格式**：运行 `python scripts/validate.py` 确保 JSON 合法

## 不接受的内容

- 捏造或严重失实的语录
- 包含人身攻击或歧视性内容
- 侵犯他人隐私的内容
- 与高考/教育无关的内容
