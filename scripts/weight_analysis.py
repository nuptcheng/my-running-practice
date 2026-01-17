#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
体重-心率-配速关联分析脚本
验证体重对心率和配速的影响
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 导入分析脚本的函数
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analyze import analyze_data

def pace_to_seconds(pace_str):
    """将配速转换为秒数"""
    try:
        parts = pace_str.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    except:
        return None

def analyze_weight_correlation(all_records):
    """分析体重与心率、配速的关联"""

    # 筛选有完整数据的记录
    valid_records = []
    for r in all_records:
        if r['weight'] and r['avg_hr'] and r['pace']:
            pace_seconds = pace_to_seconds(r['pace'])
            if pace_seconds:
                valid_records.append({
                    'date': r['date'],
                    'weight': r['weight'],
                    'avg_hr': r['avg_hr'],
                    'pace_seconds': pace_seconds,
                    'distance': r['distance']
                })

    if len(valid_records) < 2:
        print("数据不足，至少需要2条完整记录才能进行关联分析")
        return None

    # 按日期排序
    valid_records.sort(key=lambda x: x['date'])

    return valid_records

def calculate_correlation(x, y):
    """计算相关系数"""
    if len(x) < 2:
        return 0

    x = np.array(x)
    y = np.array(y)

    # 计算皮尔逊相关系数
    correlation = np.corrcoef(x, y)[0, 1]
    return correlation

def print_analysis_report(valid_records):
    """打印分析报告"""
    if not valid_records:
        return

    weights = [r['weight'] for r in valid_records]
    hrs = [r['avg_hr'] for r in valid_records]
    paces = [r['pace_seconds'] for r in valid_records]

    print("=" * 60)
    print("体重-心率-配速关联分析报告")
    print("=" * 60)
    print()

    print(f"分析记录数: {len(valid_records)} 条")
    print()

    # 体重变化
    weight_change = weights[-1] - weights[0]
    print("【体重变化】")
    print(f"起始体重: {weights[0]:.1f} kg")
    print(f"当前体重: {weights[-1]:.1f} kg")
    print(f"体重变化: {weight_change:+.1f} kg")
    print()

    # 心率变化
    hr_change = hrs[-1] - hrs[0]
    print("【心率变化】")
    print(f"起始平均心率: {hrs[0]} bpm")
    print(f"当前平均心率: {hrs[-1]} bpm")
    print(f"心率变化: {hr_change:+d} bpm")
    print()

    # 配速变化
    pace_change = paces[-1] - paces[0]
    print("【配速变化】")
    print(f"起始配速: {paces[0]//60}:{paces[0]%60:02d}")
    print(f"当前配速: {paces[-1]//60}:{paces[-1]%60:02d}")
    print(f"配速变化: {pace_change:+d} 秒/km")
    print()

    # 相关性分析
    print("【相关性分析】")

    # 体重与心率的相关性
    weight_hr_corr = calculate_correlation(weights, hrs)
    print(f"体重与心率相关系数: {weight_hr_corr:.3f}")
    if abs(weight_hr_corr) > 0.7:
        print("  → 强相关：体重对心率影响显著")
    elif abs(weight_hr_corr) > 0.4:
        print("  → 中等相关：体重对心率有一定影响")
    else:
        print("  → 弱相关：体重对心率影响较小")

    # 体重与配速的相关性
    weight_pace_corr = calculate_correlation(weights, paces)
    print(f"体重与配速相关系数: {weight_pace_corr:.3f}")
    if abs(weight_pace_corr) > 0.7:
        print("  → 强相关：体重对配速影响显著")
    elif abs(weight_pace_corr) > 0.4:
        print("  → 中等相关：体重对配速有一定影响")
    else:
        print("  → 弱相关：体重对配速影响较小")

    print()

    # 预测分析
    if weight_change != 0:
        print("【预测分析】")

        # 计算每kg体重对心率的影响
        hr_per_kg = hr_change / weight_change if weight_change != 0 else 0
        print(f"每减重1kg，心率变化约: {hr_per_kg:.1f} bpm")

        # 预测达到目标体重时的心率
        target_weight = 78
        weight_to_lose = weights[-1] - target_weight
        if weight_to_lose > 0:
            predicted_hr = hrs[-1] + (hr_per_kg * (-weight_to_lose))
            print(f"预测体重降至{target_weight}kg时，心率约: {predicted_hr:.0f} bpm")

            target_hr = 150
            if predicted_hr <= target_hr:
                print(f"  ✅ 预计可以达到目标心率{target_hr} bpm")
            else:
                print(f"  ⚠️  预计心率{predicted_hr:.0f} bpm，仍高于目标{target_hr} bpm")

        print()

    # 建议
    print("【训练建议】")
    if weight_change < 0:
        print("✅ 体重在下降，继续保持")
    elif weight_change > 0:
        print("⚠️  体重在上升，需要调整饮食")
    else:
        print("→ 体重保持稳定")

    if hr_change < 0:
        print("✅ 心率在降低，有氧能力在提升")
    elif hr_change > 0:
        print("⚠️  心率在上升，需要注意训练强度")
    else:
        print("→ 心率保持稳定")

    print()
    print("=" * 60)

