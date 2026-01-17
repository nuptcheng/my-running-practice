#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跑步数据可视化脚本
生成各种图表展示跑步数据趋势
"""

import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 导入分析脚本的函数
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analyze import analyze_data, parse_markdown_table

def plot_distance_trend(all_records, output_dir='output'):
    """绘制跑步距离趋势图"""
    if not all_records:
        return

    dates = [datetime.strptime(r['date'], '%Y-%m-%d') for r in all_records]
    distances = [r['distance'] for r in all_records]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, distances, marker='o', linestyle='-', linewidth=2, markersize=6)
    plt.title('跑步距离趋势', fontsize=16, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('距离 (公里)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'distance_trend.png'), dpi=300)
    print(f"✓ 已生成: {output_dir}/distance_trend.png")
    plt.close()

def plot_pace_trend(all_records, output_dir='output'):
    """绘制配速趋势图"""
    if not all_records:
        return

    # 将配速转换为秒数
    def pace_to_seconds(pace_str):
        try:
            parts = pace_str.split(':')
            return int(parts[0]) * 60 + int(parts[1])
        except:
            return None

    dates = []
    paces = []
    for r in all_records:
        pace_seconds = pace_to_seconds(r['pace'])
        if pace_seconds:
            dates.append(datetime.strptime(r['date'], '%Y-%m-%d'))
            paces.append(pace_seconds / 60)  # 转换为分钟

    if not dates:
        return

    plt.figure(figsize=(12, 6))
    plt.plot(dates, paces, marker='o', linestyle='-', linewidth=2, markersize=6, color='orange')
    plt.title('配速趋势', fontsize=16, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('配速 (分/公里)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.gca().invert_yaxis()  # 配速越小越好，所以反转Y轴
    plt.tight_layout()

    plt.savefig(os.path.join(output_dir, 'pace_trend.png'), dpi=300)
    print(f"✓ 已生成: {output_dir}/pace_trend.png")
    plt.close()

def plot_heart_rate(all_records, output_dir='output'):
    """绘制心率趋势图"""
    hr_records = [r for r in all_records if r['avg_hr']]
    if not hr_records:
        return

    dates = [datetime.strptime(r['date'], '%Y-%m-%d') for r in hr_records]
    avg_hrs = [r['avg_hr'] for r in hr_records]
    max_hrs = [r['max_hr'] for r in hr_records if r['max_hr']]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, avg_hrs, marker='o', linestyle='-', linewidth=2, markersize=6,
             label='平均心率', color='red')
    if len(max_hrs) == len(dates):
        plt.plot(dates, max_hrs, marker='s', linestyle='--', linewidth=2, markersize=5,
                 label='最大心率', color='darkred', alpha=0.7)

    plt.title('心率趋势', fontsize=16, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('心率 (bpm)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(os.path.join(output_dir, 'heart_rate_trend.png'), dpi=300)
    print(f"✓ 已生成: {output_dir}/heart_rate_trend.png")
    plt.close()

def plot_weight_trend(all_records, output_dir='output'):
    """绘制体重趋势图"""
    weight_records = [r for r in all_records if r['weight']]
    if not weight_records:
        return

    dates = [datetime.strptime(r['date'], '%Y-%m-%d') for r in weight_records]
    weights = [r['weight'] for r in weight_records]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, weights, marker='o', linestyle='-', linewidth=2, markersize=6, color='green')
    plt.title('体重变化趋势', fontsize=16, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('体重 (kg)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(os.path.join(output_dir, 'weight_trend.png'), dpi=300)
    print(f"✓ 已生成: {output_dir}/weight_trend.png")
    plt.close()

def plot_monthly_summary(monthly_stats, output_dir='output'):
    """绘制月度统计图"""
    if not monthly_stats:
        return

    months = sorted(monthly_stats.keys())
    distances = [monthly_stats[m]['total_distance'] for m in months]
    counts = [monthly_stats[m]['count'] for m in months]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # 月度跑量
    ax1.bar(months, distances, color='steelblue', alpha=0.7)
    ax1.set_title('月度跑量统计', fontsize=16, fontweight='bold')
    ax1.set_xlabel('月份', fontsize=12)
    ax1.set_ylabel('总距离 (公里)', fontsize=12)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.tick_params(axis='x', rotation=45)

    # 月度训练次数
    ax2.bar(months, counts, color='coral', alpha=0.7)
    ax2.set_title('月度训练次数', fontsize=16, fontweight='bold')
    ax2.set_xlabel('月份', fontsize=12)
    ax2.set_ylabel('训练次数', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'monthly_summary.png'), dpi=300)
    print(f"✓ 已生成: {output_dir}/monthly_summary.png")
    plt.close()

def plot_feeling_distribution(all_records, output_dir='output'):
    """绘制感受评分分布"""
    feeling_records = [r for r in all_records if r['feeling']]
    if not feeling_records:
        return

    feelings = [r['feeling'] for r in feeling_records]
    feeling_counts = defaultdict(int)
    for f in feelings:
        feeling_counts[f] += 1

    plt.figure(figsize=(10, 6))
    scores = sorted(feeling_counts.keys())
    counts = [feeling_counts[s] for s in scores]

    plt.bar(scores, counts, color='purple', alpha=0.7)
    plt.title('训练感受评分分布', fontsize=16, fontweight='bold')
    plt.xlabel('感受评分', fontsize=12)
    plt.ylabel('次数', fontsize=12)
    plt.xticks(range(1, 11))
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()

    plt.savefig(os.path.join(output_dir, 'feeling_distribution.png'), dpi=300)
    print(f"✓ 已生成: {output_dir}/feeling_distribution.png")
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

    print(f"\n找到 {len(all_records)} 条跑步记录，开始生成图表...\n")

    # 生成各种图表
    plot_distance_trend(all_records, output_dir)
    plot_pace_trend(all_records, output_dir)
    plot_heart_rate(all_records, output_dir)
    plot_weight_trend(all_records, output_dir)
    plot_monthly_summary(monthly_stats, output_dir)
    plot_feeling_distribution(all_records, output_dir)

    print(f"\n所有图表已生成到 {output_dir} 目录")
    print("=" * 60)

if __name__ == '__main__':
    main()
