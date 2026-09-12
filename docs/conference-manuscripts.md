# 顶会论文使用手册

[仓库首页](../README.md) · [安装与调用](#安装与调用) · [选择会议与阶段](#选择会议与阶段) ·
[从材料起草论文](#从材料起草论文) · [修改已有稿件](#修改已有稿件) ·
[Rebuttal 与讨论修订](#rebuttal-与讨论修订) · [Camera-ready 与交付](#camera-ready-与交付)

`prepare-conference-manuscripts` 面向 AAAI、ICLR、ACL、CVPR、ICML、NeurIPS、ICCV 等计算机会议的论文工作。
它把方法解释、实验叙述、摘要、图表、统计报告、匿名性、审稿回复和最终文件放在同一个证据边界内处理。
重点是让读者看清：论文解决什么问题，方法改变了什么计算，哪些比较支撑结论，结论在哪里不成立。

本页是作者使用手册，不是自动投稿器或会议政策汇总。
运行指令见 [SKILL.md](../skills/prepare-conference-manuscripts/SKILL.md)。
内置会议适配器是有日期的工程资料；真实任务仍需核对目标会议当前要求。
不要把“顶会风格”理解成统一的三条贡献、固定实验数量或一套可以套用的修辞。

## 安装与调用

按[仓库快速开始](../README.md#快速开始)安装完整目录
`skills/prepare-conference-manuscripts`，然后在所用 agent runtime 中刷新技能列表。
摘要、统计报告、会议适配器和源检查都在这个目录内，不必另装兄弟 skill。

如果您还在仓库根目录，可以这样定义路径并安装需要的 Python 依赖：

```bash
SKILL_DIR="$PWD/skills/prepare-conference-manuscripts"
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
```

已经安装到其他位置时，把第一行替换成包含 `SKILL.md` 的实际绝对目录。
进入论文项目后，`SKILL_DIR` 仍应指向安装目录，而不是当前论文目录。
依赖文件见 [requirements.txt](../skills/prepare-conference-manuscripts/requirements.txt)。
Python 依赖不等于 TeX、Word 或 PowerPoint 渲染器；这些能力由实际工作环境提供。

最有效的首次调用不是“帮我润色到顶会水平”，而是说明目标、证据与交付：

```text
使用 $prepare-conference-manuscripts 处理我的会议论文。
目标会议、年份、track 和阶段见项目说明。先确认适配范围和当前规则。
输入是当前 main.tex、已编译 PDF、bibliography、全部图表、补充材料，
以及结果表和评估协议。先只读审查，说明核心主张是否与证据一致。
输出具体问题、依据和优先修订顺序，不改原稿，不上传文件。
```

当需要修改时，直接说明可写的 revision 目录和允许修改的范围。
原稿已冻结或属于其他作者时，不要让“润色”隐含覆盖授权。
一段图注或一个 rebuttal 问题可以单独处理，不必为了小任务启动全稿流程。

## 选择会议与阶段

先明确 venue、year、track、stage 和这轮动作。
“ICLR 稿件”还不足以区分 conference 与 workshop、匿名稿与讨论修订；
“ACL 投稿”也不能代替 ARR 阶段和后续 venue commitment 的区别。

按准确的 `venue/year/track` 选择适配器。每份 profile 都是有日期的工程辅助；
若范围过时、不匹配目标投稿或当前权威性不确定，先依据当前第一方来源运行 `recon`。
只有没有匹配的当前正式 profile 时才使用 generic；创建任务内 profile，不修改捆绑 profile 来冒充其他范围。
[generic 适配器](../skills/prepare-conference-manuscripts/components/venues/generic/guide.md)
用于这种任务内补充，不是绕过已有正式适配器的通用选项。

各正式适配器链接的已发表论文观察只是可选的经验性写作证据，不是会议规则，也不是强制章节顺序。
可以学习问题、方法和证据之间的连接，但不能借已发表论文的措辞证明当前稿件新颖、有效或合规。

### 各会议适配器分别怎么用

下表反映**仓库内 profile 的范围**，其记录日期均为 2026-09-04。
这不是本页重新联网验证的政策状态，也不能推断后续年份沿用相同要求。

| 适配器 | 捆绑范围 | 开始任务时尤其要核对什么 |
|---|---|---|
| [AAAI](../skills/prepare-conference-manuscripts/components/venues/aaai/guide.md) | AAAI-27 Main Technical Track | 当前作者政策与生成文字的允许范围、匿名材料、checklist、补充包 |
| [ICLR](../skills/prepare-conference-manuscripts/components/venues/iclr/guide.md) | ICLR 2027 Conference | 作者信息状态、样式实际渲染、AI-use 事实、discussion revision 的允许范围 |
| [ACL](../skills/prepare-conference-manuscripts/components/venues/acl/guide.md) | ACL 2026 Main Conference through ARR | ARR 稿件、Author Response、venue commitment 与 camera-ready 的区别 |
| [CVPR](../skills/prepare-conference-manuscripts/components/venues/cvpr/guide.md) | CVPR 2026 Main Conference | anonymous、rebuttal、camera-ready 的样式与文件要求，图和链接匿名性 |
| [ICML](../skills/prepare-conference-manuscripts/components/venues/icml/guide.md) | ICML 2026 Main Track | accepted 样式切换、Impact Statement、评审补充材料与最终制作文件 |
| [NeurIPS](../skills/prepare-conference-manuscripts/components/venues/neurips/guide.md) | NeurIPS 2026 Main Track | main/final/preprint 状态、Paper Checklist、讨论回复与上传权限的区别 |
| [ICCV](../skills/prepare-conference-manuscripts/components/venues/iccv/guide.md) | ICCV 2025 Main Conference | review/rebuttal/camera-ready 样式模式、八页正文边界、未规定的 rebuttal 页数与补充材料大小 |

**AAAI。** 捆绑资料记录了关于 AI-written manuscript text 的政策冲突，并采用较窄的作者政策边界。
因此，真实 AAAI 任务应先核验当前来源，再确定允许的是检查、提纲、作者已有文字润色还是新起草。
不能用这个 skill 的一般 `draft` 能力推断目标阶段允许生成 submission-ready prose；
也不能把生成新段落换个名字叫翻译来回避该问题。
资料同时提供正文与补充材料的科学审查路线，不只是查模板。

**ICLR。** 匿名性要看官方样式如何渲染，不能仅因为源文件有 `author` 命令就断定泄露。
捆绑适配器区分源命令、finalcopy 状态、可见作者信息、PDF metadata 与补充材料。
AI-use 说明需要记录实际任务、工具和人工核对，不从没有记录推断没有使用。
讨论阶段要保留原提交稿，并把每次改动对应到具体意见和允许的修订范围。

**ACL。** 先说明是 ARR submission、author response、commitment 还是录用后制作。
语言模型应用到生物文本的工作仍需写清 NLP 任务、评价对象、数据来源与实际贡献；
不能只靠生物学应用背景替代方法与比较说明。
源检查覆盖该 dated profile 的样式、Limitations 和匿名性相关字段；
responsible-NLP 信息是否真实、正文边界与回复权限仍需实际核对。

**CVPR。** 视觉方法稿件尤其需要让正文、架构图、定性结果和定量比较指向同一任务。
当前项目里的图像样本、切片、患者或视频不能混用为独立单位。
捆绑适配器区分 review、rebuttal 与最终样式，但页数边界、图中身份、
外部链接是否扩展了提交内容、计算报告事实等不能只由 source checker 判定。
处理回复时先核对目标阶段允许的文件，而不是默认可以替换主稿。

**ICML。** 将方法定义、优化或近似过程、测试时程序和评估协议分开解释。
捆绑适配器含匿名与 accepted 状态、Impact Statement 及阶段性文件检查。
“出现了 Impact Statement 标题”不等于内容准确；使用的影响事实还要与方法能力和数据范围一致。
评审时可以提供的补充材料，不一定仍是最终 proceedings 的独立文件，应按当前阶段重建清单。

**NeurIPS。** 明确当前 contribution type 与 main-track 范围，再对照正文、checklist 和声明。
回答 checklist 不是在文稿外写一组更强的承诺；每个答案应能在实际材料中找到依据。
捆绑记录区分 OpenReview discussion 与修订稿上传，讨论许可不能自动变成上传许可。
最终稿重新核对样式、披露和附件，不沿用匿名期的结论。

可以这样启动范围核验：

```text
使用 $prepare-conference-manuscripts 的 recon 模式。
先读项目里记录的 venue/year/track/stage，再选择对应本地适配器。
打开当前官方 author instructions、阶段通知、模板和政策。
把已核实要求、来源冲突、尚未观察到的表单字段分开；
不要用较早年份的 profile 宣称本轮符合规则。完成后给出本次可执行的写作范围。
```

## 准备真正决定写作质量的输入

不必先把所有材料整理成新系统。先指出现有项目里哪份文件是当前权威版本，
再让 skill 读取相关材料；相互冲突的两个结果表不能凭修改时间选一个“看起来更新”的。

| 输入 | 应包含的信息 | 缺失时仍能做什么 |
|---|---|---|
| 研究问题与贡献 | 想解决的具体障碍、贡献类型、最接近的工作 | 梳理问题与证据缺口，不宣布 novelty |
| 方法与实现说明 | 输入、监督、输出、关键计算、训练和推理差异 | 修复解释顺序，未提供细节保持待确认 |
| 评估协议 | 数据来源、划分、可用信息、比较预算、指标方向、选择规则 | 审查已知协议，不能设计一套新协议冒充原实验 |
| 实际结果 | 对应表格、每单位输出、误差或区间、失败情况 | 写有来源的描述，不补造未运行比较 |
| 当前论文材料 | 源文件、编译 PDF、bibliography、图表、appendix/supplement | 说明实际覆盖，缺 PDF 就不能声称检查页面 |
| 版本与审稿材料 | 最后提交稿、完整意见、已完成的新分析 | 区分旧证据、修订和仍未解决的问题 |
| 作者事实 | 作者、伦理、资助、利益冲突、AI use、数据代码状态 | 列出准确的作者核对项，不套用声明 |

AI-for-biology 稿件容易混淆的不是术语，而是评价对象。
例如“未见扰动”“未见剂量”“未见细胞系”和“未见供体”回答不同的泛化问题。
若原实验只留出剂量，不能通过写作把它升级为未见药物预测。
同样，多个随机种子、细胞或视野不能自动变成新的独立生物学样本。

先用一句话固定当前工作真正支持的结论。
再把 title、abstract、contributions、Results 和 conclusion 中的主张定位到表格、图、
定理或实际输出。这个对照可以沿用现有笔记，不要求额外建立复杂元数据系统。

## 从材料起草论文

### 先建立论证，再决定章节分配

如果只有零散笔记，先要求输出“问题—方法改变—判别证据—适用边界”的段落提纲。
提纲的单位是读者需要理解的论点，不是模型模块数量。
每个实验段落应该回答一个问题；每个方法段落应该解释一个必要的对象或操作。

对于方法稿，先看当前最佳相关方法在什么条件下不能完成什么任务，
以及本方法改变的是目标、表示、计算、信息利用还是推理过程。
这个差异需要来自当前方法和文献证据，而非“现有方法忽略复杂生物学”之类笼统缺口。

对于理论、数据资源或系统稿，保持原贡献类型。
不要因为方法难以解释而把它改写成 benchmark，也不要为了套用方法论文结构虚构模型贡献。
任务的科学方向由项目决定，论文 skill 负责忠实表达。

```text
使用 $prepare-conference-manuscripts 起草论文提纲。
依据已提供的方法、协议和结果，先用一句话概括论文回答的问题。
逐段列出要解决的局部问题、对应证据、合理解释和必要限制。
解释每张主图与主表为什么在这里出现；不规定必须三条贡献或固定实验数量。
暂不补缺失实验，先给可写范围和具体缺口。
```

### Introduction：把真实差异写清楚

开头给足理解任务所需的背景，然后尽快缩小到具体未知。
描述最近相关方法已有的能力，再指出与当前设定有关的限制。
一个引用列表不等于 gap 分析；一句“已有方法不能处理”需要对应技术事实与使用条件。

引出方法时说明所改变的计算为什么对这个障碍有用。
贡献句应包含可识别的区别和支持它的证据，不能仅是新命名的模块清单。
删除方法名后，读者仍应知道论文的科学问题是什么。

Introduction 结尾可以概览证据，但不需要重写一遍 Abstract。
把实际没有建立的“机制”“临床效用”或“普适性”从承诺中移除，
同时保留真正建立的积极贡献，而非把整篇论文改成限制清单。

### Method：从对象到操作，再到训练和推理

在使用符号前定义任务输入、监督、输出和可用信息。
沿着贡献改变的计算说明什么被转换、条件化、优化或估计，以及为何这样做。
方程旁要解释它解决的问题；不能只把代码里的函数逐个翻译为段落。

如果模型定义和拟合近似不同，应分别说明。
如果训练时使用标签、对照或额外数据，而推理时不可用，不能在架构图中画成同一条输入路径。
相同术语在 Method、算法框、图和代码说明中指向同一对象。

可要求 skill 对已有文字做这样的定向修改：

```text
只重写 Method 的解释，不改变数学定义或实现。
先定义输入、监督和输出，再解释改变的核心计算；
区分模型定义、训练近似和测试时过程。每个新增技术句必须能在现有材料中找到依据。
若公式、代码或文字互相矛盾，报告具体位置，不自行选择一个版本当作正确答案。
```

本地[方法论证案例](../skills/prepare-conference-manuscripts/references/method-argument-cases.md)
示范如何把贡献、方程和比较联系起来。
这些是写作组织的参考，不是待照搬的模型、超参数或成功实验。

### Experiments：让比较回答问题

先交代读者解释结果所必需的设置：数据与划分、比较方法、信息预算、指标含义、
重复运行如何汇总，以及真正的独立单位。
关键协议不应只藏在 appendix，特别是会改变“公平比较”含义的设置。

把任务表现、机制证据、泛化和资源成本分开陈述。
一个消融去掉了什么，能支持的结论就到什么范围；
一次随机运行没有看见差异，并不证明机制不存在。
只在已经有相关测量时报告效率，不能由更短算法式推断实际更快。

结果段落先说明比较，再给出决定性的观察和范围。
保留强基线、混合排序、不确定或失败条件。
平均值为正时仍可能有关键失败；某个 regime 的优势不能扩展成“所有数据集都领先”。

```text
重写 Experiments，使每节回答一个明确问题。
逐句对照结果表，保留 comparator、信息预算、数据范围、方向和不确定性。
区分 task performance、mechanism、generalization 和 cost 的证据。
不要为凑完整故事添加未运行实验；把改变核心结论的负结果留在主论证中。
```

### Abstract、标题与结尾

等核心主张和证据稳定后，再压缩 Abstract。
它应让读者理解具体问题、方法改变、验证范围、主要结果和支持的答案。
比较型结论需要保留决定其意义的 comparator 和量级；
没有量化结果的能力描述不能为了模板临时编一个“提升百分比”。

标题、Abstract 与结论应承诺同一件事。
标题中的因果或泛化用词要有对应证据，缩短时优先删背景和无用缩写，
而不是删去使结论成立的条件。

摘要字数、是否允许引用和匿名规则按当前目标核对。
本地[摘要与统计指引](../skills/prepare-conference-manuscripts/references/abstract-and-statistics.md)
和[摘要组件](../skills/prepare-conference-manuscripts/components/abstract/guide.md)支持这一步，
但 checker 的 preset 不能替代当年的官方要求。

### 正文、appendix 与 supplement

主文保留判断核心贡献所需的定义、协议、关键比较和会改变主张的限制。
附录可以承载推导细节、额外案例、稳健性和复现资料，
不能因为主文篇幅紧就把最强反例或关键条件挪走。

区分 appendix 是主 PDF 的一部分，还是独立 supplementary file。
不同会议和阶段的提交面不同，不能把本地目录结构直接当成会场允许的提交集合。
整理后检查每个正文引用能否找到对应材料，编号是否仍一致。

## 论文图表与图注

此 skill 可以完成论文语境中的图表，不要求先装另一个绘图技能。
首先给出图的任务：解释方法、比较表现、呈现机制、展示泛化范围，还是说明成本。
复杂图的版式由这些关系决定，不由“凑多少 panel”决定。

方法图里的对象、箭头和训练/推理路径应与 Method 一致。
数据图里的单位、缺失值、归一化、聚合和误差应来自实际数据与分析记录。
定性图说明样本如何选择，不能把好看的例子当成总体证据。
单张主图承担多个任务时，图注需要说明各部分共享或不同的比较范围。

允许制作新示意图时，先实际查看高质量相关实例，提炼构图经验。
默认 GPT Image 2.5 概念稿，再用可用工具直接重建 native editable PPTX。
接口没有暴露模型选择时，如实报告 backend unknown/unverified。
定量图和真实图像保持来源驱动；概念图不能替代测量证据。
具体见[独立绘图路线](../skills/prepare-conference-manuscripts/references/standalone-figures.md)。

```text
根据现有 Method 和 Results 制作论文图表，先说明每张图回答的问题。
方法图保持对象、符号、训练与推理路径一致；数据图只使用提供的源数据。
先查看相关优质图的构图，再制作允许的概念稿和 native PPTX。
交付可编辑 master、需要的导出与实际渲染检查；不改变已批准图件或科学协议。
```

图注不只描述颜色和形状。
它需要让读者识别比较、数据范围、点/线/误差的含义和适用单位。
如果统计信息缺失，提出具体作者问题，不复制相邻图的 `n` 或检验名称。
Source-data、正文、图和图注的分母应一致。

## 修改已有稿件

<a id="section-polish"></a>

### 逐节打磨与继续下一节

如果希望一节一节修改并可靠续行，使用内置的
[逐节打磨流程](../skills/prepare-conference-manuscripts/references/section-polish-workflow.md)。
它仍属于 `polish`，不是新增模式。先确定唯一稿件版本、可写副本和本次章节范围，
按实际标题建立队列；默认一次完成一节，明确授权连续处理整篇时可以逐节继续，不重复请求批准。

每节先明确它要建立的论点，再对应段落任务与实际证据，随后做局部有据修订。
数字、单位、比较方向、否定、限定和引用范围保持不变。
验收包括对照实际来源、检查修改前后内容，以及使用项目现有方式检查受影响的成品：
LaTeX 需要时编译并看受影响页面，Word 或其他格式用其实际渲染路径；纯文本交付检查文本和链接。
不要求每节重复整稿全套检查，也不把缺渲染器的 `not_run` 写成已验收。

```text
使用 $prepare-conference-manuscripts 的 polish，先只打磨 Method 这一节。
以我指定的当前稿件和已授权 revision 副本为准，沿用项目已有进度记录。
先说明本节论点与每段工作，再根据现有方法和结果来源局部修订。
保留科学定义和数值，检查实际 diff 与受影响页面。
完成后记录证据位置、改动、真实验证结果、未解决项和下一节；本轮不要改其他章节。
```

下一次不必重新描述整篇任务，可以说：

```text
继续下一节。先读已有 checkpoint，核对当前稿件和证据是否仍是上次版本。
如果上节来源、图或正文有变，重开受影响项，不直接沿用旧 done。
在已有授权范围内处理下一节；关键证据冲突保持未解决，不跳过后标记完成。
```

进度写回项目已有 checkpoint，只在没有合适记录时建立简短的本地作者工作记录。
记录不进入正文、supplement 或投稿包，也不要求固定日志名、每节 Git 提交或额外代理。
它用于判断哪里真正改过、哪里验收失败和下一项是什么，不是另一套研究管理流程。

明确要求“按队列连续处理我授权的所有章节”后，可以逐节完成，不必每节停下来要确认。
关键证据异常只停止受影响的修改与验收，独立且已授权的工作可以继续，但未解决项仍然可见。
只有单节授权时，完成该节和必要的相邻文字、引用一致性检查，不扩成整篇审查。
多节或整稿队列全部验收后，再对授权范围及其依赖做一次跨节、主补、图表引用和成品一致性检查。
只完成一节不等于整稿完成；逐节完成也不自动包含投稿打包。
如果请求同时包含全稿润色与打包，仍遵循下方 whole-paper 的先审查边界，最终核对复用同一次有效验收。

### 先修逻辑，再修句子

读完当前版本后，让 skill 为每段写一句“这段正在完成什么工作”。
这会暴露重复铺垫、没有支持的跳跃、提前使用的定义，以及章节间没有必要性的顺序。
再决定哪些段落需要移动、合并或拆分，最后处理句子节奏和术语。

全稿请求应覆盖所有提供的章节，而不是只润色摘要和开头。
精读范围、未提供部分和只做抽查的内容应在交付中明确。
不必要的修辞统一可能破坏信息密度，应以具体问题为单位修改。

```text
使用 $prepare-conference-manuscripts 审查并修改整篇稿件。
先做 reverse outline 和 claim-evidence 对照，再按问题优先级修改副本。
覆盖全部已提供章节、图注和附录引用，保留数字、否定词、方向、单位和引用范围。
交付逐项修改说明与未解决问题；不要把整篇重写成同一种句式。
```

对于“润色并打包”的组合请求，运行
[全稿工作流](../skills/prepare-conference-manuscripts/references/full-paper-workflow.md)。
它先 intake、必要的 recon 和 audit，再在通过边界后修改副本与打包。
未解决 P0、缺少科学协议或关键结果无支持时，状态为 `NOT READY`，不推进受影响的 polish/package。

### 统计与评价表达

核对独立单位、样本层级、配对或重复测量、排除与缺失、估计对象、
区间或离散程度、比较族及实际使用的检验。
重复种子、fold、细胞、切片或技术重复分别起什么作用，不能用一个笼统的 `n` 混过去。

润色不自动获得重新设计统计的权限。
如果实际分析和稿件不一致，先定位冲突；必要的新分析应明确为研究任务。
不能在改句子时补一个检验、把事后分析写成预注册，或将不显著解释为等效。

### 引用与最近相关工作

核心 novelty 句需要当前第一方来源支撑。
邻近工作应说明相同点、实际差异和对比较的影响，不能仅因标题相似宣判完全相同。
也不能因工作不完全相同就不讨论其方法或基线作用。

引用应贴合句子的具体主张。压缩段落时不要让原先只支持半句的引用变成支持整段。
未打开的论文、缺少的补充文件和未确认的细节保持明确状态。

## Rebuttal 与讨论修订

先读取完整意见和最后提交版本，再安排回复顺序。
一个 reviewer 的一段话可能有多个关切，不能只回应其中最容易的一项。
保留意见层级，先处理决定性问题，但最终覆盖全部 material comments。

本地[回复指引](../skills/prepare-conference-manuscripts/references/rebuttal-and-revision.md)
区分纠错、澄清、完成的新证据、有依据的不同意、部分解决和接受限制。
这比把每条意见都写成“感谢，我们已解决”更准确。

| 关切 | 应给出的回应 | 不应替代它的内容 |
|---|---|---|
| 事实或表述错误 | 承认具体错误、修正文句、定位改动 | 泛泛道歉而不改正文 |
| 方法不清楚 | 用现有定义、方程或流程解释 | 新增未实现模块 |
| 缺少比较 | 已有证据或获授权完成的新分析 | 把拟开展实验写成结果 |
| 对范围有异议 | 说明证据边界，必要时缩窄主张 | 用更强修辞反驳 |
| 复现问题 | 实际命令、材料与检查结果 | 只写“代码会公开” |
| 合理但未完成的要求 | 部分解决、具体限制与未运行状态 | 隐去未解决部分 |

```text
使用 $prepare-conference-manuscripts 的 rebuttal 模式。
以最后提交稿为基准，逐条保留 reviewer/chair 的实际关切。
为每条列出现有依据、回应决定、拟修改位置和仍未解决的问题，再写回复。
只引用已完成且已检查的新分析；需要新实验时另列，不承诺其结果。
最后核对回复声称的每项改动确实出现在允许修改的稿件中。
```

会议 rebuttal、OpenReview discussion 与期刊 revise-and-resubmit 不是同一个文件。
先核对允许回复的格式、长度和修订面，不能默认允许上传新主稿或新补充文件。
公开回复、上传附件或修改 portal 都是外部动作，不因本地回复写好而自动执行。

## Camera-ready 与交付

从接受稿或作者批准的基准版本开始，而不是从另一个“最新”目录开始。
将会场要求、回复中承诺的改动、作者批准的可选改动分开，
并核对是否出现超出允许范围的科学变化。

检查标题、作者、单位、致谢、声明、样式状态、图表和补充引用。
匿名阶段需要隐藏的内容未必应继续隐藏；最终阶段新增的声明也不能借用其他论文的事实。
作者同意、资助、伦理和相关稿件状态只能由已确认资料支持。

```text
使用 $prepare-conference-manuscripts 的 camera-ready 模式。
输入是接受稿、决定信、完整回复、当前官方最终稿说明和作者确认事实。
逐项核对承诺修改，更新获准的身份与声明，生成候选源文件和 PDF。
比较基准与候选，检查图表、附录、数据代码引用及最终附件集合。
只准备本地交付，不上传或提交。
```

### 源检查与页面检查各负责什么

[manuscript-core](../skills/prepare-conference-manuscripts/components/manuscript-core/guide.md)
包含 TeX、PDF、archive 与 review-report 工具。
它们能检查部分样式、stage、metadata 和文件问题，
不能证明页面视觉正确、核心论证成立或 portal 已保存。

如果真实任务已经确认 ICLR profile 适用，且当前论文目录确有 `main.tex` 和 `main.pdf`，
可以沿用前面已定义的安装路径运行：

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" main.tex \
  --profile "$SKILL_DIR/components/venues/iclr/references/venue-profile.json" \
  --stage anonymous_submission
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_pdf.py" main.pdf \
  --profile "$SKILL_DIR/components/venues/iclr/references/venue-profile.json" \
  --stage anonymous_submission
```

这只是已有命令的调用方式，不表示当前稿件应投 ICLR 或该 profile 已完成实时核验。
其他会议使用其对应且已确认的 profile；不要仅替换年份字符串。
页数、参考文献边界、可见身份、字体、裁切、公式、浮动图表、图注和链接需检查实际渲染页面。
没有 PDF 或渲染环境时，报告精确的 `not_run` 部分，不把源检查当成页面验收。

### 最终应该收到什么

组合全稿任务按[交付骨架](../skills/prepare-conference-manuscripts/assets/full-paper-deliverables.md)返回：

1. 输入清单、适用范围和缺少材料；
2. 主张到证据的对应及冲突；
3. 有位置、影响和最小处理方式的 P0/P1/P2 报告；
4. 有顺序的修订计划；
5. 实际修订 diff，或没有修改的原因；
6. 本地验证、人工检查覆盖与 `READY` / `NOT READY` 状态。

单项任务按实际请求交付，不必生成不相关文件。
所有“完成”“检查过”“已修改”应对应可观察材料；本地 READY 不等于已上传、已提交或会被接收。

## 常见问题与可选工具示例

**只有结果，没有完整论文，能开始吗？** 可以先做提纲和证据组织。
缺方法、拆分或对照信息时，应指出缺口，不把想象的实验流程写入 Methods。

**能保证达到顶会水准吗？** 不能保证接收，也不能用写作补足科研贡献。
它能改善问题—方法—比较的可读性，检查证据与文件的一致性，并留下真实未解决问题。

**没有额外绘图 skill 能否完成论文图？** 可以，绘图路线已内置。
复杂版式可由可用的专项技能增强，但不是完成本任务的前置安装。

**只希望熟悉本地工具？** 可选的
[机械检查示例](../skills/prepare-conference-manuscripts/examples/showcase/README.md)
演示 CSV 图渲染和 TeX 源检查。它使用六行构造数据，不代表顶会论文的内容、图件或方法质量，
也不是本手册的主要起点。

维护时按需安装[测试依赖](../requirements-test.txt)，从仓库根目录运行：

```bash
python3 -B -m unittest discover -s tests/conference-manuscripts -p 'test_*.py'
```

[期刊手册](journal-manuscripts.md) · [科研绘图](scientific-visualizations.md) ·
[贡献说明](../CONTRIBUTING.md) · [第三方条款](../THIRD_PARTY.md) · [许可证](../LICENSE)
