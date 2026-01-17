#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跑步数据分析脚本
读取所有跑步记录，生成统计分析报告
"""

import os
from collections import defaultdict

def parse_markdown_table(file_path):
    """解析Markdown表格中的跑步数据"""
    records = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找表格内容
    lines = content.split('\n')
    in_table = False

    for line in lines:
        if line.startswith('| 日期'):
            in_table = True
            continue
        if in_table and line.startswith('|---'):
            continue
        if in_table and line.startswith('|'):
            # 解析数据行
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 9 and parts[0] and parts[0] != '日期':
                try:
                    record = {
                        'date': parts[0],
                        'distance': float(parts[1]),
                        'duration': float(parts[2]),  # 改为float支持小数
                        'pace': parts[3],
                        'avg_hr': int(parts[4]) if parts[4] and parts[4] != '-' else None,
                        'max_hr': int(parts[5]) if parts[5] and parts[5] != '-' else None,
                        'weight': float(parts[6]) if parts[6] and parts[6] != '-' else None,
                        'venue': parts[7],  # 改为venue（场地）
                        'feeling': int(parts[8]) if parts[8] and parts[8] != '-' else None,
                        'note': parts[9] if len(parts) > 9 else ''
                    }
                    records.append(record)
                except (ValueError, IndexError) as e:
                    # 调试：打印解析失败的行
                    print(f"解析失败: {line}")
                    print(f"错误: {e}")
                    continue
        elif in_table and not line.strip().startswith('|'):
            in_table = False

    return records

def analyze_data(data_dir='data'):
    """分析所有跑步数据"""
    all_records = []
    monthly_stats = defaultdict(lambda: {
        'total_distance': 0,
        'total_duration': 0,
        'count': 0,
        'avg_hr_sum': 0,
        'avg_hr_count': 0,
        'weights': [],
        'feelings': []
    })

    # 遍历所有年份和月份文件
    for year in os.listdir(data_dir):
        year_path = os.path.join(data_dir, year)
        if not os.path.isdir(year_path):
            continue

        for month_file in os.listdir(year_path):
            if not month_file.endswith('.md'):
                continue

            file_path = os.path.join(year_path, month_file)
            records = parse_markdown_table(file_path)
            all_records.extend(records)

            # 统计月度数据
            month_key = f"{year}-{month_file[:2]}"
            for record in records:
                monthly_stats[month_key]['total_distance'] += record['distance']
                monthly_stats[month_key]['total_duration'] += record['duration']
                monthly_stats[month_key]['count'] += 1

                if record['avg_hr']:
                    monthly_stats[month_key]['avg_hr_sum'] += record['avg_hr']
                    monthly_stats[month_key]['avg_hr_count'] += 1

                if record['weight']:
                    monthly_stats[month_key]['weights'].append(record['weight'])

                if record['feeling']:
                    monthly_stats[month_key]['feelings'].append(record['feeling'])

    return all_records, monthly_stats

def print_report(all_records, monthly_stats):
    """打印分析报告"""
    print("=" * 60)
    print("跑步数据分析报告")
    print("=" * 60)
    print()

    # 总体统计
    if all_records:
        total_distance = sum(r['distance'] for r in all_records)
        total_duration = sum(r['duration'] for r in all_records)
        total_count = len(all_records)
        avg_distance = total_distance / total_count
        avg_duration = total_duration / total_count

        print("【总体统计】")
        print(f"总跑步次数: {total_count} 次")
        print(f"总跑步距离: {total_distance:.2f} 公里")
        print(f"总跑步时长: {total_duration:.0f} 分钟 ({total_duration/60:.1f} 小时)")
        print(f"平均每次距离: {avg_distance:.2f} 公里")
        print(f"平均每次时长: {avg_duration:.0f} 分钟")
        print()

        # 心率统计
        hr_records = [r for r in all_records if r['avg_hr']]
        if hr_records:
            avg_hr = sum(r['avg_hr'] for r in hr_records) / len(hr_records)
            max_hr = max(r['max_hr'] for r in hr_records if r['max_hr'])
            print(f"平均心率: {avg_hr:.0f} bpm")
            print(f"最高心率: {max_hr} bpm")
            print()

        # 体重统计
        weight_records = [r for r in all_records if r['weight']]
        if weight_records:
            weights = [r['weight'] for r in weight_records]
            print(f"最新体重: {weights[-1]:.1f} kg")
            print(f"最高体重: {max(weights):.1f} kg")
            print(f"最低体重: {min(weights):.1f} kg")
            print(f"体重变化: {weights[-1] - weights[0]:+.1f} kg")
            print()

    # 月度统计
    if monthly_stats:
        print("【月度统计】")
        print(f"{'月份':<12} {'次数':>6} {'总距离(km)':>12} {'平均心率':>10} {'平均感受':>10}")
        print("-" * 60)

        for month in sorted(monthly_stats.keys()):
            stats = monthly_stats[month]
            avg_hr = stats['avg_hr_sum'] / stats['avg_hr_count'] if stats['avg_hr_count'] > 0 else 0
            avg_feeling = sum(stats['feelings']) / len(stats['feelings']) if stats['feelings'] else 0

            print(f"{month:<12} {stats['count']:>6} {stats['total_distance']:>12.2f} "
                  f"{avg_hr:>10.0f} {avg_feeling:>10.1f}")
        print()

    # 最近5次记录
    if all_records:
        print("【最近5次跑步】")
        recent = all_records[-5:]
        for r in reversed(recent):
            print(f"{r['date']}: {r['distance']}km, {r['pace']}, "
                  f"心率{r['avg_hr'] or '-'}bpm, 感受{r['feeling'] or '-'}/10")
        print()

    print("=" * 60)

def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, 'data')

    if not os.path.exists(data_dir):
        print("错误: 找不到data目录")
        return

    all_records, monthly_stats = analyze_data(data_dir)

    if not all_records:
        print("暂无跑步记录数据")
        return

    print_report(all_records, monthly_stats)

if __name__ == '__main__':
    main()
