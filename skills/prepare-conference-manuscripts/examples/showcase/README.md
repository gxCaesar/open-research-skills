# 可选机械检查：会议稿本地工具

这个目录用于熟悉 CSV 图渲染与 TeX 源检查，不是顶会论文、专业图件或研究结果的展示。
六行得分均为预设的 synthetic 数据，没有训练模型或运行生物实验。
真实论文任务请从安装目录中的 [会议稿入口](../../SKILL.md) 出发，
提供实际 venue/year/track/stage、稿件、方法、协议和结果；无需先跑这个练习。

这里保留现有文件供复现工具行为。运行脚本不会起草或修改整篇论文，
不能用一次 PASS 证明主张成立、页面合规或投稿完成。

## 安装位置与输出

默认当前终端位于仓库根目录。使用独立安装副本时，把第一行改成包含
`SKILL.md` 的实际绝对目录；所有资源都在本 skill 内。
需要 Python 3.9+ 和相应 requirements，不需要 TeX 渲染器或图像服务。

```bash
SKILL_DIR="$PWD/skills/prepare-conference-manuscripts"
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
DEMO="$SKILL_DIR/examples/showcase"
DEMO_OUT="$(mktemp -d)"
```

新建输出目录避免覆盖已有结果。下面的命令使用同一个终端里定义的变量。

## 可选运行一：确认来源数据图能够导出

```bash
MPLCONFIGDIR="$DEMO_OUT/.mpl" XDG_CACHE_HOME="$DEMO_OUT/.cache" \
  python3 "$SKILL_DIR/scripts/render_evidence_figure.py" \
  "$DEMO/figure.json" "$DEMO_OUT/figure"
```

预期 exit 0，生成 `$DEMO_OUT/figure.svg`、`figure.pdf`、`figure.png`。
每点来自 [scores.csv](scores.csv) 一行，横纵坐标由 [figure.json](figure.json) 指定。
这个最小散点图只测试导出路径，不演示架构图、复合图设计或 concept-to-native-PPTX 工作流。
文件生成后仍需打开实际导出检查；脚本成功不等于专业论文图件完成。

## 可选运行二：检查故意有缺陷的源文件

下一条预期失败，应单独运行，避免 shell 的遇错退出掩盖后续检查：

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" \
  "$DEMO/before.tex" --profile "$DEMO/demo-profile.json" \
  --stage anonymous_submission --format markdown
```

预期 exit 1，两个 P0 findings：
`ANON_SOURCE_IDENTITY` 位于 [before.tex](before.tex) 第 3 行，
`ANON_ACKNOWLEDGMENTS` 位于第 12 行。
源文件中的过度结果句不是这个 checker 会发现的科学问题。

再检查已经提供的短修正版：

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" \
  "$DEMO/after.tex" --profile "$DEMO/demo-profile.json" \
  --stage anonymous_submission --format markdown
```

预期 exit 0，`Findings: 0`。[after.tex](after.tex) 本来就存在；
该命令只检查它，不是由 before 自动产生 after。
exit 2 表示输入或 profile 不可用，不能当成普通论文 finding。

## 教学 profile 具体检查什么

[demo-profile.json](demo-profile.json) 的 `SHOWCASE_README` source ID 指向本页。
此虚构匿名阶段要求 `article` class、`graphicx` package 和 abstract，
并检查活跃的 `author` / `affiliation` 命令及致谢段落。
profile 日期只是 fixture 日期，不是当前官方政策。

真实会议的样式行为不同。例如源文件出现作者命令，未必意味着最终匿名稿可见作者。
实际任务必须选择匹配且已核对当前权威的适配器，并检查真实渲染结果，
不能把本例的教学 profile 用作通用会议规则。

## 随附的教学对照材料

以下文本继续保留，仅用于理解“数据描述”与“科学主张”的差别，
不是正式论文写作模板，也不是脚本输出或实际 agent 执行记录：

- [case-brief.md](case-brief.md)：虚构方法设想与六行数据的边界；
- [manuscript-example.md](manuscript-example.md)：教学提纲和英文片段；
- [reviewer-response.md](reviewer-response.md)：虚构审稿关切与回复示范。

构造得分保留四个正差、两个负差，平均配对差为 0.005 任意单位。
这些数值不来自设想模型，不支持机制、显著性或生物学泛化。
研究写作应使用真实材料和当前稿件问题，而不是把这里的 synthetic 标签删掉后套用。

## 这次练习没有覆盖的工作

没有编译 TeX、检查最终 PDF、验证参考文献或会议政策，
没有生成整篇论文、运行研究实验、制作专业方法图或提交文件。
工具的局部检查应与作者实际需要的写作、页面审阅和文件交付分开说明。
