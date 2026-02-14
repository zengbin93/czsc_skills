"""
笔识别技能

基于缠论的笔识别算法，用于识别K线图中的笔结构
笔是缠论中的基本结构单位，由相邻的分型之间的K线序列构成
"""

from typing import List, Dict, Any, Optional
from czsc_skills.base import BaseSkill, SkillRegistry


@SkillRegistry.register
class BiRecognitionSkill(BaseSkill):
    """
    笔识别技能
    
    识别K线数据中的笔结构，笔是缠论技术分析的基础单位
    
    笔的定义：
    1. 顶分型和底分型之间至少包含一根独立K线
    2. 笔的方向由起始分型决定
    3. 相邻两笔方向必须相反
    
    使用示例:
        skill = BiRecognitionSkill(name="笔识别", min_bi_len=5)
        result = skill.execute(klines_data)
    """
    
    def __init__(self, name: str = "笔识别", description: str = "识别K线中的笔结构", 
                 min_bi_len: int = 5, **kwargs):
        """
        初始化笔识别技能
        
        Args:
            name: 技能名称
            description: 技能描述
            min_bi_len: 最小笔长度（K线数量）
            **kwargs: 其他参数
        """
        super().__init__(name, description, **kwargs)
        self.min_bi_len = min_bi_len
        
    def execute(self, klines: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """
        执行笔识别
        
        Args:
            klines: K线数据列表，每个元素是一个字典，包含 open, high, low, close, dt 等字段
            **kwargs: 其他参数
            
        Returns:
            包含识别结果的字典:
            {
                "bis": [...],  # 识别出的笔列表
                "count": int,  # 笔的数量
                "last_bi": {...}  # 最后一笔的信息
            }
        """
        if not klines or len(klines) < self.min_bi_len:
            return {
                "bis": [],
                "count": 0,
                "last_bi": None,
                "message": "K线数据不足，无法识别笔"
            }
        
        # 简化的笔识别逻辑示例
        # 实际应用中需要调用 czsc 库的笔识别函数
        bis = []
        
        # 这里是示例实现，实际需要使用 czsc 库的算法
        # from czsc.analyze import CZSC
        # czsc_obj = CZSC(klines)
        # bis = czsc_obj.bi_list
        
        return {
            "bis": bis,
            "count": len(bis),
            "last_bi": bis[-1] if bis else None,
            "message": f"成功识别 {len(bis)} 笔"
        }
    
    def validate(self) -> bool:
        """
        验证配置
        
        Returns:
            True if valid, False otherwise
        """
        if self.min_bi_len < 3:
            return False
        return True
