# Changelog

## v5.2.1 — 2026-10-29

- 网页版补社交分享卡 `site/og.png`（源文件 `site/og-card.html`，含生成命令）：`og:image` / `twitter:card` / `canonical`，微信、微博、X 分享时有预览图
- 仓库 homepage 指向网页版（GitHub 侧栏「Website」可直接点开）

## v5.2.0 — 2026-10-29

网页版 + AI 检索入口 + CI，数据本身不变（仍为 105 条，截止 2026-03-25）。

- 新增网页版 `site/index.html`（由 `scripts/build-site.py` 从 data 生成）：105 条可搜索、按分类筛选，每条带 id / 出处 / 可信度；部署到 GitHub Pages
- 新增 `llms.txt`：AI 检索入口（语料路径、边界、引用说明）
- 新增 `docs/COMPARISON.md`：与下游 `zhangxuefeng-skillset` 的口径对照（谁更新了什么、冲突怎么裁）
- 新增 CI `.github/workflows/validate.yml`：schema 校验 + docs / site / exports 与 data 的同步检查；PR 会跑
- 新增 `.github/workflows/pages.yml`：Pages 部署；README 加 validate 徽章
- SKILL.md 补两处 2026 版框架的例外（「城市>学校>专业」在理科/执照/高分段让位专业；「宁去大城市 211」的三条破例），并标注「非原话」，与语料分栏

## v5.1.0 — 2026-10-29

Agent Skill 打包与引用治理，数据本身不变（仍为 105 条，截止 2026-03-25）。

- 新增 `SKILL.md`：仓库可直接作为 Agent Skill 安装（`npx skills add dongsheng123132/gaokao-mentor-wisdom`），
  内置五步决策流程（城市 > 学校 > 专业 / 冲稳保 / 风险清单）、语料检索方法、引用规则与硬边界
- 新增 `CITATION.cff`：GitHub 侧栏生成「Cite this repository」
- README：新增安装说明、下游引用墙、「可信度计数 + 数据截止」说明；徽章改为 Agent Skill / 数据截止 / 维护日期
- 清理：旧的 v1–v4 导出与临时文件移入本地 `exports/_archive/`（已 gitignore，不进仓库）；补提交 v5 宣发文案 `exports/social-copy-v5.html`

## v5.0 — 2026-03-25

- 桌面版 + 手机版双版本电子书（HTML / PDF）
- 105 条语录定稿，六大分类（专业选择 28 / 就业 18 / 人生 18 / 院校 16 / 学习 12 / 志愿策略 13）

更早的初始化与扩充提交见 `git log`。
