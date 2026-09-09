# 会议稿完整案例：从方法简述到受证据约束的表达

这是一个可阅读、可局部运行的 synthetic 教学案例。
场景涉及细胞扰动响应预测，但没有训练模型或运行生物实验。
方法简述是设想，六个任务得分是手工构造值；两者没有实际实验生产关系。
本例不是论文范文、已接收稿件或真实会议政策。

![六个构造任务的基线与候选得分。](preview.png)

## 先读输入，再看输出

| 文件 | 用途 |
|---|---|
| [case-brief.md](case-brief.md) | 方法设想、六行数据、缺失材料、可用于交互练习的任务请求 |
| [scores.csv](scores.csv) | 六个任务的原始构造得分 |
| [manuscript-example.md](manuscript-example.md) | 示范写作提纲及英文 Abstract、Method、Results、legend、Limitations |
| [reviewer-response.md](reviewer-response.md) | 三条虚构审稿意见及有修改位置的回应 |
| [before.tex](before.tex) | 故意含身份命令、致谢与过度结论的短源文件 |
| [after.tex](after.tex) | 保留数值、修复源缺陷的短修正版 |
| [figure.json](figure.json) | 从 CSV 画散点图的规格 |
| [demo-profile.json](demo-profile.json) | 本教学场景的源检查规则 |
| [preview.png](preview.png) | 由所提供渲染器生成并随案例提供的预览 |

`manuscript-example.md` 比短 TeX fixture 更完整；它不是由 TeX 转换或 checker 生成。
提纲、英文段落、前后修改和回复均是预先编写的示范，
不是某次 agent 执行记录。读者可按任务请求自己练习，但不需要得到逐字相同的回答。

## 为什么这样写

先区分方法状态：状态表示加扰动描述只是概念比较，没有实现、训练或消融。
接着逐行看得分：配对差依次为 0.02、0.01、-0.01、0.02、0.01、-0.02，
四个任务较高、两个较低，平均差 0.005 任意单位。
因此 Results 需要保留负差，而不是把平均数写成一致提升。

> 修改前：The candidate consistently outperforms the baseline across all tasks.
>
> 修改后：In six illustrative tasks, the candidate score is higher on four tasks and
> lower on two. The mean paired difference is 0.005 arbitrary score units.

然后把“无真实模型、无抽样模型、无不确定性估计、无泛化验证”写进限制，
在模拟审稿回复里明确尚未完成消融。这样 Abstract、Results、图注和回复对同一证据给出一致解释。
完整示范见 [manuscript-example.md](manuscript-example.md)；
checker 本身不发现或验证这一科学修订。

## 教学 profile 的范围

`SHOWCASE_README` source ID 指向本页。本虚构匿名阶段要求 `article` class、
`graphicx` package 和 abstract；检查活跃的 `author` / `affiliation` 命令及致谢段落。
profile 日期只是 fixture 日期，不是官方政策刷新。真实投稿应使用匹配的当前正式适配器。

## 实际运行：数据图与源检查

默认在仓库根目录执行。若使用独立安装副本，把第一行改成包含 `SKILL.md` 的实际绝对目录；
其余资源均随该目录提供。先准备 Python 3.9+ 与对应 requirements，不需要 TeX 或图像服务。

```bash
SKILL_DIR="$PWD/skills/prepare-conference-manuscripts"
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
DEMO="$SKILL_DIR/examples/showcase"
DEMO_OUT="$(mktemp -d)"
MPLCONFIGDIR="$DEMO_OUT/.mpl" XDG_CACHE_HOME="$DEMO_OUT/.cache" \
  python3 "$SKILL_DIR/scripts/render_evidence_figure.py" \
  "$DEMO/figure.json" "$DEMO_OUT/figure"
```

预期 exit 0。到 `$DEMO_OUT` 打开 `figure.png`，同目录还有可编辑文字的 SVG 与矢量 PDF。
图中每点对应一个任务，横轴是 baseline，纵轴是 candidate，单位任意。
所有六行均显示，不含拟合、误差条或统计检验。

下一条故意失败，请单独运行，避免 shell 的遇错退出掩盖后面的检查：

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" \
  "$DEMO/before.tex" --profile "$DEMO/demo-profile.json" \
  --stage anonymous_submission --format markdown
```

预期 exit 1：`ANON_SOURCE_IDENTITY` 在第 3 行，
`ANON_ACKNOWLEDGMENTS` 在第 12 行。它不会报告“所有任务领先”的科学错误。

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" \
  "$DEMO/after.tex" --profile "$DEMO/demo-profile.json" \
  --stage anonymous_submission --format markdown
```

预期 exit 0，`Findings: 0`。修正版本来就在目录中；这条命令不是文本编辑器。

## 本地能观察到的交付

| 类型 | 实际得到什么 | 没有做什么 |
|---|---|---|
| 图渲染 | 三个图文件，点来自 CSV | 不训练模型、不验证方法有效性 |
| 源检查 | bad 两个 P0 findings；after 零 findings | 不编译 TeX、不检查最终 PDF |
| 教学示范 | 已提供的提纲、段落和回复 | 不声称它们由脚本自动生成 |
| 数据解释 | 四高两低、平均差 0.005 的逐行可核对描述 | 不进行总体推断或显著性检验 |

本例没有模拟完整投稿流程或 concept-to-native-PPTX 路线。
可将同样的证据边界应用到真实任务，但不能把构造值、虚构方法或模拟 reviewer 变成研究证据。
