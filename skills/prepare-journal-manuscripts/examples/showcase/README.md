# 可选机械检查：期刊稿本地工具

本目录只用于熟悉图文件导出、分析记录字段和数据清单校验。
它不是 Nature-family 文章、专业图件或生物学证据展示。
六组配对值均为预设的 synthetic 数据，没有模型运行、真实标本或治疗。

真实任务请从安装目录中的 [期刊稿入口](../../SKILL.md) 开始，
提供具体期刊、文章类型、当前阶段、正文、Methods、图注、结果及数据访问事实。
无需先运行这个练习；它不能替代完整文章组织、逐节修改或编辑材料工作。

## 安装位置与输出

默认当前终端位于仓库根目录。独立安装用户把第一行换成包含
`SKILL.md` 的实际绝对目录；其余资源随这个 skill 提供。
需要 Python 3.9+ 与 requirements，不需要文档渲染器、图像服务或账号。

```bash
SKILL_DIR="$PWD/skills/prepare-journal-manuscripts"
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
DEMO="$SKILL_DIR/examples/showcase"
DEMO_OUT="$(mktemp -d)"
```

下面的命令使用同一终端中的变量。新建输出目录保留已有导出。

## 可选运行一：确认来源数据图能够导出

```bash
MPLCONFIGDIR="$DEMO_OUT/.mpl" XDG_CACHE_HOME="$DEMO_OUT/.cache" \
  python3 "$SKILL_DIR/scripts/render_evidence_figure.py" \
  "$DEMO/figure.json" "$DEMO_OUT/figure"
```

预期 exit 0，生成 `$DEMO_OUT/figure.svg`、`figure.pdf`、`figure.png`。
[figure.json](figure.json) 将 [observations.csv](observations.csv) 的 baseline 与 follow_up
映射到每个点的横纵坐标。六行均显示，不含模型拟合、误差条或统计检验。

这只是小型导出检查，不演示专业复合图、真实图像处理、机制图或 native PPTX 制作。
仍需打开实际输出检查，不能用脚本成功代替论文图件验收。

## 可选运行二：检查缺失的独立单位字段

下一条是故意失败的对照，请单独运行，避免遇错退出的 shell 停止后续步骤：

```bash
python3 "$SKILL_DIR/components/statistics-reporting/scripts/validate_analysis_register.py" \
  "$DEMO/analysis-missing-unit.json" --mode final --format markdown
```

预期 exit 1，一条 `INDEPENDENT_UNIT` error。随后检查完整记录：

```bash
python3 "$SKILL_DIR/components/statistics-reporting/scripts/validate_analysis_register.py" \
  "$DEMO/analysis-complete.json" --mode final --format markdown
```

预期 exit 0，`PASS`，零 errors/warnings。
[不完整记录](analysis-missing-unit.json)与[完整记录](analysis-complete.json)
只在 `independent_unit` 字段是否填入上不同。
这个例子证明指定缺字段会被报告，不证明 validator 读懂了正文、数过原数据或选择了正确分析。

## 可选运行三：检查数据清单

```bash
python3 "$SKILL_DIR/components/data-availability/scripts/validate_data_inventory.py" \
  "$DEMO/data-inventory.json" --mode final --format markdown
```

预期 exit 0，`PASS`，零 errors/warnings。
[data-inventory.json](data-inventory.json)使用 `within_paper_or_supplement` 路线，
只说明此教学例附带 source CSV。没有外部存储或 accession，
日期也不是期刊政策或仓库访问的核验日期。

真实 Data Availability 需要覆盖支持主文和补充主张的全部数据及实际访问路线，
不是填完这个 JSON 就自动得到可投稿声明。

## 随附的教学对照材料

以下文件保留为可选阅读，不是专业期刊稿件模板、脚本输出或实际 agent 执行记录：

- [case-brief.md](case-brief.md)：六组构造值与配对关系；
- [before.md](before.md)：故意错误的样本数、因果和数据存放说明；
- [after.md](after.md)：预先准备的短 Results、Methods、legend 和可用性说明；
- [editorial-response.md](editorial-response.md)：教学 cover-note 与虚构编辑回复。

六个构造标本各有两个值，不能写成十二个独立标本。
四组 follow_up 较高、两组较低，不代表治疗有效或模型表现。
这些边界用于理解字段检查与科学解释的区别，不应成为真实论文的内容替代品。

## 这次练习没有覆盖的工作

程序不会修订正文、判断因果设计、验证原始样本数或访问外部仓库。
它不做假设检验、不渲染完整稿件、不产生 clean/marked 返修文档，
不发送编辑信、不提交文件。真实交付应分别说明哪些写作、数据核对和页面检查确实完成。
