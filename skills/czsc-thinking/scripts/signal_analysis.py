#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调用合适的信号函数辅助分析行情买卖点

这个脚本演示如何使用 czsc 库的信号函数分析买卖点。

使用方法：
    python signal_analysis.py --input data.csv --symbol 000001.SZ

依赖：
    pip install czsc pandas
"""

import argparse
import pandas as pd
from czsc import CZSC, RawBar, Freq, Direction
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
        trade_date = str(int(float(row['trade_date']))) if '.' in str(row['trade_date']) else str(row['trade_date'])
        if len(trade_date) == 8:  # YYYYMMDD 格式
            dt = pd.to_datetime(trade_date, format='%Y%m%d')
        else:
            dt = pd.to_datetime(trade_date)
        
        bar = RawBar(
            symbol=symbol,
            dt=dt,
            freq=Freq.D,
            open=float(row['open']),
            close=float(row['close']),
            high=float(row['high']),
            low=float(row['low']),
            vol=float(row.get('vol', 0)),
            amount=float(row.get('amount', 0)),
            id=len(raw_bars)
        )
        raw_bars.append(bar)
    
    print(f"成功转换 {len(raw_bars)} 条数据")
    return raw_bars


def analyze_buy_sell_points(czsc_obj):
    """
    分析买卖点
    
    参数：
        czsc_obj: CZSC 对象
    """
    print("\n" + "=" * 60)
    print("买卖点分析")
    print("=" * 60)
    
    # 分析笔的买卖点
    if czsc_obj.bi_list and len(czsc_obj.bi_list) >= 3:
        print("\n基于笔的买卖点分析：")
        
        # 分析最近的笔
        recent_bis = czsc_obj.bi_list[-5:]
        
        for i, bi in enumerate(recent_bis):
            direction = str(bi.direction)
            
            # 判断是否为潜在买点（向上笔的起点）
            if bi.direction == Direction.Up:
                print(f"\n潜在买点 {i+1}:")
                print(f"  时间：{bi.fx_a.dt.strftime('%Y-%m-%d')}")
                print(f"  价格：{bi.fx_a.fx:.2f}")
                print(f"  类型：{bi.fx_a.mark}分型")
                
                # 判断买点类型
                if i >= 2:
                    prev_bi = recent_bis[i-2]
                    if prev_bi.direction == Direction.Up and bi.fx_a.fx > prev_bi.fx_a.fx:
                        print(f"  特征：回调不破前低（可能是二买）")
                    elif bi.fx_a.fx < prev_bi.fx_a.fx:
                        print(f"  特征：创新低后反弹（可能是一买）")
            
            # 判断是否为潜在卖点（向下笔的起点）
            elif bi.direction == Direction.Down:
                print(f"\n潜在卖点 {i+1}:")
                print(f"  时间：{bi.fx_a.dt.strftime('%Y-%m-%d')}")
                print(f"  价格：{bi.fx_a.fx:.2f}")
                print(f"  类型：{bi.fx_a.mark}分型")
                
                # 判断卖点类型
                if i >= 2:
                    prev_bi = recent_bis[i-2]
                    if prev_bi.direction == Direction.Down and bi.fx_a.fx < prev_bi.fx_a.fx:
                        print(f"  特征：反弹不过前高（可能是二卖）")
                    elif bi.fx_a.fx > prev_bi.fx_a.fx:
                        print(f"  特征：创新高后回落（可能是一卖）")


def analyze_divergence(czsc_obj):
    """
    分析背驰
    
    参数：
        czsc_obj: CZSC 对象
    """
    print("\n" + "=" * 60)
    print("背驰分析")
    print("=" * 60)
    
    if czsc_obj.bi_list and len(czsc_obj.bi_list) >= 3:
        # 比较最近两笔的强度
        recent_bis = czsc_obj.bi_list[-3:]
        
        if len(recent_bis) >= 2:
            bi1 = recent_bis[-2]
            bi2 = recent_bis[-1]
            
            # 计算笔的幅度
            amp1 = abs(bi1.fx_b.fx - bi1.fx_a.fx)
            amp2 = abs(bi2.fx_b.fx - bi2.fx_a.fx)
            
            print(f"\n最近两笔比较：")
            print(f"  前一笔（{bi1.fx_a.dt.strftime('%Y-%m-%d')} -> {bi1.fx_b.dt.strftime('%Y-%m-%d')}）：")
            print(f"    方向：{str(bi1.direction)}")
            print(f"    幅度：{amp1:.2f}")
            
            print(f"  最后一笔（{bi2.fx_a.dt.strftime('%Y-%m-%d')} -> {bi2.fx_b.dt.strftime('%Y-%m-%d')}）：")
            print(f"    方向：{str(bi2.direction)}")
            print(f"    幅度：{amp2:.2f}")
            
            # 判断背驰
            if bi1.direction == bi2.direction:
                if bi1.direction == Direction.Up:
                    if bi2.fx_b.fx > bi1.fx_b.fx and amp2 < amp1:
                        print(f"\n  ⚠️ 可能存在上涨背驰：价格创新高但幅度减小")
                        print(f"  建议：关注卖点")
                elif bi1.direction == Direction.Down:
                    if bi2.fx_b.fx < bi1.fx_b.fx and amp2 < amp1:
                        print(f"\n  ⚠️ 可能存在下跌背驰：价格创新低但幅度减小")
                        print(f"  建议：关注买点")


def analyze_trend(czsc_obj):
    """
    分析趋势
    
    参数：
        czsc_obj: CZSC 对象
    """
    print("\n" + "=" * 60)
    print("趋势分析")
    print("=" * 60)
    
    if czsc_obj.bi_list and len(czsc_obj.bi_list) >= 3:
        # 分析最近几笔的高低点
        recent_bis = czsc_obj.bi_list[-5:]
        
        # 提取高点和低点
        highs = [bi.fx_b.fx for bi in recent_bis if bi.direction == Direction.Up]
        lows = [bi.fx_b.fx for bi in recent_bis if bi.direction == Direction.Down]
        
        print(f"\n最近笔的高低点分析：")
        
        # 判断趋势
        if len(highs) >= 2:
            if highs[-1] > highs[0]:
                print(f"  高点趋势：上升（{highs[0]:.2f} -> {highs[-1]:.2f}）")
            else:
                print(f"  高点趋势：下降（{highs[0]:.2f} -> {highs[-1]:.2f}）")
        
        if len(lows) >= 2:
            if lows[-1] > lows[0]:
                print(f"  低点趋势：上升（{lows[0]:.2f} -> {lows[-1]:.2f}）")
            else:
                print(f"  低点趋势：下降（{lows[0]:.2f} -> {lows[-1]:.2f}）")
        
        # 综合判断
        if len(highs) >= 2 and len(lows) >= 2:
            if highs[-1] > highs[0] and lows[-1] > lows[0]:
                print(f"\n  整体趋势：📈 上升趋势")
                print(f"  操作建议：逢低买入，持有为主")
            elif highs[-1] < highs[0] and lows[-1] < lows[0]:
                print(f"\n  整体趋势：📉 下降趋势")
                print(f"  操作建议：逢高卖出，空仓为主")
            else:
                print(f"\n  整体趋势：📊 震荡趋势")
                print(f"  操作建议：高抛低吸，区间操作")


def main():
    parser = argparse.ArgumentParser(description='分析股票的买卖点信号')
    parser.add_argument('--input', type=str, required=True, help='输入数据文件（CSV格式）')
    parser.add_argument('--symbol', type=str, required=True, help='股票代码')
    parser.add_argument('--freq', type=str, default='日线', help='分析周期，默认为日线')
    
    args = parser.parse_args()
    
    # 加载数据
    df = load_data_from_csv(args.input)
    
    # 转换为 RawBar
    raw_bars = convert_to_raw_bars(df, args.symbol)
    
    # 创建 CZSC 对象
    print(f"\n正在创建 CZSC 对象（周期：{args.freq}）...")
    czsc_obj = CZSC(raw_bars)
    
    # 分析买卖点
    analyze_buy_sell_points(czsc_obj)
    
    # 分析背驰
    analyze_divergence(czsc_obj)
    
    # 分析趋势
    analyze_trend(czsc_obj)
    
    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
