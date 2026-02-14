# 贡献指南

感谢您对 czsc_skills 项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请：

1. 检查 [Issues](https://github.com/zengbin93/czsc_skills/issues) 页面，确保问题尚未被报告
2. 创建新的 Issue，清晰地描述问题或建议
3. 如果是 bug，请提供复现步骤、期望行为和实际行为

### 提交代码

1. **Fork 项目**
   ```bash
   # 在 GitHub 上 Fork 项目
   # 克隆您的 fork
   git clone https://github.com/YOUR_USERNAME/czsc_skills.git
   cd czsc_skills
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **安装开发依赖**
   ```bash
   pip install -e ".[dev]"
   ```

4. **编写代码**
   - 遵循现有的代码风格
   - 添加必要的文档字符串
   - 确保代码通过所有测试

5. **运行测试**
   ```bash
   pytest tests/ -v
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "描述您的更改"
   ```

7. **推送到 GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 清晰地描述您的更改
   - 链接相关的 Issue

## 开发指南

### 创建新技能

1. 在 `czsc_skills/skills/` 目录下创建新的 Python 文件
2. 继承 `BaseSkill` 类
3. 使用 `@SkillRegistry.register` 装饰器注册技能
4. 实现 `execute()` 方法
5. 添加文档字符串和类型注解

示例：

```python
from czsc_skills.base import BaseSkill, SkillRegistry

@SkillRegistry.register
class MySkill(BaseSkill):
    """技能描述"""
    
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
    
    def execute(self, data, **kwargs):
        """执行技能逻辑"""
        # 实现您的逻辑
        return {"result": "success"}
```

### 编写测试

1. 在 `tests/` 目录下创建测试文件
2. 使用 pytest 编写测试用例
3. 确保测试覆盖主要功能和边界情况

### 代码风格

- 使用 4 个空格缩进
- 遵循 PEP 8 规范
- 使用有意义的变量和函数名
- 添加必要的注释和文档字符串
- 中文注释使用 UTF-8 编码

### 文档

- 为新功能添加示例到 `examples/` 目录
- 更新 README.md 相关部分
- 添加详细的文档字符串

## 行为准则

- 尊重他人
- 友善交流
- 建设性反馈
- 专注于代码质量

## 问题？

如有任何问题，请：
- 查看现有的 Issues
- 创建新的 Issue
- 发送邮件至项目维护者

感谢您的贡献！
