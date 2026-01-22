# 项目规则（my-running-practice）

## 项目目标

- 这是个人跑步训练管理项目，用于记录、分析和优化训练数据，服务 2026 年度目标：10km 配速 5:40/km、心率尽量≤160（用户可能心率偏高）、体重目标 74kg
- 当前训练阶段：有氧基础建立期；核心策略：心率优先、循序渐进、配速服务于控心率

## 目录与文件职责

- data/YYYY/MM-MonthName.md：月度跑步记录与“本月统计”
- training-plans/YYYY-MM-plan.md：月度训练计划，含每次训练计划 vs 实际、周小结、月度统计
- docs/：使用指南、工作流、训练建议周报与索引
- scripts/：数据分析与可视化脚本（Python）
- output/：脚本生成的图表（仅在需要时更新）

## 数据记录规范（data/）

- 月度文件命名：`data/YYYY/NN-MonthName.md`（例如 `data/2026/01-January.md`）
- 表格字段顺序必须保持一致：
  - 日期｜距离(km)｜时长(分钟)｜配速(分/km)｜平均心率(bpm)｜最大心率(bpm)｜体重(kg)｜场地｜感受(1-10)｜备注
- 缺失值使用 `-`
- 时长使用分钟（允许小数，保留两位小数更一致）；配速格式 `m:ss`；日期格式 `YYYY-MM-DD`
- 跑步记录允许“未跑步”占位行（距离/时长/配速等为 `-`，备注说明原因）

## 批量归档流程（用户一次提供多日训练数据时）

1) 更新月度跑步记录
- 在对应月度表格中批量追加多行记录
- 同步更新“本月统计”：
  - 实际跑量：距离求和（仅统计距离为数字的训练）
  - 平均配速：按距离加权平均（用总时长/总距离得到平均配速）
  - 平均心率：算术平均（仅对有平均心率数值的训练）
  - 训练次数：计数（仅统计距离为数字的训练）

2) 更新月度训练计划
- 在对应日期标记状态（✅/❌/待完成），填写实际数据与“对比分析”
- 更新周小结与月度统计表格
- 必须生成“下一周完整训练计划”（周一到周日 7 天都要写明）：
  - 训练日：目标距离、配速区间、心率区间、每公里详细目标（渐进：前慢热身→中段稳定→末段控制）
  - 休息日：标注“休息”，给出恢复建议

3) 图表生成（仅在用户明确要求时）
- 运行：`python3 scripts/visualize.py`
- 输出位于 `output/`（distance/pace/heart_rate/weight/monthly_summary）

## 训练建议（按月归档，仅在用户要求输出建议时）

- 新建/更新文件：`docs/training-advice-YYYY-MM.md`（例如 `docs/training-advice-2026-01.md`）
- 必须包含：本月汇总、单次训练复盘（含计划 vs 实际、关键点）、整体评估、训练建议、下周完整 7 天计划或链接到训练计划文件、下次训练行动要点
- 同步更新索引：`docs/training-advice-index.md`（新增链接、关键结论与数据概览）

## 脚本与验证

- 快速录入（交互式）：`python3 scripts/quick_log.py`（不要在无人值守场景自动运行）
- 分析（非交互）：`python3 scripts/analyze.py`
- 可视化（需要 matplotlib）：`python3 scripts/visualize.py`
- 依赖安装（如缺失）：`pip3 install pandas matplotlib seaborn`
- 若修改了 `scripts/` 下 Python 代码，至少运行：
  - `python3 -m compileall scripts`
  - `python3 scripts/analyze.py`
