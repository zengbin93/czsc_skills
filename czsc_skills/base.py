"""
基础技能类和技能注册器

提供所有技能的基类和统一的技能注册管理机制
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import inspect


class BaseSkill(ABC):
    """
    技能基类
    
    所有技能都应该继承此类，并实现 execute 方法
    """
    
    def __init__(self, name: str, description: str = "", **kwargs):
        """
        初始化技能
        
        Args:
            name: 技能名称
            description: 技能描述
            **kwargs: 其他参数
        """
        self.name = name
        self.description = description
        self.config = kwargs
        
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        执行技能
        
        子类必须实现此方法
        
        Returns:
            技能执行结果
        """
        pass
    
    def validate(self) -> bool:
        """
        验证技能配置是否正确
        
        Returns:
            True if valid, False otherwise
        """
        return True
    
    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name})"
    
    def __repr__(self):
        return self.__str__()


class SkillRegistry:
    """
    技能注册器
    
    用于注册和管理所有可用的技能
    """
    
    _skills: Dict[str, type] = {}
    
    @classmethod
    def register(cls, skill_class: type) -> type:
        """
        注册技能类
        
        Args:
            skill_class: 技能类
            
        Returns:
            技能类（用于装饰器）
        """
        if not issubclass(skill_class, BaseSkill):
            raise TypeError(f"{skill_class.__name__} must be a subclass of BaseSkill")
        
        skill_name = skill_class.__name__
        if skill_name in cls._skills:
            raise ValueError(f"Skill {skill_name} already registered")
        
        cls._skills[skill_name] = skill_class
        return skill_class
    
    @classmethod
    def get_skill(cls, name: str) -> Optional[type]:
        """
        获取技能类
        
        Args:
            name: 技能名称
            
        Returns:
            技能类，如果不存在返回 None
        """
        return cls._skills.get(name)
    
    @classmethod
    def list_skills(cls) -> List[str]:
        """
        列出所有已注册的技能
        
        Returns:
            技能名称列表
        """
        return list(cls._skills.keys())
    
    @classmethod
    def create_skill(cls, name: str, **kwargs) -> Optional[BaseSkill]:
        """
        创建技能实例
        
        Args:
            name: 技能名称
            **kwargs: 技能初始化参数
            
        Returns:
            技能实例，如果技能不存在返回 None
        """
        skill_class = cls.get_skill(name)
        if skill_class is None:
            return None
        
        return skill_class(**kwargs)
    
    @classmethod
    def get_skill_info(cls, name: str) -> Optional[Dict[str, Any]]:
        """
        获取技能信息
        
        Args:
            name: 技能名称
            
        Returns:
            技能信息字典
        """
        skill_class = cls.get_skill(name)
        if skill_class is None:
            return None
        
        return {
            "name": name,
            "class": skill_class.__name__,
            "doc": skill_class.__doc__,
            "module": skill_class.__module__,
        }
