<div align="center">

# Open Research Skills

### 让科研材料成为清楚的论证、可编辑的图件和可复用的成果。

科研绘图 · 会议论文 · 期刊论文 · 中文基金 · 研究到发表

[选择 skill](#choose) · [快速开始](#start) · [绘图](#visualization) · [会议论文](#conference) · [期刊论文](#journal) · [基金](#funding) · [研究工作流](#workflow)

</div>

这是一个面向日常科研的 agent skill 工具箱。五个完整 skill 在一个仓库中维护，每个都能单独安装、独立使用。你可以从一张图、一段 Results 或一个研究问题开始，不必先启动整套研究流程。

教程以 AI 与生物研究为主，覆盖单细胞、扰动预测和空间多组学；组织材料、科学写作和交付方法也可迁移到其他领域。每个 skill 都提供**使用说明、完整教学情境、可读成品和可运行示例**。

<a id="choose"></a>

## 选择你这次需要的 skill

| 你现在的任务 | 入口 | 典型交付 |
|---|---|---|
| 把方法、机制或多组学结果画清楚 | [科研绘图](#visualization) | 可编辑架构图、多面板图、矢量文件与 legend |
| 从材料成稿，或修改 CS 会议论文 | [会议论文](#conference) | 论文与附录、结果论证、rebuttal、camera-ready |
| 组织期刊论文与投稿、修回材料 | [期刊论文](#journal) | 稿件、图注、数据声明、cover letter、审稿回复 |
| 梳理中文基金的科学问题与论证 | [中文基金](#funding) | 证据需求、研究内容、章节 brief、审阅建议 |
| 判断课题并推进实验、成稿与交付 | [研究工作流](#workflow) | 可行性判断、比较结果、下一步实验与复现材料 |

按**本次要交付的东西**选择即可。论文 skill 能独立处理论文需要的图件，研究工作流能独立组织成稿；专门的绘图 skill 提供更丰富的设计支持，但不是其他四个的强制依赖。

<a id="start"></a>

## 快速开始

### 1. 获取仓库，先看一个完整案例

```bash
git clone https://github.com/gxCaesar/open-research-skills.git
cd open-research-skills
```

不想先配置 agent？可以直接阅读或运行案例：

- 想看图件：[空间多组学复合图](skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/README.md)。
- 想看写作：[会议论文的一轮写作与修改](skills/prepare-conference-manuscripts/examples/showcase/README.md)。
- 想立即运行：[扰动预测教学比较](skills/research-publication-pipeline/examples/perturbation-comparison/README.md)，只需 Python 标准库。

### 2. 安装一个完整 skill

下面用绘图 skill 和仓库旁的 `research-demo` 练习项目演示。在仓库根目录执行；已有科研项目时，将 `RESEARCH_PROJECT` 改为那个项目的实际路径。

```bash
RESEARCH_PROJECT="$PWD/../research-demo"
SKILL_NAME=build-scientific-visualizations
SKILL_DEST="$RESEARCH_PROJECT/.agents/skills"
mkdir -p "$SKILL_DEST"

if test -e "$SKILL_DEST/$SKILL_NAME" || test -L "$SKILL_DEST/$SKILL_NAME"; then
  echo "目标已存在，未覆盖；请先保留并比较本地修改。"
else
  cp -R "skills/$SKILL_NAME" "$SKILL_DEST/"
fi
test -f "$SKILL_DEST/$SKILL_NAME/SKILL.md"
```

上面是 **Codex 项目级安装**。使用 Claude Code 时，把 `SKILL_DEST` 那行换成 `SKILL_DEST="$RESEARCH_PROJECT/.claude/skills"`，再执行后面的复制步骤。

| 使用范围 | Codex | Claude Code |
|---|---|---|
| 当前科研项目 | 项目内 `.agents/skills/` | 项目内 `.claude/skills/` |
| 所有本地项目 | `$HOME/.agents/skills/` | `$HOME/.claude/skills/` |

个人级安装只需将 `SKILL_DEST` 设为表中的对应目录。只复制完整的 `skills/<skill-name>/`，不要仅复制 `SKILL.md`，也不要再套一层同名目录。安装全部时，对五个名称分别执行同样的复制步骤。更新前保留自己的修改，不要直接覆盖。

路径与发现方式核对于 2026-09-09，参见 [Codex 官方说明](https://developers.openai.com/codex/skills)与 [Claude Code 官方说明](https://code.claude.com/docs/en/skills)。其他兼容 runtime 使用其自身的目录与发现机制；本仓库不配置账号或模型服务。

### 3. 在科研项目中调用

在 `research-demo` 或你的科研项目中打开 agent，并确认 skill 已出现在可用列表里。Codex CLI / IDE 使用 `$skill-name`，Claude Code 使用 `/skill-name`。也可以自然语言明确要求使用该 skill。

例如在 Codex 对话中输入：

```text
$build-scientific-visualizations
根据 methods.md 中的扰动预测方法，画出模型总览和交互模块展开图。
保留训练与推理边界，交付可编辑 PPTX、矢量 PDF 和 SVG。
```

将第一行替换为 `/build-scientific-visualizations` 即为 Claude Code 的显式调用形式。这是**对话输入，不是 shell 命令**。文件名要换成你实际提供的材料；发现不到新 skill 时，先检查目录层级，再重启对应 runtime。

### 4. 按任务准备依赖

阅读与标准库教学比较无需安装第三方包。绘图等脚本使用各 skill 自己的 `requirements.txt`；在仓库根目录可这样准备环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r skills/build-scientific-visualizations/requirements.txt
```

本文 shell 示例面向 macOS/Linux 的 bash/zsh，Python 3.9 或以上。Windows 请用对应 shell 的环境激活与变量语法。字体、Poppler、TeX、Office 渲染器及图像模型不是这些 Python 依赖的一部分，完整需求见各教程。

<a id="visualization"></a>

## 01 · 科研绘图

`build-scientific-visualizations` 将科学对象、方法关系和源数据组织为可读图件。适合单张机制图或架构图、一张密集复合图，以及 main / Extended Data / Supplementary 整套图。

**带上什么：** 方法说明或论文段落、数据表与已有绘图代码、独立样本与配对关系、目标宽度或版面要求。

**得到什么：** 图件、可编辑源文件、所需矢量导出、legend 与源数据说明。

### 案例 A：从空间多组学表格到 14-panel 复合图

![空间多组学教学复合图：空间锚图、ROI、分子层、配对比较与控制面板](skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/preview/spatial-multiomics-atlas.png)

空间锚图建立位置关系，同源 ROI 与 RNA 层承接局部观察，donor × assay 热图和配对图组织比较，后续面板补充组成、null 与敏感性。画布为 183 × 170 mm；12 个 donor 标识与 17,280 个 cell 坐标均为合成数据，不是显微图或真实研究结论。

在已准备绘图依赖的环境中，从仓库根目录运行：

```bash
SKILL_DIR="$PWD/skills/build-scientific-visualizations"
DEMO_OUT=$(mktemp -d)
MPLCONFIGDIR="$DEMO_OUT/.mpl" XDG_CACHE_HOME="$DEMO_OUT/.cache" \
  python3 -B "$SKILL_DIR/examples/spatial-multiomics-atlas/render.py" \
  --output "$DEMO_OUT/atlas"
```

实际生成 `spatial-multiomics-atlas.pdf`、`.svg` 和 `.png`；这个数据图例不生成 PPTX。

[完整情境与重绘教程](skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/README.md) · [PDF](skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/preview/spatial-multiomics-atlas.pdf) · [SVG](skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/preview/spatial-multiomics-atlas.svg) · [源数据](skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/data) · [Legend](skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/legend.md)

### 案例 B：从方法说明到可编辑架构图

![扰动条件化模型教学架构：总览、交互模块和训练推理边界](skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.png)

模型图分开 baseline state、perturbation 和 context，并展开 attention 与残差计算。另一张 Nature-inspired 图用组织、细胞、配对分子层和 donor 层级解释采样关系。两张都是虚构教学设计，文字、形状和连线在 PPTX 中可分别编辑。

[模型图 PPTX](skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.pptx) · [模型图 PDF](skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.pdf) · [空间机制图预览与编辑教程](skills/build-scientific-visualizations/examples/advanced-method-diagrams/README.md) · [空间机制图 PPTX](skills/build-scientific-visualizations/examples/advanced-method-diagrams/nature-spatial-mechanism.pptx)

新建或重设计示意图的默认方法是：**参考优秀构图 → GPT Image 2.5 概念稿 → 重建原生可编辑矢量 PPTX → 检查实际渲染。** 数据图与测量图像仍从原始材料绘制。当前图像工具若不公开后端版本，应报告版本未核实，不能把示例当成指定版本的运行认证。

```text
使用 build-scientific-visualizations。
根据 methods.md 和目前的 Figure 1，重设计模型总览与关键模块展开。
保留符号、箭头含义和训练/推理边界，使用默认概念稿到原生 PPTX 的路线。
交付可编辑 PPTX、矢量 PDF/SVG、图注；结果面板从 figures/data/ 重绘。
```

[完整中文使用教程](docs/scientific-visualizations.md) · [18-panel 进阶案例](skills/build-scientific-visualizations/examples/multimodal-18-panel/README.md) · [两种风格与六套配色](skills/build-scientific-visualizations/references/diagram-style-profiles.md)

<a id="conference"></a>

## 02 · 会议论文

`prepare-conference-manuscripts` 面向 CS 会议论文的新稿、修改、附录、rebuttal 和 camera-ready。它将研究问题、方法和结果组织成连贯论证，也处理论文所需图件与投稿阶段检查。

**带上什么：** 目标 venue/year/track、方法与实验记录、结果表、当前稿件；修回时另附审稿意见。

**得到什么：** 任务范围内的英文稿件、图表与图注、修改说明或逐点回复。

### 完整案例：扰动预测结果的一轮写作与修改

![会议论文案例的六组合成配对任务分数](skills/prepare-conference-manuscripts/examples/showcase/preview.png)

输入是方法背景、六组合成任务分数和一份有问题的初稿。教程展示如何形成写作提纲，完成 Abstract / Results / Limitations 节选，再回应一条质疑。

> In six illustrative tasks, the candidate score is higher on four tasks and lower on two. The mean paired difference is 0.005 arbitrary score units.

这段修改保留了两项不利结果；“所有任务都更好”不再成立。文本属于带注释的教学写作，图件由 CSV 渲染；源文件检查器另行演示匿名阶段的问题，并不自动生成或验证上述科学修订。

[输入、写作过程与可运行示例](skills/prepare-conference-manuscripts/examples/showcase/README.md) · [修改前](skills/prepare-conference-manuscripts/examples/showcase/before.tex) · [修改后](skills/prepare-conference-manuscripts/examples/showcase/after.tex)

```text
使用 prepare-conference-manuscripts。
根据 methods.md、results/ 和 draft.tex，完善 Results 与 Limitations，
再调整摘要，使问题、方法和证据范围一致。保留不利结果，不补造统计量。
先列出材料缺口；已有材料足够的部分直接修改，交付稿件和简短修改说明。
```

[完整中文教程：新稿、修改、rebuttal 与提交阶段](docs/conference-manuscripts.md)

<a id="journal"></a>

## 03 · 期刊论文

`prepare-journal-manuscripts` 组织期刊论文及编辑沟通材料：从故事线和全文，到主图、补充材料、统计报告、数据声明、cover letter 和修回。

**带上什么：** 目标期刊与文章类型、科学问题、方法和结果、样本结构、数据来源、当前稿件。

**得到什么：** 连贯稿件、完整 legend、统计与数据声明，以及所需编辑或审稿回复。

### 完整案例：六个配对 specimen 的结果报告

![期刊论文案例：六个教学 specimen 各自的两次观测](skills/prepare-journal-manuscripts/examples/showcase/preview.png)

六个 specimen 各有 baseline 与 follow-up 值，并不是十二个独立 specimen。案例贯通 Results、Methods、legend 与 Data Availability，展示这些部分如何使用同一个样本定义。

> Six constructed specimens each contribute one baseline and one follow-up value. Follow-up exceeds baseline for four specimens and is lower for two.

修改移除无法支持的因果与推广结论，数据声明指向实际随附的 CSV。英文成稿是教学示范，不是统计检查器自动产物；示例不进行假设检验，也没有真实治疗或实验对象。

[完整情境、成稿与运行方法](skills/prepare-journal-manuscripts/examples/showcase/README.md) · [修改前](skills/prepare-journal-manuscripts/examples/showcase/before.md) · [修改后](skills/prepare-journal-manuscripts/examples/showcase/after.md)

```text
使用 prepare-journal-manuscripts。
根据 manuscript.md、配对 specimen 结果表和数据清单，
完善 Results、Methods、figure legends 与 Data Availability。
统一独立样本数、配对关系和结论范围，并起草一封简洁的 cover letter。
缺少的 accession 或检验结果明确标出，不虚构补齐。
```

[完整中文教程：全文、数据声明、cover letter 与修回](docs/journal-manuscripts.md)

<a id="funding"></a>

## 04 · 中文基金

`writing-funding-proposals` 帮助梳理选题、科学问题、立项依据、研究内容和技术路线，将已有材料组织为可供申请人继续写作的论证结构。

**带上什么：** 申报指南与申请类别、自己的研究积累、初步想法、数据条件、已有章节。

**得到什么：** 政策与材料需求、问题—证据—研究内容的对应关系、章节 brief 和审阅建议；具体协助范围遵循当前资助方及机构要求。

### 完整案例：细胞扰动研究如何形成研究内容

案例从一个虚构问题开始：用扰动前细胞状态选择参考样本，能否改善未见扰动响应预测？它将想法展开为同信息对照下的可检验比较，而不是直接承诺“显著提升预测”。

| 需要写清楚的内容 | 案例怎样处理 |
|---|---|
| 科学问题 | 说明待区分的解释与所需变量，而非堆叠模型名称 |
| 研究内容 | 对照、数据划分与评估对象对应到问题 |
| 可行性 | 分开已具备条件、尚需验证的数据关联和证据缺口 |
| 年度安排 | 按数据核实、比较实验和验证交付组织工作 |
| 风险与产物 | 承诺完成可解释的比较，保留负向结果的处理方案 |

[完整中文情境与带注释章节 brief](skills/writing-funding-proposals/examples/section-brief-walkthrough.md) · [本地记录检查 demo](skills/writing-funding-proposals/examples/README.md)

```text
使用 writing-funding-proposals。
阅读 call.pdf、research-notes.md 和现有“研究内容”章节。
围绕细胞状态与扰动响应梳理一个中心科学问题，
交付证据缺口、研究内容对应表、年度安排建议和带注释的章节 brief。
区分已有结果与研究计划，不虚构前期基础。
```

章节 brief 是教学编辑材料，不是可直接提交的申请书。另附的标准库 demo 只检查合成记录完整性，不构建真实申请书 PDF，也不核验申请资格。

[完整中文教程：选题、论证、章节审阅与图文任务](docs/research-funding-proposals.md)

<a id="workflow"></a>

## 05 · 研究到发表

`research-publication-pipeline` 用于跨阶段研究任务：判断问题与数据条件，组织实验比较，解释结果，再推进到成稿和可复现交付。它也可以只处理其中一个已经明确的阶段。

**带上什么：** 研究问题、数据与文献线索、现有代码和结果、当前项目状态及资源限制。

**得到什么：** 有证据支撑的判断、下一项具体工作、实验或写作产物，以及所需复现代码。

### 完整案例：从扰动预测教学比较到下一步实验

案例提供六个虚构任务的 baseline / candidate 分数。轻量脚本实际读取表格，计算每项差值、提高/下降/持平数量与平均差值；教程再解释这些观察支持什么、缺少什么、下一项比较应该解决什么问题。

从仓库根目录运行，无需第三方包：

```bash
SKILL_DIR="$PWD/skills/research-publication-pipeline"
DEMO_OUT=$(mktemp -d)
python3 -B "$SKILL_DIR/examples/perturbation-comparison/analyze_scores.py" \
  --scores "$SKILL_DIR/examples/perturbation-comparison/scores.csv" \
  --output "$DEMO_OUT/comparison"
```

实际生成 `differences.csv`、`summary.json` 和 `summary.md`。输出目录必须不存在，避免覆盖已有结果。

| 可观察输出 | 如何用于写作与决策 |
|---|---|
| 六项配对差值 | 展示异质性，不只汇报一个平均数 |
| 四项提高、两项下降 | 限定结果段落，不写成一致领先 |
| 平均差值 0.005 | 仅为教学分数摘要，不能据此宣布真实 benchmark 的 SOTA |
| 可独立运行的分析代码 | 让读者用随附输入重算结果，而不是只看状态记录 |

[输入、运行命令、结果与下一步判断](skills/research-publication-pipeline/examples/perturbation-comparison/README.md) · [进阶：小型代码包打包演练](skills/research-publication-pipeline/examples/README.md)

```text
使用 research-publication-pipeline。
阅读 project-notes.md、数据说明与现有 baseline 结果。
分别判断数据可行性、新颖性证据和目标 venue 的匹配程度，
核对公平比较与可测提升空间，提出下一项最有判别力的小实验。
先完成本地分析与准备；不要启动远程训练、访问锁定测试或代为投稿。
```

教学分数是人工构造的，不是训练得到的生物学结果。计算摘要由脚本生成；研究判断与论文段落是明确标注的示范写作。真实项目仍需要真实数据、当前文献和实际实验。

[完整中文教程：课题判断、实验推进、成稿与复现交付](docs/research-publication-workflow.md)

## 常见问题

**需要一次安装五个吗？** 不需要。每个目录都带自己的指令、脚本、模板、参考与示例。它们可以协作，但没有强制安装顺序。

**运行 demo 等于调用了 skill 吗？** 不等于。脚本验证的是某个具体软件行为；在 agent 中调用 skill，才会根据你的材料进行分析、写作或制图。可读案例帮助你理解预期产物，不能当作自动生成能力的测试报告。

**会自动训练、改论文或投稿吗？** 取决于你明确交给 agent 的任务与可用能力。示例不会训练模型、购买服务或投稿。对既有稿件、实验协议及外部操作，应按任务授权执行。

**概念图和数据图有什么区别？** 概念图解释对象与关系；数据图报告观察。前者可在允许时采用 AI 辅助构图，后者必须使用真实来源。把概念稿重绘为矢量图不免除 AI 使用披露或期刊政策要求。

**可以直接换 CSV 吗？** 教学 renderer 有固定字段与样本约定，不是任意 CSV 的通用可视化界面。迁移时同时调整数据映射、比较单位、图形与解释，具体见各案例。

**出现预期的 exit 1 怎么办？** 会议和期刊案例包含故意不合格输入，教程标明了原因。先单独执行这些命令，再执行修订后的检查；不要把演示失败当成安装失败。

## 文档、依赖与贡献

首页帮助选择，五份中文指南负责讲清使用，随 skill 分发的案例负责展示具体输入与成品。英文保留在代码、技术术语与英文论文示例中，运行入口和参考文档不作机械翻译。

维护者在仓库根目录运行：

```bash
python3 -B scripts/run_tests.py
python3 -B scripts/check_public_content.py .
```

统一测试入口会分别运行根目录和五个 skill 的测试。测试依赖见 [requirements-test.txt](requirements-test.txt)，普通使用者只需安装任务所需依赖。本仓库未配置托管 CI。

[参与贡献](CONTRIBUTING.md) · [维护者](MAINTAINERS.md) · [第三方说明](THIRD_PARTY.md) · [Apache-2.0 许可证](LICENSE)
