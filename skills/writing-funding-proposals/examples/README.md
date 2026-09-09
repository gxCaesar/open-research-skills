# 基金方案示例与记录工具演练

先看 [细胞扰动课题的带批注章节任务书](section-brief-walkthrough.md)。它说明如何把
科学问题、证据需求、公平比较、研究内容、年度安排与风险连成完整计划，
并给出立项依据、研究内容和研究基础的具体写作任务。这是供读者理解的虚构案例，
不是申请书正文或程序导出的真实工作区。

下面保留原有 `run_demo.py` 的 synthetic 记录夹具，供需要了解工具的人进阶使用。
它不承担科学论证或章节写作的工作。

## 从独立 skill 运行

从仓库根目录执行；完整安装后把 `SKILL_DIR` 改成实际目录：

```bash
SKILL_DIR="$PWD/skills/writing-funding-proposals"
DEMO_OUT=$(mktemp -d)
python3 -B "$SKILL_DIR/examples/run_demo.py" "$DEMO_OUT/funding-demo"
```

需要 Python 3.9+，仅依赖标准库，没有网络或账户要求。示例使用 macOS/Linux shell，
其他系统可提供等价的新路径。`mktemp -d` 创建父目录，`funding-demo` 是尚不存在的子目录。
脚本拒绝覆盖既有输出，也拒绝把输出放在已安装 skill 内。

## 预期终端输出

```text
Observed validator status: PASS
Observed validator scope: record_completeness (record-only)
```

程序还会打印教学用途提醒与输出目录。它初始化工作区并写入虚构记录，
使用固定的 `--as-of 2024-02-29` 历史快照检查 final 模式的记录完整性。
初始化或检查失败时，进程以非零退出码结束。

## 检查哪些产物

| 相对输出路径 | 用途 |
|---|---|
| `START_HERE.md` | 本地工作区导航 |
| `argument/argument-map.json` | 机制 M、结局 Y 的问题、比较与输出关系 |
| `sections/rationale.md` | 一句夹具文本，不是申请正文 |
| `evidence/claim-ledger.csv` | 主张如何对应来源字段的示范 |
| `commitments/commitment-records.json` | 有边界的计划承诺如何记录 |
| `delivery/final.pdf` | 检查器需要的占位路径，不是真实 PDF |

使用文本编辑器查看这些文件。PDF 查看器无法打开标记文件是预期的，
不表示真实申请书构建失败；该程序根本没有运行排版引擎。

## 这个演示不能证明什么

全部内容均为 synthetic。历史日期与 2026 项目标记只用于软件测试，
不表示真实政策查证，来源和申请人标签也不是实证材料。
`record_completeness` 仅说明记录满足本地契约，不证明来源真实性、申请人资格、
科学有效性、作者责任、排版质量、资助结果或允许提交。

没有生成真实申请书、官方模板、前期结果、AI 图像、可编辑 PPTX 或渲染后的候选文件。
请在独立真实项目中补齐实际材料，按核实后的允许范围推进，不要把本夹具重命名为
自己的申请。新细胞扰动任务书与原有 M/Y 夹具分开，夹具的科学标签和测试含义未改变。
