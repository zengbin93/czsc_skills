"""
czsc_skills - 缠中说禅技术分析技能库

基于 waditu/czsc 库的量化交易策略技能模板
提供可复用的技能模块，用于构建缠论量化交易策略
"""

__version__ = "0.1.0"
__author__ = "zengbin93"

from czsc_skills.base import BaseSkill, SkillRegistry

__all__ = ["BaseSkill", "SkillRegistry"]
