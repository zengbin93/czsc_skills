#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例：完整的缠论分析流程演示

这个脚本演示如何使用三个分析脚本完成从数据获取到买卖点分析的完整流程。
注意：这是一个演示脚本，需要有效的 Tushare token 才能运行。

使用方法：
    python example_workflow.py --token YOUR_TUSHARE_TOKEN --ts_code 000001.SZ
"""

import argparse
import os
import sys
from datetime import datetime, timedelta


def run_command(cmd):
    """运行命令并打印"""
    print(f"\n{'=' * 60}")
    print(f"执行命令: {cmd}")
    print(f"{'=' * 60}")
    result = os.system(cmd)
    if result != 0:
        print(f"命令执行失败: {cmd}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='缠论分析完整流程演示')
    parser.add_argument('--token', type=str, required=True, help='Tushare API token')
    parser.add_argument('--ts_code', type=str, default='000001.SZ', help='股票代码，默认 000001.SZ')
    parser.add_argument('--days', type=int, default=180, help='数据天数，默认180天')
    
    args = parser.parse_args()
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)
    
    start_date_str = start_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')
    
    output_file = f"{args.ts_code.replace('.', '_')}_data.csv"
    
    print("\n" + "=" * 60)
    print("缠论分析完整流程演示")
    print("=" * 60)
    print(f"股票代码: {args.ts_code}")
    print(f"数据范围: {start_date_str} - {end_date_str}")
    print(f"输出文件: {output_file}")
    
    # 步骤 1: 获取数据
    print("\n\n步骤 1/3: 获取行情数据")
    cmd1 = (f"python fetch_market_data.py "
            f"--token {args.token} "
            f"--ts_code {args.ts_code} "
            f"--start_date {start_date_str} "
            f"--end_date {end_date_str} "
            f"--output {output_file}")
    run_command(cmd1)
    
    # 步骤 2: 分析缠论结构
    print("\n\n步骤 2/3: 分析缠论结构")
    cmd2 = (f"python analyze_czsc_structure.py "
            f"--input {output_file} "
            f"--symbol {args.ts_code}")
    run_command(cmd2)
    
    # 步骤 3: 分析买卖点信号
    print("\n\n步骤 3/3: 分析买卖点信号")
    cmd3 = (f"python signal_analysis.py "
            f"--input {output_file} "
            f"--symbol {args.ts_code}")
    run_command(cmd3)
    
    print("\n\n" + "=" * 60)
    print("完整流程执行完成！")
    print("=" * 60)
    print(f"\n数据文件已保存: {output_file}")
    print("\n下次可以直接使用保存的数据文件进行分析：")
    print(f"  python analyze_czsc_structure.py --input {output_file} --symbol {args.ts_code}")
    print(f"  python signal_analysis.py --input {output_file} --symbol {args.ts_code}")


if __name__ == '__main__':
    main()
