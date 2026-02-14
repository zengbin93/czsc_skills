# czsc_skills

缠论（缠中说禅）技能库 - 基于 waditu/czsc 库的 Claude Skills

## 简介

这是一个围绕 [waditu/czsc](https://github.com/waditu/czsc) 库核心内容构建的 Claude Skills 仓库。通过 SKILL.md 格式的技能文件，帮助 Claude 更好地理解和应用缠论（缠中说禅理论）进行量化交易分析。

### 什么是缠论？

缠论（缠中说禅理论）是一套结构化的技术分析方法论，通过识别市场结构（分型、笔、线段、中枢等）来进行交易决策。核心理念是"不测而测"，即不预测市场方向，而是根据市场结构的变化做出反应。

### 什么是 Skills？

Skills 是包含指令、脚本和资源的文件夹，Claude 可以动态加载以提升在特定任务上的表现。每个 skill 通过 SKILL.md 文件提供结构化的指导。

## 技能列表

本仓库提供以下缠论相关技能：

### 1. czsc-thinking - 缠论思维技能

教导 AI 代理如何以缠论原文的方式分析交易机会和市场。该技能采用模块化结构：

**核心文件：**
- `SKILL.md` - 简洁的技能指令文件（141行），包含核心思维框架和分析流程

**参考资料：**
- `references/chan-theory-core.md` - 完整的缠论核心理论，包括哲学、方法论和金句精选

**使用示例：**
- `examples/usage-scenarios.md` - 实战场景示例，包括股票分析、大盘研判、策略制定等

**实用脚本：**
1. **fetch_market_data.py** - 通过 Tushare 获取行情数据
2. **analyze_czsc_structure.py** - 调用 CZSC 对象分析缠论结构（分型、笔、线段等）
3. **signal_analysis.py** - 调用信号函数辅助分析买卖点、背驰和趋势

详细使用说明请参考：[scripts/README.md](skills/czsc-thinking/scripts/README.md)

## 使用方法

### 在 Claude.ai 中使用

1. 访问 [Claude.ai](https://claude.ai)
2. 上传任一技能文件夹或打包的 .skill 文件
3. 在对话中引用该技能来分析K线数据

### 在 Claude Code 中使用

```bash
# 克隆仓库
git clone https://github.com/zengbin93/czsc_skills.git

# 在 Claude Code 中引用技能
/plugin add ./czsc_skills
```

### 在 API 中使用

参考 [Skills API 文档](https://docs.claude.com/en/api/skills-guide)

## 技能结构

每个技能遵循 Anthropic Agent Skills 标准：

```
skill-name/
├── SKILL.md              # 必需：包含 YAML frontmatter 和 Markdown 指令（建议<150行）
├── scripts/              # 可选：可执行脚本
├── references/           # 可选：参考文档和深度理论内容
├── examples/             # 可选：使用场景示例
└── assets/              # 可选：模板和资源文件
```

**最佳实践：**
- SKILL.md 应保持简洁，聚焦于核心指令和思维框架
- 将详细的理论内容移至 `references/` 目录
- 将使用场景和案例移至 `examples/` 目录
- 将可执行工具移至 `scripts/` 目录

## 创建自定义技能

使用 `skill-creator` 技能来创建新的缠论技能：

1. 确定技能用途和具体场景
2. 规划可复用的脚本、参考文档和资源
3. 创建 SKILL.md 文件
4. 添加必要的脚本和参考资料
5. 测试和迭代

## 依赖

本仓库中的技能基于以下库：

- [waditu/czsc](https://github.com/waditu/czsc) - 缠中说禅技术分析工具
- Python >= 3.8
- pandas, numpy 等数据分析库

## 许可证

MIT License

## 相关资源

- [waditu/czsc](https://github.com/waditu/czsc) - 缠论技术分析工具
- [Anthropic Skills](https://github.com/anthropics/skills) - Agent Skills 标准
- [Agent Skills 规范](http://agentskills.io)
