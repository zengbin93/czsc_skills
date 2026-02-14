"""
信号生成技能

基于缠论的信号生成器，用于生成交易信号
信号是缠论量化交易策略的核心组成部分
"""

from typing import List, Dict, Any, Optional
from czsc_skills.base import BaseSkill, SkillRegistry


@SkillRegistry.register
class SignalGeneratorSkill(BaseSkill):
    """
    信号生成技能
    
    根据K线数据、笔、线段等缠论要素生成交易信号
    
    信号类型包括：
    1. 买卖点信号：识别缠论买卖点
    2. 趋势信号：判断市场趋势方向
    3. 背驰信号：识别背驰形态
    
    使用示例:
        skill = SignalGeneratorSkill(name="信号生成器", signal_type="买卖点")
        signals = skill.execute(czsc_obj)
    """
    
    def __init__(self, name: str = "信号生成器", description: str = "生成缠论交易信号",
                 signal_type: str = "all", **kwargs):
        """
        初始化信号生成技能
        
        Args:
            name: 技能名称
            description: 技能描述
            signal_type: 信号类型 ("买卖点", "趋势", "背驰", "all")
            **kwargs: 其他参数
        """
        super().__init__(name, description, **kwargs)
        self.signal_type = signal_type
        
    def execute(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        执行信号生成
        
        Args:
            data: 输入数据，可以是 czsc 对象或包含必要信息的字典
            **kwargs: 其他参数
            
        Returns:
            包含生成的信号字典:
            {
                "signals": [...],  # 信号列表
                "count": int,  # 信号数量
                "latest_signal": {...}  # 最新信号
            }
        """
        signals = []
        
        # 这里是示例实现，实际需要使用 czsc 库的信号函数
        # from czsc.signals import get_default_signals
        # signals = get_default_signals(czsc_obj)
        
        # 根据信号类型过滤
        if self.signal_type != "all":
            signals = [s for s in signals if s.get("type") == self.signal_type]
        
        return {
            "signals": signals,
            "count": len(signals),
            "latest_signal": signals[-1] if signals else None,
            "signal_type": self.signal_type,
            "message": f"成功生成 {len(signals)} 个信号"
        }
    
    def validate(self) -> bool:
        """
        验证配置
        
        Returns:
            True if valid, False otherwise
        """
        valid_types = ["买卖点", "趋势", "背驰", "all"]
        return self.signal_type in valid_types
    
    def get_signal_summary(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        获取信号摘要
        
        Args:
            signals: 信号列表
            
        Returns:
            信号摘要统计
        """
        summary = {
            "total": len(signals),
            "buy_signals": 0,
            "sell_signals": 0,
            "neutral_signals": 0,
        }
        
        for signal in signals:
            direction = signal.get("direction", "neutral")
            if direction == "buy":
                summary["buy_signals"] += 1
            elif direction == "sell":
                summary["sell_signals"] += 1
            else:
                summary["neutral_signals"] += 1
        
        return summary
