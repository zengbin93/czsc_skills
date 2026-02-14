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

1. **czsc-thinking** - 缠论思维技能：教导如何以缠论原文的方式分析交易机会和市场，包含完整的缠论分析脚本工具

### czsc-thinking 脚本工具

czsc-thinking 技能包含三个实用的 Python 脚本，演示了完整的缠论分析流程：

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
├── SKILL.md              # 必需：包含 YAML frontmatter 和 Markdown 指令
├── scripts/              # 可选：可执行脚本
├── references/           # 可选：参考文档
└── assets/              # 可选：模板和资源文件
```

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
