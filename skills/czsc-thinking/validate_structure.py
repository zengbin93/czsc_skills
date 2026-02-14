#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证 czsc-thinking 技能的重构结构

此脚本验证：
1. SKILL.md 文件存在且格式正确
2. references 目录存在且包含正确的文件
3. examples 目录存在且包含正确的文件
4. SKILL.md 中的引用链接正确
"""

import os
import sys
from pathlib import Path


def validate_structure():
    """验证技能目录结构"""
    skill_dir = Path(__file__).parent
    
    print("=" * 60)
    print("验证 czsc-thinking 技能重构结构")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. 验证 SKILL.md 存在
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md 文件不存在")
    else:
        print("✓ SKILL.md 存在")
        
        # 读取文件一次，同时获取行数和内容
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.count('\n') + 1
        print(f"  行数: {lines}")
        
        if lines > 200:
            warnings.append(f"SKILL.md 文件行数({lines})偏多，建议控制在150行以内")
            
        if "references/chan-theory-core.md" not in content:
            errors.append("SKILL.md 中缺少对 references/chan-theory-core.md 的引用")
        else:
            print("✓ SKILL.md 包含对 references/chan-theory-core.md 的引用")
            
        if "examples/usage-scenarios.md" not in content:
            errors.append("SKILL.md 中缺少对 examples/usage-scenarios.md 的引用")
        else:
            print("✓ SKILL.md 包含对 examples/usage-scenarios.md 的引用")
    
    # 2. 验证 references 目录
    ref_dir = skill_dir / "references"
    if not ref_dir.exists():
        errors.append("references 目录不存在")
    else:
        print("✓ references 目录存在")
        
        # 检查 chan-theory-core.md
        chan_theory = ref_dir / "chan-theory-core.md"
        if not chan_theory.exists():
            errors.append("references/chan-theory-core.md 文件不存在")
        else:
            print("✓ references/chan-theory-core.md 存在")
            with open(chan_theory, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            print(f"  行数: {lines}")
    
    # 3. 验证 examples 目录
    examples_dir = skill_dir / "examples"
    if not examples_dir.exists():
        errors.append("examples 目录不存在")
    else:
        print("✓ examples 目录存在")
        
        # 检查 usage-scenarios.md
        usage = examples_dir / "usage-scenarios.md"
        if not usage.exists():
            errors.append("examples/usage-scenarios.md 文件不存在")
        else:
            print("✓ examples/usage-scenarios.md 存在")
            with open(usage, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            print(f"  行数: {lines}")
    
    # 4. 验证 scripts 目录
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        errors.append("scripts 目录不存在")
    else:
        print("✓ scripts 目录存在")
        
        required_scripts = [
            "fetch_market_data.py",
            "analyze_czsc_structure.py", 
            "signal_analysis.py",
            "README.md"
        ]
        
        for script in required_scripts:
            script_path = scripts_dir / script
            if not script_path.exists():
                errors.append(f"scripts/{script} 文件不存在")
            else:
                print(f"✓ scripts/{script} 存在")
    
    # 输出结果
    print("\n" + "=" * 60)
    print("验证结果")
    print("=" * 60)
    
    if errors:
        print("\n❌ 发现以下错误:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\n⚠️  警告:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("\n✓ 所有检查通过！技能结构重构成功。")
        return 0
    elif not errors:
        print("\n✓ 结构验证通过（有一些警告）")
        return 0
    else:
        print("\n❌ 验证失败")
        return 1


if __name__ == "__main__":
    sys.exit(validate_structure())
