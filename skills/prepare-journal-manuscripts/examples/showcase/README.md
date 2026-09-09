# 期刊稿完整案例：让六组配对记录贯穿正文与编辑回复

这是 synthetic AI-for-biology 报告练习，不是生物研究、已接收文章或期刊政策示例。
它借响应预测研究的背景，示范怎样修复单位、因果与数据存放的表述。
没有运行模型、采集标本或施加治疗；六行数值全部为手工构造。

![六个构造标本的 baseline 与 follow-up 配对值。](preview.png)

## 输入与可读输出

| 文件 | 用途 |
|---|---|
| [case-brief.md](case-brief.md) | 背景、六组值、配对单位和可用于交互练习的任务请求 |
| [observations.csv](observations.csv) | 六个构造标本，每行两个配对值 |
| [before.md](before.md) | 故意夸大样本数、因果、泛化和外部存储的初稿 |
| [after.md](after.md) | 一致的 Results、Methods、完整 legend、Data availability 和 Limitations |
| [editorial-response.md](editorial-response.md) | 人工 cover-note 片段与模拟编辑回复 |
| [figure.json](figure.json) | 来源于 CSV 的图规格 |
| [analysis-missing-unit.json](analysis-missing-unit.json) | 故意缺少独立单位的报告记录 |
| [analysis-complete.json](analysis-complete.json) | 完整的描述性配对展示记录，不声称做了推断 |
| [data-inventory.json](data-inventory.json) | 指向实际提供的 source CSV |
| [preview.png](preview.png) | 由所提供渲染器生成并随案例提供的图 |

修订正文和编辑材料是预先编写的教学参照，不是运行脚本后的隐藏输出，
也不是受控 agent 行为评测记录。脚本只负责图渲染与指定记录检查。

## 从哪一步修起

第一步是读 ID 和配对关系，而不是先改语言。六个标本各有两个值，共十二个测量值，
不等于十二个独立标本。四组 follow_up 较高、两组较低；没有真实治疗或人群抽样。

> 修改前：Twelve independent samples prove that the treatment improves response and
> generalizes to the wider population.
>
> 修改后：Six constructed specimens each contribute one baseline and one follow-up
> value. Follow-up exceeds baseline for four specimens and is lower for two.

第二步是让每个部分承担明确工作：

| 部分 | 具体修改 | 保留的限制 |
|---|---|---|
| Results | 六个标本、四高两低，保留所有记录 | 不宣称因果或泛化 |
| Methods | 一行一个标本、两个配对值、无排除 | 不编统计检验、模型或区间 |
| Legend | 单位、n、横纵轴、来源和无误差条 | 点不是组均值，图不是治疗效果估计 |
| Data availability | 指向随案例提供的 observations.csv | 无外部存储或 accession |
| 编辑回复 | 每条意见对应上述具体修改 | 改了表述不等于完成新实验 |

[完整修订稿](after.md) 保留英文科研表达，[编辑材料](editorial-response.md)解释如何回应审稿意见。
真实研究应以实际设计和运行结果取代教学设定，而非仅去掉 synthetic 标签。

## 实际运行：数据图与记录检查

默认当前目录为仓库根目录。独立安装用户把第一行换为包含 `SKILL.md` 的实际绝对目录；
其余命令不依赖仓库父目录或其他 skill。需要 Python 3.9+ 与 requirements，
不需要文档渲染器、图像服务或账号。

```bash
SKILL_DIR="$PWD/skills/prepare-journal-manuscripts"
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
DEMO="$SKILL_DIR/examples/showcase"
DEMO_OUT="$(mktemp -d)"
MPLCONFIGDIR="$DEMO_OUT/.mpl" XDG_CACHE_HOME="$DEMO_OUT/.cache" \
  python3 "$SKILL_DIR/scripts/render_evidence_figure.py" \
  "$DEMO/figure.json" "$DEMO_OUT/figure"
```

预期 exit 0，生成 `$DEMO_OUT/figure.svg`、`figure.pdf`、`figure.png`。
打开预览查看所有六点；SVG 保留可编辑文字，PDF 是矢量。
每点横坐标为 baseline、纵坐标为 follow_up，均为任意单位。

下一条是**故意失败**，请单独运行；避免遇错退出的 shell 停在这里后误以为整个例子结束：

```bash
python3 "$SKILL_DIR/components/statistics-reporting/scripts/validate_analysis_register.py" \
  "$DEMO/analysis-missing-unit.json" --mode final --format markdown
```

预期 exit 1，一条 `INDEPENDENT_UNIT` error。随后运行完整记录：

```bash
python3 "$SKILL_DIR/components/statistics-reporting/scripts/validate_analysis_register.py" \
  "$DEMO/analysis-complete.json" --mode final --format markdown
```

预期 exit 0，`PASS`，零 errors/warnings。两份 JSON 仅在独立单位字段是否填写上不同，
这个对照不证明 validator 读懂了文稿或重新计算了样本数。

```bash
python3 "$SKILL_DIR/components/data-availability/scripts/validate_data_inventory.py" \
  "$DEMO/data-inventory.json" --mode final --format markdown
```

预期 exit 0，`PASS`，零 errors/warnings。清单使用 `within_paper_or_supplement`，
只表示此教学例附带源文件。日期是 fixture 日期，不是期刊政策核验或外部存储检查。

## 能交付什么，不能推出什么

你可以直接阅读修订稿、完整图注、编辑说明与回复；也能重画来源数据图并运行三个记录检查。
但这些程序不会生成或修订正文，不判断因果设计，不验证 raw-data counts 或仓库访问，
不选择适当统计方法，也不进行假设检验。

本例不渲染完整稿件、不制作 tracked-change 文档、不生成图像概念稿或 native PPTX，
也不向编辑发信。实际任务中这些是可另行完成、必须如实说明状态的工作，
不是一次 PASS 自动包含的结果。
