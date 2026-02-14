#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通过 Tushare 获取行情数据

这个脚本演示如何使用 Tushare API 获取股票行情数据。
需要先设置 Tushare token 才能使用。

使用方法：
    python fetch_market_data.py --token YOUR_TOKEN --ts_code 000001.SZ --start_date 20240101 --end_date 20240614

依赖：
    pip install czsc tushare pandas
"""

import argparse
from czsc import DataClient
from datetime import datetime


def fetch_stock_data(token, ts_code, start_date, end_date, cache_path=None):
    """
    获取股票日线数据
    
    参数：
        token: str, Tushare API token
        ts_code: str, 股票代码，如 '000001.SZ'
        start_date: str, 开始日期，格式 'YYYYMMDD'
        end_date: str, 结束日期，格式 'YYYYMMDD'
        cache_path: str, 缓存路径，默认为 None
    
    返回：
        DataFrame: 包含 OHLCV 数据的 DataFrame
    """
    # 初始化 DataClient
    if cache_path is None:
        cache_path = "./.tushare_cache"
    
    pro = DataClient(
        url="https://api.tushare.pro",
        token=token,
        cache_path=cache_path,
        timeout=300
    )
    
    # 获取日线数据
    print(f"正在获取 {ts_code} 从 {start_date} 到 {end_date} 的数据...")
    df = pro.daily(
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date
    )
    
    if df is None or df.empty:
        print("未获取到数据，请检查股票代码和日期范围")
        return None
    
    # 按日期排序
    df = df.sort_values('trade_date')
    
    print(f"成功获取 {len(df)} 条记录")
    print("\n数据预览：")
    print(df.head())
    print(f"\n数据范围：{df['trade_date'].min()} 到 {df['trade_date'].max()}")
    
    return df


def fetch_stock_basic(token, cache_path=None):
    """
    获取股票基本信息
    
    参数：
        token: str, Tushare API token
        cache_path: str, 缓存路径，默认为 None
    
    返回：
        DataFrame: 包含股票基本信息的 DataFrame
    """
    if cache_path is None:
        cache_path = "./.tushare_cache"
    
    pro = DataClient(
        url="https://api.tushare.pro",
        token=token,
        cache_path=cache_path,
        timeout=300
    )
    
    print("正在获取股票基本信息...")
    df = pro.stock_basic(
        exchange="",
        list_status="L",
        fields="ts_code,symbol,name,area,industry,list_date"
    )
    
    print(f"成功获取 {len(df)} 只股票信息")
    print("\n数据预览：")
    print(df.head(10))
    
    return df


def main():
    parser = argparse.ArgumentParser(description='通过 Tushare 获取股票数据')
    parser.add_argument('--token', type=str, required=True, help='Tushare API token')
    parser.add_argument('--ts_code', type=str, help='股票代码，如 000001.SZ')
    parser.add_argument('--start_date', type=str, help='开始日期，格式 YYYYMMDD')
    parser.add_argument('--end_date', type=str, help='结束日期，格式 YYYYMMDD')
    parser.add_argument('--cache_path', type=str, default='./.tushare_cache', help='缓存路径')
    parser.add_argument('--list_stocks', action='store_true', help='列出所有股票基本信息')
    parser.add_argument('--output', type=str, help='输出文件路径（CSV格式）')
    
    args = parser.parse_args()
    
    if args.list_stocks:
        # 获取股票列表
        df = fetch_stock_basic(args.token, args.cache_path)
    elif args.ts_code and args.start_date and args.end_date:
        # 获取指定股票的行情数据
        df = fetch_stock_data(
            token=args.token,
            ts_code=args.ts_code,
            start_date=args.start_date,
            end_date=args.end_date,
            cache_path=args.cache_path
        )
    else:
        parser.print_help()
        return
    
    # 保存到文件
    if args.output and df is not None:
        df.to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到 {args.output}")


if __name__ == '__main__':
    main()
