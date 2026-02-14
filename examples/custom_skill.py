"""
自定义技能示例

演示如何创建和使用自定义技能
"""

from typing import List, Dict, Any
from czsc_skills.base import BaseSkill, SkillRegistry
# 导入已有技能以确保它们被注册
from czsc_skills.skills import FractalDetectorSkill, BiRecognitionSkill, SignalGeneratorSkill


@SkillRegistry.register
class TrendAnalysisSkill(BaseSkill):
    """
    趋势分析技能
    
    分析K线数据的趋势，判断上涨、下跌或震荡
    """
    
    def __init__(self, name: str = "趋势分析", description: str = "分析市场趋势",
                 window: int = 20, **kwargs):
        """
        初始化趋势分析技能
        
        Args:
            name: 技能名称
            description: 技能描述
            window: 分析窗口大小
            **kwargs: 其他参数
        """
        super().__init__(name, description, **kwargs)
        self.window = window
    
    def execute(self, klines: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """
        执行趋势分析
        
        Args:
            klines: K线数据列表
            **kwargs: 其他参数
            
        Returns:
            趋势分析结果
        """
        if not klines or len(klines) < self.window:
            return {
                "trend": "unknown",
                "strength": 0,
                "message": f"K线数据不足，至少需要 {self.window} 根K线"
            }
        
        # 简单的趋势判断：比较窗口内首尾收盘价
        start_close = klines[-self.window].get("close", 0)
        end_close = klines[-1].get("close", 0)
        
        change_pct = ((end_close - start_close) / start_close * 100) if start_close > 0 else 0
        
        # 判断趋势
        if change_pct > 5:
            trend = "上涨"
            strength = min(change_pct / 10, 1.0)  # 归一化强度
        elif change_pct < -5:
            trend = "下跌"
            strength = min(abs(change_pct) / 10, 1.0)
        else:
            trend = "震荡"
            strength = abs(change_pct) / 5
        
        return {
            "trend": trend,
            "strength": strength,
            "change_pct": round(change_pct, 2),
            "start_price": start_close,
            "end_price": end_close,
            "window": self.window,
            "message": f"趋势: {trend}，变化: {change_pct:.2f}%"
        }
    
    def validate(self) -> bool:
        """验证配置"""
        return self.window > 0


def example_custom_skill():
    """示例：使用自定义技能"""
    print("=" * 50)
    print("自定义技能示例 - 趋势分析")
    print("=" * 50)
    
    # 创建趋势分析技能
    skill = TrendAnalysisSkill(name="趋势分析器", window=10)
    
    # 准备测试数据 - 模拟上涨趋势
    klines = [
        {"dt": f"2024-01-{i+1:02d}", "close": 100 + i * 2}
        for i in range(15)
    ]
    
    # 执行趋势分析
    result = skill.execute(klines)
    
    print(f"分析结果: {result['message']}")
    print(f"趋势类型: {result['trend']}")
    print(f"趋势强度: {result['strength']:.2f}")
    print(f"价格变化: {result['change_pct']}%")
    print()
    
    # 验证技能已注册
    print("已注册的技能:", SkillRegistry.list_skills())
    print()


if __name__ == "__main__":
    example_custom_skill()
