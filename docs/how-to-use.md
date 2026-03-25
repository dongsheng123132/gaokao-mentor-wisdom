# 使用指南 | How to Use

## 浏览语录

### 方式一：直接阅读 JSON

所有语录存储在 `data/` 目录下，按名师和分类组织。

### 方式二：生成 Markdown 文档

```bash
python scripts/json2md.py
```

生成的文档在 `docs/<mentor>/` 目录下，更适合阅读。

### 方式三：AI 集成

导出为 AI 友好格式：

```bash
# RAG chunks (用于检索增强生成)
python scripts/export-training.py

# Fine-tuning pairs (用于微调)
python scripts/export-training.py --format fine-tune
```

## 数据 Schema

详见 `schema/quote.schema.json`，所有数据文件必须符合此 schema。

验证方法：

```bash
python scripts/validate.py
```

## 搜索语录

使用标签 (`tags`) 字段进行语录检索。常用标签包括：

- 专业相关：`金融`、`计算机`、`医学`、`土木工程`
- 主题相关：`就业`、`考公`、`家境`、`985`、`211`
- 受众相关：`高考生`、`家长`、`大学生`
