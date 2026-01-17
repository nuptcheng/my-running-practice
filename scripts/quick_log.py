#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跑步记录快速录入和计划对比工具
"""

import os
import sys
from datetime import datetime

def get_project_root():
    """获取项目根目录"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)

def calculate_pace(distance_km, duration_minutes):
    """计算配速"""
    pace_minutes = duration_minutes / distance_km
    minutes = int(pace_minutes)
    seconds = int((pace_minutes - minutes) * 60)
    return f"{minutes}:{seconds:02d}"

def add_running_record():
    """交互式添加跑步记录"""
    print("=" * 60)
    print("跑步记录录入")
    print("=" * 60)
    print()

    # 获取日期
    date_input = input("日期 (直接回车使用今天): ").strip()
    if not date_input:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = date_input

    # 获取基本数据
    distance = float(input("距离 (km): "))
    duration = float(input("时长 (分钟): "))

    # 计算配速
    pace = calculate_pace(distance, duration)
    print(f"计算配速: {pace}")

    # 心率数据
    avg_hr = input("平均心率 (bpm): ").strip()
    max_hr = input("最大心率 (bpm): ").strip()

    # 体重
    weight = input("体重 (kg): ").strip()

    # 场地类型
    print("\n场地类型:")
    print("1. 跑步机")
    print("2. 户外")
    print("3. 操场")
    print("4. 其他")
    venue_choice = input("选择场地 (1-4): ").strip()
    venue_map = {"1": "跑步机", "2": "户外", "3": "操场", "4": "其他"}
    venue = venue_map.get(venue_choice, "其他")

    # 感受评分
    feeling = input("感受评分 (1-10): ").strip()

    # 备注
    note = input("备注: ").strip()

    # 生成记录行
    record_line = f"| {date} | {distance} | {duration:.2f} | {pace} | {avg_hr or '-'} | {max_hr or '-'} | {weight or '-'} | {venue} | {feeling or '-'} | {note} |"

    print("\n" + "=" * 60)
    print("生成的记录:")
    print("=" * 60)
    print(record_line)
    print()

    # 对比训练计划
    compare_with_plan(date, distance, pace, avg_hr)

    return record_line

def compare_with_plan(date, distance, pace, avg_hr):
    """对比训练计划"""
    print("\n" + "=" * 60)
    print("与训练计划对比")
    print("=" * 60)

    # 目标值（从训练计划中读取）
    target_hr_min = 145
    target_hr_max = 155
    target_pace_min = "6:15"
    target_pace_max = "6:45"

    print(f"\n📊 本次训练数据:")
    print(f"  距离: {distance} km")
    print(f"  配速: {pace}")
    print(f"  心率: {avg_hr or '未记录'} bpm")

    print(f"\n🎯 训练计划目标:")
    print(f"  心率: {target_hr_min}-{target_hr_max} bpm")
    print(f"  配速: {target_pace_min} - {target_pace_max}")

    print(f"\n✅ 完成情况:")

    # 心率对比
    if avg_hr and avg_hr != '-':
        hr_value = int(avg_hr)
        if target_hr_min <= hr_value <= target_hr_max:
            print(f"  ✅ 心率达标: {hr_value} bpm")
        elif hr_value < target_hr_min:
            under = target_hr_min - hr_value
            print(f"  ⚠️  心率偏低: {hr_value} bpm (低于目标 {under} bpm)")
            print(f"     说明: 可以适当加快配速")
        else:
            over = hr_value - target_hr_max
            print(f"  ❌ 心率超标: {hr_value} bpm (超出 {over} bpm)")
            print(f"     建议: 下次降低配速，控制心率")
    else:
        print(f"  ⚠️  未记录心率数据")

    # 配速对比
    pace_seconds = pace_to_seconds(pace)
    target_min_seconds = pace_to_seconds(target_pace_min)
    target_max_seconds = pace_to_seconds(target_pace_max)

    if pace_seconds:
        if target_min_seconds <= pace_seconds <= target_max_seconds:
            print(f"  ✅ 配速达标: {pace}")
        elif pace_seconds < target_min_seconds:
            diff = target_min_seconds - pace_seconds
            print(f"  ❌ 配速过快: {pace} (快了 {diff} 秒/km)")
            print(f"     建议: 放慢速度，优先控制心率")
        else:
            print(f"  ⚠️  配速偏慢: {pace}")
            print(f"     说明: 配速慢没关系，心率控制更重要")

    print("\n" + "=" * 60)

def pace_to_seconds(pace_str):
    """将配速转换为秒数"""
    try:
        parts = pace_str.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    except:
        return None

def main():
    """主函数"""
    try:
        record_line = add_running_record()

        print("\n💾 请将以下记录添加到月度记录文件中:")
        print(record_line)
        print("\n📝 记录文件位置: data/YYYY/MM-Month.md")

    except KeyboardInterrupt:
        print("\n\n已取消录入")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