def plot_weight_hr_correlation(valid_records, output_dir='output'):
    """绘制体重-心率关联图"""
    if not valid_records:
        return

    weights = [r['weight'] for r in valid_records]
    hrs = [r['avg_hr'] for r in valid_records]
    dates = [r['date'] for r in valid_records]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # 体重和心率随时间变化
    ax1_twin = ax1.twinx()

    line1 = ax1.plot(range(len(dates)), weights, 'o-', color='green',
                     linewidth=2, markersize=8, label='体重')
    line2 = ax1_twin.plot(range(len(dates)), hrs, 's-', color='red',
                          linewidth=2, markersize=8, label='心率')

    ax1.set_xlabel('训练次数', fontsize=12)
    ax1.set_ylabel('体重 (kg)', fontsize=12, color='green')
    ax1_twin.set_ylabel('心率 (bpm)', fontsize=12, color='red')
    ax1.set_title('体重与心率变化趋势', fontsize=16, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='green')
    ax1_twin.tick_params(axis='y', labelcolor='red')
    ax1.grid(True, alpha=0.3)

    # 合并图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')

    # 体重-心率散点图
    ax2.scatter(weights, hrs, s=100, alpha=0.6, color='purple')

    # 添加趋势线
    if len(weights) >= 2:
        z = np.polyfit(weights, hrs, 1)
        p = np.poly1d(z)
        weight_range = np.linspace(min(weights), max(weights), 100)
        ax2.plot(weight_range, p(weight_range), "r--", alpha=0.8, linewidth=2, label='趋势线')

        # 显示相关系数
        corr = calculate_correlation(weights, hrs)
        ax2.text(0.05, 0.95, f'相关系数: {corr:.3f}',
                transform=ax2.transAxes, fontsize=12,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax2.set_xlabel('体重 (kg)', fontsize=12)
    ax2.set_ylabel('心率 (bpm)', fontsize=12)
    ax2.set_title('体重-心率关联分析', fontsize=16, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'weight_hr_correlation.png'), dpi=300)
    print(f"✓ 已生成: {output_dir}/weight_hr_correlation.png")
    plt.close()

def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, 'data')
    output_dir = os.path.join(project_dir, 'output')

    if not os.path.exists(data_dir):
        print("错误: 找不到data目录")
        return

    print("正在分析数据...")
    all_records, monthly_stats = analyze_data(data_dir)

    if not all_records:
        print("暂无跑步记录数据")
        return

    print(f"找到 {len(all_records)} 条跑步记录\n")

    # 分析体重关联
    valid_records = analyze_weight_correlation(all_records)

    if valid_records:
        # 打印分析报告
        print_analysis_report(valid_records)

        # 生成关联图表
        plot_weight_hr_correlation(valid_records, output_dir)

        print(f"\n图表已保存到 {output_dir} 目录")
    else:
        print("\n提示: 需要记录体重数据才能进行关联分析")
        print("请在每次跑步时记录体重，以便追踪体重对心率和配速的影响")

if __name__ == '__main__':
    main()
