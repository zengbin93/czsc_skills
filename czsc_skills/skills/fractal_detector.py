"""
分型识别技能

基于缠论的分型识别算法，用于识别K线图中的顶分型和底分型
分型是缠论中最基础的概念，是构成笔和线段的基础
"""

from typing import List, Dict, Any, Optional
from czsc_skills.base import BaseSkill, SkillRegistry


@SkillRegistry.register
class FractalDetectorSkill(BaseSkill):
    """
    分型识别技能
    
    识别K线数据中的顶分型和底分型
    
    分型定义：
    1. 顶分型：第二根K线的高点是三根K线中最高的，低点也是三根K线中最高的
    2. 底分型：第二根K线的低点是三根K线中最低的，高点也是三根K线中最低的
    3. 分型是构成笔的基础元素
    
    使用示例:
        skill = FractalDetectorSkill(name="分型识别", include_potential=False)
        result = skill.execute(klines_data)
    """
    
    def __init__(self, name: str = "分型识别", description: str = "识别K线中的顶底分型",
                 include_potential: bool = False, **kwargs):
        """
        初始化分型识别技能
        
        Args:
            name: 技能名称
            description: 技能描述
            include_potential: 是否包含潜在分型（未确认的分型）
            **kwargs: 其他参数
        """
        super().__init__(name, description, **kwargs)
        self.include_potential = include_potential
        
    def execute(self, klines: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """
        执行分型识别
        
        Args:
            klines: K线数据列表，每个元素是一个字典，包含 high, low 等字段
            **kwargs: 其他参数
            
        Returns:
            包含识别结果的字典:
            {
                "fractals": [...],  # 分型列表
                "top_fractals": [...],  # 顶分型列表
                "bottom_fractals": [...],  # 底分型列表
                "count": int  # 分型总数
            }
        """
        if not klines or len(klines) < 3:
            return {
                "fractals": [],
                "top_fractals": [],
                "bottom_fractals": [],
                "count": 0,
                "message": "K线数据不足，至少需要3根K线"
            }
        
        fractals = []
        top_fractals = []
        bottom_fractals = []
        
        # 简化的分型识别逻辑示例
        # 实际应用中需要调用 czsc 库的分型识别函数
        
        # 遍历K线，识别分型
        for i in range(1, len(klines) - 1):
            prev_k = klines[i - 1]
            curr_k = klines[i]
            next_k = klines[i + 1]
            
            # 识别顶分型
            if (curr_k.get("high", 0) >= prev_k.get("high", 0) and 
                curr_k.get("high", 0) >= next_k.get("high", 0) and
                curr_k.get("low", 0) >= prev_k.get("low", 0) and
                curr_k.get("low", 0) >= next_k.get("low", 0)):
                
                fractal = {
                    "type": "top",
                    "index": i,
                    "dt": curr_k.get("dt"),
                    "high": curr_k.get("high"),
                    "low": curr_k.get("low"),
                }
                fractals.append(fractal)
                top_fractals.append(fractal)
            
            # 识别底分型
            elif (curr_k.get("low", float('inf')) <= prev_k.get("low", float('inf')) and 
                  curr_k.get("low", float('inf')) <= next_k.get("low", float('inf')) and
                  curr_k.get("high", float('inf')) <= prev_k.get("high", float('inf')) and
                  curr_k.get("high", float('inf')) <= next_k.get("high", float('inf'))):
                
                fractal = {
                    "type": "bottom",
                    "index": i,
                    "dt": curr_k.get("dt"),
                    "high": curr_k.get("high"),
                    "low": curr_k.get("low"),
                }
                fractals.append(fractal)
                bottom_fractals.append(fractal)
        
        return {
            "fractals": fractals,
            "top_fractals": top_fractals,
            "bottom_fractals": bottom_fractals,
            "count": len(fractals),
            "top_count": len(top_fractals),
            "bottom_count": len(bottom_fractals),
            "message": f"成功识别 {len(fractals)} 个分型（{len(top_fractals)} 顶分型，{len(bottom_fractals)} 底分型）"
        }
    
    def validate(self) -> bool:
        """
        验证配置
        
        Returns:
            True if valid, False otherwise
        """
        return True
    
    def filter_fractals(self, fractals: List[Dict[str, Any]], 
                        fractal_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        过滤分型
        
        Args:
            fractals: 分型列表
            fractal_type: 分型类型 ("top" 或 "bottom")，None表示不过滤
            
        Returns:
            过滤后的分型列表
        """
        if fractal_type is None:
            return fractals
        
        return [f for f in fractals if f.get("type") == fractal_type]
