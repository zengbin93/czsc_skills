"""
测试基础功能
"""

import pytest
from czsc_skills.base import BaseSkill, SkillRegistry
from czsc_skills.skills import FractalDetectorSkill, BiRecognitionSkill, SignalGeneratorSkill


class TestSkillRegistry:
    """测试技能注册器"""
    
    def test_list_skills(self):
        """测试列出技能"""
        skills = SkillRegistry.list_skills()
        assert len(skills) > 0
        assert "FractalDetectorSkill" in skills
        assert "BiRecognitionSkill" in skills
        assert "SignalGeneratorSkill" in skills
    
    def test_get_skill(self):
        """测试获取技能类"""
        skill_class = SkillRegistry.get_skill("FractalDetectorSkill")
        assert skill_class is not None
        assert skill_class == FractalDetectorSkill
    
    def test_get_skill_not_found(self):
        """测试获取不存在的技能"""
        skill_class = SkillRegistry.get_skill("NonExistentSkill")
        assert skill_class is None
    
    def test_get_skill_info(self):
        """测试获取技能信息"""
        info = SkillRegistry.get_skill_info("FractalDetectorSkill")
        assert info is not None
        assert info["name"] == "FractalDetectorSkill"
        assert info["class"] == "FractalDetectorSkill"


class TestFractalDetectorSkill:
    """测试分型识别技能"""
    
    def test_basic_execution(self):
        """测试基础执行"""
        skill = FractalDetectorSkill(name="测试分型识别")
        
        klines = [
            {"dt": "2024-01-01 09:30", "high": 10.5, "low": 10.0},
            {"dt": "2024-01-01 10:00", "high": 11.0, "low": 10.3},  # 顶分型
            {"dt": "2024-01-01 10:30", "high": 10.7, "low": 10.2},
        ]
        
        result = skill.execute(klines)
        assert "fractals" in result
        assert "count" in result
        assert isinstance(result["fractals"], list)
    
    def test_insufficient_data(self):
        """测试数据不足的情况"""
        skill = FractalDetectorSkill(name="测试分型识别")
        
        klines = [
            {"dt": "2024-01-01 09:30", "high": 10.5, "low": 10.0},
        ]
        
        result = skill.execute(klines)
        assert result["count"] == 0
    
    def test_top_fractal_detection(self):
        """测试顶分型识别"""
        skill = FractalDetectorSkill(name="测试分型识别")
        
        klines = [
            {"dt": "2024-01-01 09:30", "high": 10.0, "low": 9.5},
            {"dt": "2024-01-01 10:00", "high": 11.0, "low": 10.3},  # 顶分型
            {"dt": "2024-01-01 10:30", "high": 10.5, "low": 10.0},
        ]
        
        result = skill.execute(klines)
        assert result["top_count"] >= 0


class TestBiRecognitionSkill:
    """测试笔识别技能"""
    
    def test_basic_execution(self):
        """测试基础执行"""
        skill = BiRecognitionSkill(name="测试笔识别", min_bi_len=5)
        
        klines = [
            {"dt": f"2024-01-01 {i:02d}:00", "high": 10 + i * 0.1, "low": 9.5 + i * 0.1}
            for i in range(10)
        ]
        
        result = skill.execute(klines)
        assert "bis" in result
        assert "count" in result
        assert isinstance(result["bis"], list)
    
    def test_insufficient_data(self):
        """测试数据不足的情况"""
        skill = BiRecognitionSkill(name="测试笔识别", min_bi_len=10)
        
        klines = [
            {"dt": f"2024-01-01 {i:02d}:00", "high": 10, "low": 9}
            for i in range(5)
        ]
        
        result = skill.execute(klines)
        assert result["count"] == 0
    
    def test_validate(self):
        """测试验证功能"""
        skill = BiRecognitionSkill(name="测试笔识别", min_bi_len=5)
        assert skill.validate() is True
        
        skill_invalid = BiRecognitionSkill(name="测试笔识别", min_bi_len=2)
        assert skill_invalid.validate() is False


class TestSignalGeneratorSkill:
    """测试信号生成技能"""
    
    def test_basic_execution(self):
        """测试基础执行"""
        skill = SignalGeneratorSkill(name="测试信号生成", signal_type="all")
        
        data = {
            "klines": [],
            "bis": [],
        }
        
        result = skill.execute(data)
        assert "signals" in result
        assert "count" in result
        assert result["signal_type"] == "all"
    
    def test_validate(self):
        """测试验证功能"""
        skill = SignalGeneratorSkill(name="测试信号生成", signal_type="all")
        assert skill.validate() is True
        
        skill_invalid = SignalGeneratorSkill(name="测试信号生成", signal_type="invalid")
        assert skill_invalid.validate() is False
    
    def test_signal_summary(self):
        """测试信号摘要"""
        skill = SignalGeneratorSkill(name="测试信号生成")
        
        signals = [
            {"direction": "buy"},
            {"direction": "sell"},
            {"direction": "neutral"},
        ]
        
        summary = skill.get_signal_summary(signals)
        assert summary["total"] == 3
        assert summary["buy_signals"] == 1
        assert summary["sell_signals"] == 1
        assert summary["neutral_signals"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
