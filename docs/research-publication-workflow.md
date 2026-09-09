# 研究到发表：把研究问题做成可检查的结果

[返回仓库导览](../README.md) · [完整 skill](../skills/research-publication-pipeline/SKILL.md)

`research-publication-pipeline` 适合从 AI-for-biology 问题出发，组织数据可行性、文献比较、
实验计划、结果解释、论文材料与可运行代码。它提供完整工作指导和本地工具；
是否得到了科学结果，要看实际数据与实验，而不是记录中的通过状态。

本教程用一个细胞扰动预测问题串起这些工作，再运行六行合成分数的实际分析。
你不需要另一个 skill 就能完成教程；会议、期刊和可视化技能是可选的专项增强。

## 先跑一个有用的例子

问题是：利用扰动前细胞状态选择参考样本，是否值得作为未见扰动响应预测的候选机制？
真实项目首先要检查数据与比较。本地教学从一张已配对的小表开始，演示得到结果后应怎样读数。

从仓库根目录执行；已独立安装时，把 `SKILL_DIR` 改成那个完整 skill 的绝对路径：

```bash
SKILL_DIR="$PWD/skills/research-publication-pipeline"
DEMO_OUT=$(mktemp -d)
python3 -B "$SKILL_DIR/examples/perturbation-comparison/analyze_scores.py" \
  --scores "$SKILL_DIR/examples/perturbation-comparison/scores.csv" \
  --output "$DEMO_OUT/comparison"
```

需要 Python 3.9+，只用标准库，不需要网络、账户、API key 或 GPU。
命令使用 macOS/Linux shell；其他系统可提供等价的新输出路径。
`DEMO_OUT` 是新父目录，`comparison` 必须尚不存在，避免覆盖上一次结果。

| 实际得到的文件 | 看什么 | 随附输入的预期结果 |
|---|---|---|
| `differences.csv` | 每个任务的候选分数减基线分数 | +0.02、+0.01、−0.01、+0.02、+0.01、−0.02 |
| `summary.json` | 全部六行的等权描述性汇总 | 4 正、2 负、0 平；平均差 +0.005 |
| `summary.md` | 程序生成并打印的结果说明 | 保留两项负差，不声称全部改善 |

这些文件位于 `$DEMO_OUT/comparison/`。分数是任意设定的 **synthetic 教学数据**，
不是训练输出。完整的输入说明、结果段落和独立源码包运行方法见
[perturbation-comparison](../skills/research-publication-pipeline/examples/perturbation-comparison/README.md)。

## 一条完整的研究主线

先判断问题能否被回答，再决定需要什么方法。下面每一步都说明提供什么材料、
让 skill 做什么以及应收回什么成果。示范指令中的真实材料路径需替换为自己的文件。

### 1. 题目接入：数据、已有工作、贡献类型分别判断

输入应包含一个具体问题、已有材料、资源约束和当前项目说明。只有一个模型名字还不够。

```text
使用 $research-publication-pipeline 评估这个问题：
在未见基因扰动的响应预测中，按扰动前细胞状态选择参考样本，
能否优于同信息基线？先阅读我提供的项目说明、数据描述和相关论文。
分别判断 data_feasibility、scoop_verdict 和 venue_fit。
列出必须同时存在的变量、可链接单位与独立验证路径。
若来源不足，指出下一项最便宜的检查，不先设计新架构。
```

有用输出不是候选标题榜单，而是三项分开的判断。数据部分应明确对照、扰动身份、
状态变量与表达终点是否能对应，细胞、实验批次和供者各是什么层级。
已有工作部分要说明最接近方法比较了什么，哪些条件相同、哪些不同。
本例没有附真实来源，因此不能预先写下数据可用、未被做过或适合某刊。

### 2. 运行规划：固定比较，再决定候选变化

假设真实材料已经支持可行性，下一步交付的是能执行的实验计划。

