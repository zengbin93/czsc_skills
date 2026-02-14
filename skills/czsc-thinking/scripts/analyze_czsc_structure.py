#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调用 czsc 库的 CZSC 对象分析行情数据的缠论结构

这个脚本演示如何使用 CZSC 对象分析K线数据，识别分型、笔、线段等缠论结构。

使用方法：
    python analyze_czsc_structure.py --input data.csv --symbol 000001.SZ

依赖：
    pip install czsc pandas
"""

import argparse
import pandas as pd
from czsc import CZSC
from czsc.objects import RawBar
from datetime import datetime


def load_data_from_csv(filepath):
    """
    从 CSV 文件加载数据
    
    参数：
        filepath: str, CSV 文件路径
    
    返回：
        DataFrame: 包含行情数据的 DataFrame
    """
    print(f"正在从 {filepath} 加载数据...")
    df = pd.read_csv(filepath)
    print(f"成功加载 {len(df)} 条记录")
    return df


def convert_to_raw_bars(df, symbol):
    """
    将 DataFrame 转换为 RawBar 对象列表
    
    参数：
        df: DataFrame, 包含 OHLCV 数据
        symbol: str, 股票代码
    
    返回：
        list: RawBar 对象列表
    """
    print("正在转换数据格式...")
    
    raw_bars = []
    for _, row in df.iterrows():
        # 处理日期格式
        trade_date = str(row['trade_date'])
        if len(trade_date) == 8:  # YYYYMMDD 格式
            dt = pd.to_datetime(trade_date, format='%Y%m%d')
        else:
            dt = pd.to_datetime(trade_date)
        
        bar = RawBar(
            symbol=symbol,
            id=len(raw_bars),
            dt=dt,
            open=float(row['open']),
            close=float(row['close']),
            high=float(row['high']),
            low=float(row['low']),
            vol=float(row.get('vol', 0)),
            amount=float(row.get('amount', 0))
        )
        raw_bars.append(bar)
    
    print(f"成功转换 {len(raw_bars)} 条数据")
    return raw_bars


def analyze_structure(czsc_obj):
    """
    分析缠论结构
    
    参数：
        czsc_obj: CZSC 对象
    """
    print("\n" + "=" * 60)
    print("缠论结构分析")
    print("=" * 60)
    
    # 基本信息
    print(f"\n股票代码：{czsc_obj.symbol}")
    print(f"分析周期：{czsc_obj.freq}")
    print(f"K线数量：{len(czsc_obj.bars_raw)}")
    
    # 分型分析
    print(f"\n分型数量：{len(czsc_obj.fx_list)}")
    if czsc_obj.fx_list:
        print("\n最近 5 个分型：")
        for fx in czsc_obj.fx_list[-5:]:
            print(f"  {fx.dt.strftime('%Y-%m-%d')} - {fx.mark} - 价格: {fx.fx}")
    
    # 笔分析
    print(f"\n笔数量：{len(czsc_obj.bi_list)}")
    if czsc_obj.bi_list:
        print("\n最近 5 笔：")
        for bi in czsc_obj.bi_list[-5:]:
            direction = "向上" if bi.direction == "up" else "向下"
            print(f"  {bi.fx_a.dt.strftime('%Y-%m-%d')} -> {bi.fx_b.dt.strftime('%Y-%m-%d')}: "
                  f"{direction} - {bi.fx_a.fx:.2f} -> {bi.fx_b.fx:.2f} "
                  f"(幅度: {abs(bi.fx_b.fx - bi.fx_a.fx):.2f})")
    
    # 线段分析
    if hasattr(czsc_obj, 'xd_list') and czsc_obj.xd_list:
        print(f"\n线段数量：{len(czsc_obj.xd_list)}")
        print("\n最近 3 个线段：")
        for xd in czsc_obj.xd_list[-3:]:
            direction = "向上" if xd.direction == "up" else "向下"
            print(f"  {xd.start.dt.strftime('%Y-%m-%d')} -> {xd.end.dt.strftime('%Y-%m-%d')}: "
                  f"{direction}")
    
    # 当前状态
    print("\n当前状态：")
    if czsc_obj.bi_list:
        last_bi = czsc_obj.bi_list[-1]
        print(f"  最后一笔方向：{'向上' if last_bi.direction == 'up' else '向下'}")
        print(f"  最后一笔价格：{last_bi.fx_a.fx:.2f} -> {last_bi.fx_b.fx:.2f}")
    
    # 获取信号（如果有）
    if hasattr(czsc_obj, 'signals') and czsc_obj.signals:
        print("\n当前信号：")
        for key, value in czsc_obj.signals.items():
            print(f"  {key}: {value}")


def main():
    parser = argparse.ArgumentParser(description='分析股票数据的缠论结构')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件（CSV格式）')
    parser.add_argument('--symbol', type=str, required=True, help='股票代码')
    parser.add_argument('--freq', type=str, default='日线', help='分析周期，默认为日线')
    parser.add_argument('--max_bi', type=int, default=20, help='最大笔数量，默认 20')
    
    args = parser.parse_args()
    
    # 加载数据
    df = load_data_from_csv(args.input)
    
    # 转换为 RawBar
    raw_bars = convert_to_raw_bars(df, args.symbol)
    
    # 创建 CZSC 对象
    print(f"\n正在创建 CZSC 对象（周期：{args.freq}）...")
    czsc_obj = CZSC(raw_bars, freq=args.freq, max_bi_num=args.max_bi)
    
    # 分析结构
    analyze_structure(czsc_obj)
    
    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
