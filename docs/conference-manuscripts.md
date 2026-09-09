# 会议论文：把方法与证据写成可审阅的稿件

[返回仓库首页](../README.md) · [安装](#安装与运行位置) · [完整教学案例](../skills/prepare-conference-manuscripts/examples/showcase/README.md) · [运行入口](../skills/prepare-conference-manuscripts/SKILL.md)

`prepare-conference-manuscripts` 用于计算机领域会议论文的起草、审查、润色、返修和本地交付。
适合“方法已经说清、结果已经得到，但论文尚未把问题、机制和证据连起来”的任务，
也适合对已有稿件逐项核对。它不会替你补出实验，或把一组不利结果写成全面领先。

这里是面向作者的中文使用指南；运行时的英文 skill 指令保持独立。
你可以只安装这一个完整目录，不需要另装摘要、统计或绘图 skill。

## 从你的任务开始

| 你现在有什么 | 怎么用 | 你应收到什么 |
|---|---|---|
| 问题、方法简述、结果表，还没有正文 | `draft` | 段落提纲、方法说明、Abstract/Results/Limitations 草稿及缺失证据 |
| 已有稿件，但主张与结果可能不一致 | `audit` | 具体位置、问题影响、依据和最小修订建议 |
| 证据稳定，希望改善表达 | `polish` | 保留数字、方向、不确定性和引用范围的修订副本 |
| 收到 reviewer comments | `rebuttal` | 逐条回应、完成与未完成工作的区分、正文修改位置 |
| 录用后修改或准备提交文件 | `camera-ready` / `package` | 对照基准版本的本地候选包、实际渲染检查和待作者确认项 |
| 会议、年份、track 或阶段不明确 | `recon` | 当前官方要求、来源和尚未确认的问题 |

“润色并打包”会先做 intake 和 audit，再修改与核对；参见
[全稿工作流](../skills/prepare-conference-manuscripts/references/full-paper-workflow.md)。
缺少支撑核心结论的证据、科学协议未明确或 P0 未解决时，仍是 `NOT READY`。
这不妨碍先完成独立可做的修订，但不能通过润色宣布已可投稿。

## 带哪些材料，输出到哪里

最少带上目标 venue/year/track/stage、希望做的动作、稿件或提纲、方法简述、结果及限制。
已有实验还应提供数据划分、比较方法、指标方向、独立单位、排除项和不确定性。
“表格里有数”不等于这些信息已知；可先让 skill 列出具体缺口。

完整修改任务可再带 bibliography、图和 source data、最后提交版本、审稿意见，以及已确认的作者、
伦理、资助和声明事实。不要要求它从其他项目复制这些事实。

约定一个新的 revision 目录。交付可以包括修订正文、claim-to-evidence 对照、图注、审稿回复、
变更清单和渲染后的候选文件。已有 canonical/frozen 稿件不因这份指南自动获得覆盖权限。
只读审查请明确“只报告，不改文件”。上传、投稿系统操作与联系会议是另外的授权动作。

## 教学案例：六个任务不足以支持“全面领先”

![六个手工构造任务的基线与候选得分。](../skills/prepare-conference-manuscripts/examples/showcase/preview.png)

场景是一个**虚构的细胞扰动响应预测方法比较**。方法简述提出如何使用细胞状态与扰动描述，
但没有训练模型或运行生物学实验。已有的 [scores.csv](../skills/prepare-conference-manuscripts/examples/showcase/scores.csv)
只含六个手工构造的任务得分，不能解释为该方法测得的性能。

[完整案例](../skills/prepare-conference-manuscripts/examples/showcase/README.md) 把以下材料接起来：

| 阅读顺序 | 材料 | 写作时解决的问题 |
|---|---|---|
| 1 | [方法与证据简述](../skills/prepare-conference-manuscripts/examples/showcase/case-brief.md) | 哪些是设想的方法，哪些是已有数值，哪些尚未做 |
| 2 | [提纲与英文稿件片段](../skills/prepare-conference-manuscripts/examples/showcase/manuscript-example.md) | 用一个问题组织 Abstract、Results 和 Limitations |
| 3 | [原始错误片段](../skills/prepare-conference-manuscripts/examples/showcase/before.tex) / [修正版](../skills/prepare-conference-manuscripts/examples/showcase/after.tex) | 从“所有任务领先”收窄为实际支持的比较 |
| 4 | [模拟审稿回复](../skills/prepare-conference-manuscripts/examples/showcase/reviewer-response.md) | 回应泛化与缺失实验，不把计划写成完成 |
| 5 | 下方可运行命令 | 真正重画数据图并检查 TeX 源缺陷 |

修订后的核心句是：

> In six illustrative tasks, the candidate score is higher on four tasks and lower on two.
> The mean paired difference is 0.005 arbitrary score units.

这些段落、提纲和回复是**预先编写的教学示例**，不是后面的脚本输出，也不是受控 agent 行为评测记录。
脚本能画图和查源文件；解释六行数据、收窄科学结论仍需阅读证据。

## 安装与运行位置

按[仓库安装说明](../README.md#快速开始)获取仓库，把完整
`skills/prepare-conference-manuscripts` 目录放到你的 agent runtime 所使用的位置并刷新技能列表。
不要只复制 `SKILL.md`。以下命令默认当前终端位于仓库根目录：

```bash
SKILL_DIR="$PWD/skills/prepare-conference-manuscripts"
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
```

若使用已经安装的副本，把第一行改成**那个实际目录的绝对路径**，即包含 `SKILL.md` 的目录。
后续命令均从 `$SKILL_DIR` 找资源，不依赖其他 skill。需要 Python 3.9+；
`pypdf==6.10.2` 用于 PDF 审查，`matplotlib==3.9.4` 用于数据图，
`python-pptx==1.0.2` 或可用演示工具用于 native PPTX。具体依赖见
[requirements.txt](../skills/prepare-conference-manuscripts/requirements.txt)。
实际 TeX/Word/PPTX 渲染器和图像生成服务是另行提供的能力，下面的 demo 不需要它们。

## 可运行的小例子

在同一个终端中，接着运行：

```bash
DEMO="$SKILL_DIR/examples/showcase"
DEMO_OUT="$(mktemp -d)"
MPLCONFIGDIR="$DEMO_OUT/.mpl" XDG_CACHE_HOME="$DEMO_OUT/.cache" \
  python3 "$SKILL_DIR/scripts/render_evidence_figure.py" \
  "$DEMO/figure.json" "$DEMO_OUT/figure"
```

这一步应 exit 0，生成 `$DEMO_OUT/figure.svg`、`figure.pdf`、`figure.png`。
SVG 保留可编辑文字，PDF 是矢量输出，PNG 是预览。新输出目录保留之前的结果；
打开实际图片检查，而不只读终端成功消息。

下面是**故意失败**的检查，请单独运行；若 shell 启用了遇错退出，不要与后续命令串成一组：

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" \
  "$DEMO/before.tex" --profile "$DEMO/demo-profile.json" \
  --stage anonymous_submission --format markdown
```

预期 exit 1，报告 `ANON_SOURCE_IDENTITY` 和 `ANON_ACKNOWLEDGMENTS`。
接着检查已提供的修正版：

```bash
python3 "$SKILL_DIR/components/manuscript-core/scripts/audit_tex.py" \
  "$DEMO/after.tex" --profile "$DEMO/demo-profile.json" \
  --stage anonymous_submission --format markdown
```

预期 exit 0，`Findings: 0`。教学 profile 要求 article、graphicx、摘要，并在此虚构匿名阶段检查
作者命令和致谢块；它不是任何真实会议的政策。这个 checker 不会把 before 自动改成 after，
也不验证“平均差 0.005”、图中科学解释或最终 PDF 匿名性。

## 可直接改写使用的任务请求

### 从方法简述起草

```text
使用 $prepare-conference-manuscripts 的 draft 模式。
先读我提供的方法简述、结果表、评估协议和目标会议信息。
先给出围绕一个科学问题的段落提纲，再起草 Abstract、Method、
Results 和 Limitations。每个结果句标出来源，缺少实验处明确留空。
在新的 revision 目录写文件，不改原稿，不编造训练细节、比较值或引用。
```

### 修改已有稿件

```text
使用 $prepare-conference-manuscripts 审查并润色这份稿件。
先核对 Abstract、contributions 和 Results 是否由同一组证据支持。
保留全部数字、不利结果、统计单位和引用范围。先列具体问题，再在副本修订。
交付修改说明、修订稿和仍需作者确认的事项；不要执行投稿。
```

### 回应审稿意见

```text
使用 $prepare-conference-manuscripts 的 rebuttal 模式。
输入是最后提交稿、完整审稿意见和已经完成的新分析。
逐条说明对方关切、回应依据、正文修改位置和仍未完成的工作。
不要把拟开展实验写成已完成；没有证据支持的意见可以说明限制并收窄结论。
```

## 会议范围与图示

正式适配器包括 [AAAI](../skills/prepare-conference-manuscripts/components/venues/aaai/guide.md)、
[ICLR](../skills/prepare-conference-manuscripts/components/venues/iclr/guide.md)、
[ACL](../skills/prepare-conference-manuscripts/components/venues/acl/guide.md)、
[CVPR](../skills/prepare-conference-manuscripts/components/venues/cvpr/guide.md)、
[ICML](../skills/prepare-conference-manuscripts/components/venues/icml/guide.md) 和
[NeurIPS](../skills/prepare-conference-manuscripts/components/venues/neurips/guide.md)。

按准确的 `venue/year/track` 选择适配器。每份 profile 都是有日期的工程辅助；
若范围过时、不匹配目标投稿或当前权威性不确定，先依据当前第一方来源运行 `recon`。
只有没有匹配的当前正式 profile 时才使用 generic；创建任务内 profile，不修改捆绑 profile 来冒充其他范围。
具体见 [generic 适配器](../skills/prepare-conference-manuscripts/components/venues/generic/guide.md)。
各正式适配器链接的已发表论文观察只是可选的经验性写作证据，不是会议规则，也不是强制章节顺序。
仓库不捆绑会议拥有的样式文件或论文范文；示例日期不证明政策仍然有效。

允许制作新方法、架构、流程或 motivation 示意图时，先实际查看相关高质量示例，
提炼阅读顺序、分组、层次与标签密度，不搬用对方数据、科学结论或专有图稿。
默认使用 GPT Image 2.5 概念稿，再用当前可用工具直接重建 native editable PPTX。
接口未提供模型选择时，照实报告 backend unknown/unverified，不认证具体版本。
数据图始终从实际来源绘制；上面的散点图不是概念图到 PPTX 的展示。
[独立绘图路线](../skills/prepare-conference-manuscripts/references/standalone-figures.md)
包含此 skill 自身所需指引；复杂多面板设计也可参考[科研绘图指南](scientific-visualizations.md)。

## 常见问题

**没有完整实验也能起草吗？** 可以组织已有材料和缺口，但不能补造结果或宣布 submission-ready。
明确是研究计划、教学案例还是已经完成的研究。

**只想润色，会重新设计我的方法吗？** 不应如此。既定科学协议是边界；方法、数据划分或核心结论
需要改变时，应说明具体问题并取得相应决定，不能藏在语言修改里。

**为什么坏例子返回 1？** 这是预期发现源缺陷。exit 2 表示输入/profile 无法使用，
不是又发现一条论文问题；修正版意外失败应读取实际错误。

**检查零问题等于可投稿吗？** 不等于。source audit 没有证明页面布局、科学有效性或最新会议合规。
真实稿件仍需当前规则、渲染页面和作者声明核对。

**没有图像服务或 TeX 环境怎么办？** 完成独立可做的正文和源检查，明确哪一步未运行。
不要把 SVG 或一张图片称为完整 native PPTX，也不要把未渲染源文件称为已检查 PDF。

## 维护与相关指南

开发检查从仓库根目录运行，按需安装[测试依赖](../requirements-test.txt)：

```bash
python3 skills/prepare-conference-manuscripts/components/abstract/tests/run_selftest.py
python3 -B -m unittest discover -s tests/conference-manuscripts -p 'test_*.py'
python3 scripts/check_public_content.py .
```

[期刊论文指南](journal-manuscripts.md) · [贡献说明](../CONTRIBUTING.md) ·
[维护者](../MAINTAINERS.md) · [第三方条款](../THIRD_PARTY.md) · [Apache-2.0](../LICENSE)
