"""
基础使用示例

演示如何使用 czsc_skills 库中的各种技能
"""

from czsc_skills import SkillRegistry
from czsc_skills.skills import BiRecognitionSkill, SignalGeneratorSkill, FractalDetectorSkill


def example_fractal_detection():
    """
    示例：使用分型识别技能
    """
    print("=" * 50)
    print("分型识别示例")
    print("=" * 50)
    
    # 创建分型识别技能
    skill = FractalDetectorSkill(
        name="分型识别器",
        description="识别K线中的顶底分型",
        include_potential=False
    )
    
    # 准备测试K线数据
    klines = [
        {"dt": "2024-01-01 09:30", "high": 10.5, "low": 10.0, "open": 10.2, "close": 10.3},
        {"dt": "2024-01-01 10:00", "high": 11.0, "low": 10.3, "open": 10.3, "close": 10.8},  # 可能的顶分型
        {"dt": "2024-01-01 10:30", "high": 10.7, "low": 10.2, "open": 10.8, "close": 10.4},
        {"dt": "2024-01-01 11:00", "high": 10.4, "low": 9.8, "open": 10.4, "close": 10.0},
        {"dt": "2024-01-01 11:30", "high": 10.2, "low": 9.5, "open": 10.0, "close": 9.7},  # 可能的底分型
        {"dt": "2024-01-01 13:00", "high": 10.5, "low": 9.7, "open": 9.7, "close": 10.3},
    ]
    
    # 执行分型识别
    result = skill.execute(klines)
    
    print(f"识别结果: {result['message']}")
    print(f"总分型数: {result['count']}")
    print(f"顶分型数: {result['top_count']}")
    print(f"底分型数: {result['bottom_count']}")
    print()


def example_bi_recognition():
    """
    示例：使用笔识别技能
    """
    print("=" * 50)
    print("笔识别示例")
    print("=" * 50)
    
    # 使用技能注册器创建技能实例
    skill = BiRecognitionSkill(
        name="笔识别器",
        min_bi_len=5
    )
    
    # 准备测试K线数据
    klines = [
        {"dt": f"2024-01-01 {i:02d}:00", "high": 10 + i * 0.1, "low": 9.5 + i * 0.1, 
         "open": 9.8 + i * 0.1, "close": 9.9 + i * 0.1}
        for i in range(10)
    ]
    
    # 执行笔识别
    result = skill.execute(klines)
    
    print(f"识别结果: {result['message']}")
    print(f"笔数量: {result['count']}")
    print()


def example_signal_generation():
    """
    示例：使用信号生成技能
    """
    print("=" * 50)
    print("信号生成示例")
    print("=" * 50)
    
    # 创建信号生成技能
    skill = SignalGeneratorSkill(
        name="交易信号生成器",
        signal_type="all"
    )
    
    # 准备测试数据
    data = {
        "klines": [],
        "bis": [],
        "segments": []
    }
    
    # 执行信号生成
    result = skill.execute(data)
    
    print(f"生成结果: {result['message']}")
    print(f"信号类型: {result['signal_type']}")
    print(f"信号数量: {result['count']}")
    print()


def example_skill_registry():
    """
    示例：使用技能注册器管理技能
    """
    print("=" * 50)
    print("技能注册器示例")
    print("=" * 50)
    
    # 列出所有已注册的技能
    skills = SkillRegistry.list_skills()
    print(f"已注册的技能: {skills}")
    print()
    
    # 获取技能信息
    for skill_name in skills:
        info = SkillRegistry.get_skill_info(skill_name)
        print(f"技能名称: {info['name']}")
        print(f"技能类: {info['class']}")
        print(f"模块: {info['module']}")
        print()


if __name__ == "__main__":
    # 运行所有示例
    example_skill_registry()
    example_fractal_detection()
    example_bi_recognition()
    example_signal_generation()
    
    print("所有示例运行完成！")
