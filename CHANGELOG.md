# Changelog

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