```text
基于已检查的材料，准备一个小规模开发实验。
固定未见扰动的拆分、主要误差定义、训练信息边界和评价单位。
先安排扰动盲、简单回归及适用强基线的公平复现，再决定状态匹配是否有可测空间。
为状态匹配增加同信息对照，列出正向、负向和无法区分三种结果各允许得出什么结论。
给出命令、输入输出、资源估计与停止条件；这次只准备本地计划，不启动远端训练。
```

| 计划必须回答的内容 | 细胞扰动问题中的例子 |
|---|---|
| 拆分测什么 | 留出完整扰动身份，不把随机细胞拆分解释成未见扰动泛化 |
| 主指标是什么 | 在预定基因集合和对照定义上的预测误差，明确方向与实现 |
| 对照是否公平 | 输入信息、参考样本库、训练与调参预算可比 |
| 一个候选改变什么 | 只改变状态匹配策略，不能同时更换数据和评价规则 |
| 下一步如何决定 | 依靠开发比较与失败条件，保留未改善的任务 |

真实任务应在观察开发结果前固定选择与停止规则，并保持 locked-test 的使用边界。
查看 [协议与方法开发](../skills/research-publication-pipeline/references/protocol-headroom-and-development.md)
了解更完整的比较要求。这里没有给合成表杜撰噪声上界、训练预算或泛化结论。

### 3. 从结果决定下一步，不从均值倒推故事

现在使用上面生成的 `differences.csv` 与 `summary.json`：

```text
使用 $research-publication-pipeline 解释这次合成分析的两个输出文件。
先核对逐任务差值与完整任务数，再给出一段结果说明。
区分已计算的描述性结果、需要真实实验才成立的解释和建议的下一步。
保留 task-3 与 task-6 的负差，不做置信区间或显著性检验。
```

这次能写的结果是：六项教学任务中四项高于基线、两项低于基线，平均差为
+0.005 个任意分数单位。正均值不支持每项任务均改善。
合适的下一步是检查失败条件与配对定义；不是把数值重命名为生物学提升。
如果真实结果支持不了原假设，应保留负结果，明确是机制、数据还是问题本身需要修改。

### 4. 形成论文材料：让每个句子有对应产物

对真实研究，提供最终选定协议、逐单位结果、完整比较及来源，再请求论文工作。
若仅有本教程的合成结果，交付只能是教学性的结果段落与缺失证据说明。

```text
使用 $research-publication-pipeline 根据已完成的研究材料准备新的论文工作副本。
先说明中心问题和每一节需要回答什么，再把结果绑定到具体表格或分析输出。
写出 Methods、Results 和有边界的 Discussion，保留负结果与未运行的验证。
在当前投稿要求已核实且工具可用时，继续完成图表、图注、声明、实际编译和页面检查。
不要把缺失的真实结果改成占位数值，也不要改动冻结原稿。
```

应得到的是内容连贯的工作稿及它实际用到的图表，而不是一份标为完成的交接记录。
自包含的 [论文完成路径](../skills/research-publication-pipeline/references/standalone-manuscript.md)
覆盖章节组织、图注、声明、渲染与本地交付。图形工作可使用内置
[figure route](../skills/research-publication-pipeline/references/standalone-figures.md)，
根据来源数据、用途与可用工具制作并检查，不要求额外安装研究 skill。

### 5. 准备别人能跑的代码

本教程直接附带有用的分析源码、输入、许可和预期输出。只复制示例目录就能从新位置运行：

```bash
PACKAGE_OUT=$(mktemp -d)
cp -R "$SKILL_DIR/examples/perturbation-comparison" "$PACKAGE_OUT/public-release"
cd "$PACKAGE_OUT/public-release"
python3 -B analyze_scores.py --scores scores.csv --output "$PACKAGE_OUT/recheck"
```

用刚复制的源码生成同样的六行差值与汇总，便完成一次小而实际的复跑。
分析结果写在 `recheck`，不混入源码目录。

真实项目的请求可以是：

```text
为已完成的分析准备 public-release/，只包括用户需要的源码、配置、依赖版本、
小例子、数据获取与预处理说明、预期输出、测试、许可和真实引用信息。
按 README 在新位置执行一次，记录实际运行与未运行的命令。
只做本地准备，不创建远端仓库、推送或发布。
```

