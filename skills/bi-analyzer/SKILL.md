---
name: bi-analyzer
description: 识别和分析缠论中的笔结构。当需要在K线数据中识别笔、分析笔的特征、验证笔的有效性时使用此技能。适用于：(1) 识别笔的起点和终点 (2) 分析笔的长度和方向 (3) 验证笔的有效性 (4) 为线段识别提供基础
---

# 笔分析器

## 概述

笔是缠论中的基本结构单位，由相邻的顶分型和底分型之间的K线序列构成。本技能帮助识别和分析K线数据中的笔结构。

## 笔的定义

### 基本要求

1. **分型交替**：笔必须由顶分型和底分型交替构成
2. **最小长度**：两个分型之间至少包含一根独立K线（通常要求5根以上）
3. **方向明确**：笔的方向由起始分型决定
   - 从底分型到顶分型：向上笔
   - 从顶分型到底分型：向下笔

### 笔的特征

- **起点**：笔的起始分型位置和价格
- **终点**：笔的结束分型位置和价格
- **长度**：笔包含的K线数量
- **方向**：向上或向下
- **幅度**：笔的价格变化幅度
- **强度**：根据长度和幅度计算

## 工作流程

### 1. 前置条件

确保已识别出所有分型（可使用 fractal-detector 技能）：
```python
fractals = [
    {"type": "bottom", "index": 2, "dt": "...", "price": 9.5},
    {"type": "top", "index": 7, "dt": "...", "price": 11.0},
    {"type": "bottom", "index": 12, "dt": "...", "price": 10.0},
    ...
]
```

### 2. 识别笔

遍历分型列表，识别有效的笔：

```
current_bi = None

for each fractal in fractals:
    if current_bi is None:
        # 开始新笔
        current_bi = {start: fractal}
    else if fractal.type != current_bi.start.type:
        # 检查是否满足最小长度要求
        k_count = fractal.index - current_bi.start.index + 1
        if k_count >= MIN_BI_LEN:
            # 形成有效笔
            save_bi(current_bi.start, fractal)
        # 开始下一笔
        current_bi = {start: fractal}
```

### 3. 笔的验证

验证笔的有效性：

**基本验证：**
- 分型类型必须交替（顶底顶底...）
- 满足最小K线数量要求（通常≥5根）
- 价格必须有明确方向（向上笔终点>起点，向下笔终点<起点）

**高级验证：**
- 笔的内部不应出现新的同向分型
- 笔的破坏条件检查
- 笔的力度分析

### 4. 笔的分析

对识别出的笔进行特征分析：

```python
bi_analysis = {
    "direction": "up" if end_price > start_price else "down",
    "length": kline_count,
    "amplitude": abs(end_price - start_price),
    "amplitude_pct": abs(end_price - start_price) / start_price * 100,
    "duration": time_difference,
    "strength": calculate_strength(length, amplitude)
}
```

## 使用示例

### 示例 1：基础笔识别

用户请求：
```
帮我识别这组K线中的所有笔

[K线数据或分型数据...]
```

处理步骤：
1. 如果提供K线数据，先识别分型
2. 基于分型识别笔
3. 计算每笔的特征
4. 返回笔列表

### 示例 2：笔的验证

用户请求：
```
验证从第3根K线到第8根K线是否构成有效的笔
```

处理步骤：
1. 检查起止位置的分型类型
2. 验证K线数量是否满足要求
3. 检查方向是否一致
4. 返回验证结果

### 示例 3：结合 czsc 库

```python
from czsc.analyze import CZSC

# 创建 CZSC 对象
czsc_obj = CZSC(klines)

# 获取笔列表
bi_list = czsc_obj.bi_list

# 分析笔
for bi in bi_list:
    print(f"{bi.fx_a.dt} -> {bi.fx_b.dt}: "
          f"{bi.direction} - 长度{bi.length}")
```

## 笔的分类

### 按方向分类
- **向上笔**：从底分型到顶分型
- **向下笔**：从顶分型到底分型

### 按强度分类
- **强笔**：长度长、幅度大
- **弱笔**：长度短、幅度小

### 按位置分类
- **趋势笔**：顺应主趋势方向
- **回调笔**：逆主趋势方向

## 注意事项

1. **最小长度要求**：通常要求至少5根K线，可根据实际调整
2. **分型必须有效**：确保分型识别正确
3. **笔的连续性**：前一笔的终点是下一笔的起点
4. **特殊情况处理**：
   - 包含关系已处理的K线
   - 极端行情下的分型
   - 缺口的处理

## 输出格式

```json
{
  "bis": [
    {
      "direction": "up",
      "start": {
        "index": 2,
        "dt": "2024-01-01 09:30",
        "price": 9.5,
        "type": "bottom"
      },
      "end": {
        "index": 7,
        "dt": "2024-01-01 11:00",
        "price": 11.0,
        "type": "top"
      },
      "length": 6,
      "amplitude": 1.5,
      "amplitude_pct": 15.79
    }
  ],
  "count": 10,
  "up_count": 5,
  "down_count": 5
}
```

## 扩展功能

基于笔识别可以扩展：
- 线段识别（需要笔的破坏）
- 中枢识别（需要多笔组合）
- 买卖点判断
- 背驰分析
