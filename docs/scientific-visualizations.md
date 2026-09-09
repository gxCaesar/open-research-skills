# 科研绘图：从科学材料到可编辑成品

[返回仓库首页](../README.md) · [14-panel 数据图](#atlas) · [方法架构图](#diagram) · [其他任务](#recipes) · [常见问题](#faq)

`build-scientific-visualizations` 负责科学图件的组织、绘制、图注和实际渲染检查。可以只画一张图，也可以协调一篇稿件的整套图；不要求安装另外四个 skill。

这份教程用两个任务讲清楚不同的制作路径：**已有数据如何组织为复合图，已有方法如何组织为示意图。** 第一条可用随附脚本重跑，第二条提供可编辑资产和面向 agent 的完整任务示范。

## 先选交付物，再选模式

| 想完成的任务 | 模式 | 交付范围 |
|---|---|---|
| 还没想清阅读顺序，先讨论排布 | `layout-sketch` | 可丢弃的布局草图 |
| 一张流程图、机制图或模型架构图 | `flowchart` | 示意图、可编辑 PPTX 与所需矢量导出 |
| 一张含多个证据面板的完整图 | `compound-figure` | 复合图、源文件、legend 与源数据 |
| 会议稿中的一组协调图件 | `conference-figure-set` | 方法、动机、结果等有明确分工的图组 |
| 期刊主图及扩展、补充图 | `journal-figure-set` | 共享符号和编码的整套图件 |

不需要记住模式名。直接描述交付物即可；模式表帮助你判断请求覆盖的是草图、单图还是图组。Sketch 不等于完成稿，架构图也不能替代实验结果图。

## 准备材料

给 agent 的材料越接近实际科学对象，它越容易把图画对：

| 材料 | 需要说明的内容 |
|---|---|
| 方法段落、当前图与草稿 legend | 图要解释哪个问题；哪些箭头表示运算、条件或监督 |
| 原始表格、已有绘图代码、测量图像或结构文件 | 数值和几何来自哪里；不要只给截图中的几个数字 |
| 样本信息和比较定义 | donor / specimen / cell 层级、配对关系、单位、排除规则 |
| 目标用途 | 期刊或会议、文章类型、插入尺寸、格式要求 |
| 视觉参考 | 借鉴层级与构图的参考，不作为本研究机制和结果的来源 |

已有可用图件只需局部修改时，直接改源文件。没有数据时可以讨论明确标为示意的布局，不能用生成图像补出不存在的结果。

## 环境与路径

安装整个 skill 的方法见[首页快速开始](../README.md#start)。以下命令从克隆仓库根目录执行，使用现有 Python 环境：

```bash
SKILL_DIR="$PWD/skills/build-scientific-visualizations"
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
DEMO_OUT=$(mktemp -d)
export MPLCONFIGDIR="$DEMO_OUT/.mpl"
export XDG_CACHE_HOME="$DEMO_OUT/.cache"
```

推荐先按首页创建虚拟环境。若已经单独安装，把 `SKILL_DIR` 指向含 `SKILL.md` 的实际目录；后续命令完全相同，不依赖仓库根目录。Python 3.9 或以上，shell 示例为 bash/zsh。

| 能力 | 额外需求 |
|---|---|
| 本页 CSV 重绘 | skill 的 Python 依赖，无需账号、GPU 或数据下载 |
| 全面 PDF 转换与字体检查 | 系统中的 Poppler 工具 |
| 新建 AI 辅助概念稿 | 可用的图像生成能力，优先指定 GPT Image 2.5 |
| 重建或编辑原生 PPTX | 支持原生演示文稿对象的制作与渲染能力 |

Python 依赖不安装后两项能力，也不提供商业模型账号。Arial 存在时使用 Arial；否则教学 renderer 会报告 DejaVu Sans，排版可能有变化。

<a id="atlas"></a>

## 案例一：空间多组学表格 → 14-panel 复合图

### 任务背景与输入

假设你要展示空间位置、RNA 与其他分子层之间的关系，以及 donor 层级的条件比较。不是把十四种图均匀摆满页面，而是让读者先定位组织区域，再理解分子变化，最后看比较与控制。

随附案例有四份 CSV：cell 坐标和分子值、donor-condition-assay 表、人工 locus tracks、选定 field/ROI。12 个 donor 标识、17,280 个 cell 及所有值均为合成数据；这不是显微图或真实 atlas。

[案例输入与字段说明](../skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/README.md) · [完整 legend](../skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/legend.md)

### 给 agent 的任务描述

```text
使用 build-scientific-visualizations，完成一个 compound-figure 教学任务。
阅读 spatial-multiomics-atlas 的四份 CSV、render.py 和 legend.md。
解释当前图的阅读顺序，并在副本中调整版面：
空间锚图与同源 ROI 在前，跨 assay 比较和 donor 配对关系在后。
保持所有输入值、比较定义和控制面板不变。
交付矢量 PDF/SVG、PNG 预览与同步更新的 legend。
```

这是修改教学布局的请求，不是修改分析。真实项目把示例材料替换为你的数据和论文段落，并明确数据中有哪些变量。

### 实际运行

完成前面的环境设置后：

```bash
python3 -B "$SKILL_DIR/examples/spatial-multiomics-atlas/render.py" \
  --output "$DEMO_OUT/atlas"
```

生成：

```text
atlas/
  spatial-multiomics-atlas.pdf
  spatial-multiomics-atlas.svg
  spatial-multiomics-atlas.png
```

终端摘要应包含 `panels: 14`、`donors: 12`、`cells: 17280`、`width_mm: 183`、`height_mm: 170` 和 `text_overflows: 0`。其中页边界检查不能发现所有面板内部重叠，仍需打开输出检查。再次写同一个目录会替换三份图件；需要保留版本时重新设置 `DEMO_OUT`。

### 如何读成品

![14-panel 空间多组学教学图](../skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/preview/spatial-multiomics-atlas.png)

- 空间大图是视觉入口，ROI 及连续信号层回答“在哪里”。
- 分子矩阵、donor × assay 热图和配对图回答“各层怎样比较”。
- 下方面板保留组成、轨迹、null 和边界敏感性，不把主图简化成只有正向结果。

PDF/SVG 是由代码绘制的矢量产物，PNG 是预览。可编辑源是绘图脚本与输入表；该案例不生成 PPTX。数据归一化、配对和控制的具体含义以随附 legend 为准，不从图的外观猜测。

[下载 PDF](../skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/preview/spatial-multiomics-atlas.pdf) · [下载 SVG](../skills/build-scientific-visualizations/examples/spatial-multiomics-atlas/preview/spatial-multiomics-atlas.svg)

### 迁移到自己的研究

先列每个面板对应的问题与数据来源，再映射样本 ID、条件、单位和配对。随附代码针对固定教学表结构，不是任意 CSV 的自动绘图接口。新研究可能需要改变面板数量、统计定义及缺失处理，不能只换文件名。

进阶阅读：[18-panel 多模态案例](../skills/build-scientific-visualizations/examples/multimodal-18-panel/README.md)、[密集复合图设计](../skills/build-scientific-visualizations/references/dense-compound-design.md)。

<a id="diagram"></a>

## 案例二：扰动预测方法 → 模型总览与模块展开

### 任务背景与输入

这个虚构教学模型有三路输入：baseline state、perturbation 与 context。两路条件进入交互模块，模块内部展开 state query、condition key/value、attention 与残差路径；观测响应只用于训练监督。

输入不是一张模糊截图，而是[随案例提供的科学内容说明](../skills/build-scientific-visualizations/examples/advanced-method-diagrams/method-brief.md)：对象、连接含义、训练/推理关系和不应暗示的结论。它不定义真实模型性能，也不把示意 token 数当成 tensor 尺寸。

### 给 agent 的任务描述

```text
使用 build-scientific-visualizations，为附件方法制作一张 conference 风格架构图。
上方画 baseline state、perturbation、context 到预测输出的总览，
下方展开交互模块；标明 attention、残差和 training-only supervision。
先参考优秀方法图的层级和留白，再用默认概念稿到原生 PPTX 的路线制作。
交付可分别编辑的文字、模块、连线，以及 PDF/SVG 和图注。
已有说明没有给出的维度、层数与效果不要补造。
```

### 新建图的默认制作路径

1. 阅读方法和 legend，确定科学对象、运算与箭头含义。
2. 检查适合当前任务的优秀示例，借鉴构图、分组和标注密度，不复制论文图或科学内容。
3. 用 GPT Image 2.5 生成概念稿；逐项纠正生成文字、公式和连接关系。
4. 重建为 PPTX 原生文字、形状、科学对象与连线，而非嵌入整张 PNG。
5. 保存、重新打开并检查实际导出；按稿件需求提供 PDF / SVG / PNG。

完整说明见[概念稿到可编辑矢量图](../skills/build-scientific-visualizations/references/image-concept-to-vector.md)。这条路径也适用于流程图、机制图、motivation 图和复合图中的示意部分。数据图和测量图像不走生成模型路径。

### 观察和修改现成文件

![总览与交互模块展开的原生模型图](../skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.png)

[原生 PPTX](../skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.pptx) · [PDF](../skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.pdf) · [SVG](../skills/build-scientific-visualizations/examples/advanced-method-diagrams/conference-conditioning-architecture.svg)

可以在刚才创建的输出目录保留一个编辑副本：

```bash
cp "$SKILL_DIR/examples/advanced-method-diagrams/conference-conditioning-architecture.pptx" \
  "$DEMO_OUT/conference-architecture-edit.pptx"
```

用兼容编辑器打开副本，选择一段文字修改标签，再移动一个模块，检查其进入和离开路径是否仍接在正确对象上。保存、重开并导出，对比标签、连线和版面。部分长路径由独立线段组成，不承诺移动模块后自动重排。

这个复制命令不制作新架构；随附 PPTX 是已经完成的可编辑资产。图像参考由 AI 生成，但当时工具未返回后端模型身份，所以不认证具体 GPT Image 版本。此前已检查原生保存、重开和渲染，未完成 Microsoft PowerPoint GUI 兼容性验证。

### 同一科学任务的另一种表达

![Nature-inspired 空间机制与采样层级](../skills/build-scientific-visualizations/examples/advanced-method-diagrams/nature-spatial-mechanism.png)

Nature-inspired 示例以组织、细胞、配对分子层和 donor 层级组织阅读路径，适合解释空间对象与采样关系。它与结构化模型图各有用途，不是给同一组方框换配色。

[空间机制图 PPTX](../skills/build-scientific-visualizations/examples/advanced-method-diagrams/nature-spatial-mechanism.pptx) · [编辑与复用说明](../skills/build-scientific-visualizations/examples/advanced-method-diagrams/README.md) · [两种风格、六套配色](../skills/build-scientific-visualizations/references/diagram-style-profiles.md) · [模板与参考图索引](../skills/build-scientific-visualizations/references/design-template-library.md)

<a id="recipes"></a>

## 更多任务的调用配方

### 先讨论布局，不做最终图

```text
使用 build-scientific-visualizations，先做 layout-sketch。
根据 figure-notes.md，提出一张复合图的阅读顺序与面板面积分配。
尚缺数据的位置明确标为未完成，不画虚构的结果曲线。
```

### 一篇会议论文的协调图组

```text
使用 build-scientific-visualizations，完成 conference-figure-set。
阅读 draft.tex 与现有 figures/，说明每张图分别支持哪个论证，
统一模块名称、符号和颜色，并在论文实际插入尺寸检查。
保留已经正确的数据分析，不固定要求每篇稿件都画相同数量的图。
```

### 一篇期刊论文的主图与扩展图

```text
使用 build-scientific-visualizations，协调主图与 Extended Data。
读取稿件、图注和 donor-level source data，统一配对关系及条件编码。
按指定期刊当前要求检查宽度、字体和导出，并交付图注与源文件。
```

### 领域素材如何选图

[空间与单细胞](../skills/build-scientific-visualizations/references/recipes-spatial-single-cell.md)覆盖组织—ROI—样本汇总关系；[蛋白、代谢与糖生物](../skills/build-scientific-visualizations/references/recipes-molecular-omics.md)区分丰度、检测和鉴定状态；[基因组、结构与临床](../skills/build-scientific-visualizations/references/recipes-genomic-structural-clinical.md)保留坐标、参考版本与比较尺度。这些是输入到图形的选择指南，不替你重新定义分析。

## 进阶工具

需要组织完整图件工作目录时，先查看实际工具帮助：

```bash
python3 -B "$SKILL_DIR/shared/figure-core/scripts/init_figure_project.py" --help
python3 -B "$SKILL_DIR/shared/figure-core/scripts/run_workflow.py" --help
```

初始化只是准备工作目录。后续需填写真实来源和版面定义，完成 layout，再检查 final。上述工具不会自动调用图像模型或构建原生 PPTX，直接 CSV demo 也不等于整套图件工作流。

<a id="faq"></a>

## 常见问题与交付检查

**Nature-inspired 是否代表符合投稿规范？** 不代表。它描述视觉方向。真实稿件以指定期刊、文章类型和投稿阶段的当前要求为准。

**PDF/SVG 和 PPTX 都“可编辑”，区别是什么？** PDF/SVG 保留矢量图形；原生 PPTX 还提供可单独选取修改的文稿对象。把 PNG 塞进 PPTX 或把整个 SVG 当一个对象，并不等于模块级编辑。

**能用生成图像替代显微图或分子结构吗？** 不能。测量图像与精确科学结构必须来自原始文件。AI 辅助示意图还需要遵守当前期刊图像政策及披露要求，矢量重绘不能免除这些要求。

**检查通过是否说明科学内容正确？** 不是。自动检查覆盖指定字段、页边界及部分内容风险。交付前仍要检查实际图中的配对、图例、箭头、标注与原始科学材料是否一致。

最小验收是：文件能打开；用途、尺寸与格式相符；文字和图形可读；数值与关系有来源；图注能独立解释单位和比较。只有使用了原生对象并检查其编辑行为，才描述为原生可编辑 PPTX。

维护者可从仓库根目录运行对应测试：

```bash
python3 -B -m unittest discover -s tests/scientific-visualizations -p 'test_*.py'
```

[会议论文中的图件整合](conference-manuscripts.md) · [期刊全文与图注](journal-manuscripts.md) · [贡献说明](../CONTRIBUTING.md)