更完整的检查方式见 [public code release](../skills/research-publication-pipeline/references/public-code-release.md)。
不要把整个研究目录、私人数据或控制记录当成源码包。

## 安装与按需调用

安装方法统一见 [开始使用](../README.md#start)。安装后选择
`research-publication-pipeline`，或在支持命名技能的运行时使用 `$research-publication-pipeline`。

下面的初始化示例直接使用 checkout，无需修改安装路径。请从仓库根目录运行；
如果上一节已进入源码包目录，先回到 `open-research-skills` 根目录。
它会创建一个新的工作区，空记录不表示研究已经完成：

```bash
SKILL_DIR="$PWD/skills/research-publication-pipeline"
DEMO_OUT=$(mktemp -d)
python3 "$SKILL_DIR/scripts/init_publication_project.py" "$DEMO_OUT/project" \
  --project-id perturbation-study --title "未见扰动响应预测的状态匹配比较" \
  --domain single-cell --contribution-lane sota-method
```

常用工作模式为 `survey`、`plan`、`pilot`、`develop`、`monitor`、`freeze`、
`claim-lock`、`handoff`、`manuscript` 和 `public-release`。
它们是任务入口，不是要求每次依次运行的十道检查。

主教程分析和记录工具仅需标准库。读取 PDF、生成图形或编辑 PPTX 时，按安装目录内
`requirements.txt` 装入所需依赖；PDF 页面渲染另需对应本地工具。
实际论文编译、外部图像服务和在线来源读取取决于你的环境，不会由示例自动安装或启动。

## 进阶：记录检查与算术打包冒烟测试

如果你在维护本地工作流，可另运行原有的 `run_demo.py`：

```bash
# SKILL_DIR 指向你的完整 research-publication-pipeline 安装目录。
DEMO_OUT=$(mktemp -d)
python3 -B "$SKILL_DIR/examples/run_demo.py" "$DEMO_OUT/record-demo" --with-public-release
```

它会生成 synthetic 记录，打印 `pilot: PASS`、`development: PASS`、
`handoff: PASS` 与 `public-release: PASS`。真正执行的算术例子是 `[1, 2, 3]` 的计数 3、
求和 6，并在打包后执行两个测试。它没有训练模型，也没有计算科研比较。
详细解释见 [进阶示例](../skills/research-publication-pipeline/examples/README.md)。
这不是主教程配对分析的前置步骤。

## 一次说明清楚的边界

合成任务不是独立生物学重复；本教程没有真实数据访问、训练、置信区间、推断检验、
新颖性证明、SOTA 比较或独立验证。记录检查只验证其声明的字段和局部文件条件，
不能代替科学判断、真实来源检查、论文渲染或复现。
远端计算、locked-test 访问、冻结稿件修改、公开发布与提交仍需对应的明确授权。

遇到负结果不应隐去任务或换指标。如果缺少数据，先补可行性证据；如果只想查状态，
只报告观察到的状态；只有明确的完整研究任务才继续到论文与本地交付。

## 测试与维护

从仓库根目录运行新分析的最小测试：

```bash
python3 -B -m unittest discover -s tests/research-publication-workflow \
  -p test_perturbation_comparison.py
```

完整工作流测试为 `python3 -B -m unittest discover -s tests/research-publication-workflow -p 'test_*.py'`，
其中 PDF 与图形测试需仓库的 `requirements-test.txt` 环境。
发布内容检查为 `python3 scripts/check_public_content.py .`。

原创代码、文档与测试采用 Apache-2.0 许可。参见
[维护说明](../MAINTAINERS.md)、[贡献指南](../CONTRIBUTING.md) 与 [第三方说明](../THIRD_PARTY.md)。
其他专项教程：[会议论文](conference-manuscripts.md)、[期刊论文](journal-manuscripts.md)、
[科学可视化](scientific-visualizations.md)、[科研基金](research-funding-proposals.md)。
