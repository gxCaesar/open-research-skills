# 空间多组学案例：从四张表到 14-panel 复合图

这个完整教学任务展示如何把空间位置、分子层和 donor 配对比较放在同一页。最终成品是一张 183 × 170 mm 的矢量复合图；每个面板都有对应的数据来源和叙事用途。

全部 17,280 个 cell、12 个配对 donor 标识、分子值与 locus tracks 均为人工构造的 synthetic 数据。坐标点不是显微图，生成器插入的空间模式也不是研究发现。

[查看 PDF](preview/spatial-multiomics-atlas.pdf) · [查看 SVG](preview/spatial-multiomics-atlas.svg) · [完整图注](legend.md)

## 1. 任务与输入

教学问题是：怎样同时呈现空间局部结构、多分子层和 donor 内条件比较，而不让十四个面板变成同等大小的图表清单？

| 输入表 | 一行代表什么 | 用途 |
|---|---|---|
| [cells.csv](data/cells.csv) | 一个 donor-condition 下的合成 cell | state、x/y、径向位置和六个分子值 |
| [assays.csv](data/assays.csv) | 一个 donor-condition-feature | 十项任意单位 assay 汇总，C/P 完整配对 |
| [tracks.csv](data/tracks.csv) | 一个 assay-condition-position bin | 三个人工 locus tracks，不对应真实 genome assembly |
| [regions.csv](data/regions.csv) | 一个选定 field/ROI | 明确 donor、condition 与裁切坐标 |

跨 assay 的关系通过 donor ID 连接，不以数组位置猜配对。读取器会拒绝重复、非有限、缺失或不匹配的 assay 单位，并检查 donor 的两个 cell 条件。这是固定教学表结构，不是任意 assay 的导入工具。

## 2. 交给 agent 的完整请求

```text
使用 build-scientific-visualizations。
阅读本例的四份 CSV、render.py 与 legend.md，说明十四个面板的阅读顺序。
在副本中制作一张空间多组学复合图：空间锚图与同源 ROI 先建立位置，
分子矩阵和 donor 配对比较承接结果，保留 null 与敏感性面板。
不要改变值、配对或分析定义。交付 PDF/SVG、PNG 与同步图注。
```

这条请求演示 agent 如何读材料并组织图件。下面的脚本则直接重画随附场景，两者不是同一种能力测试。

## 3. 本地重画

从克隆仓库根目录设置路径。若已单独安装，把 `SKILL_DIR` 改为含 `SKILL.md` 的实际目录，保留其余命令：

```bash
SKILL_DIR="$PWD/skills/build-scientific-visualizations"
python3 -m pip install -r "$SKILL_DIR/requirements.txt"
DEMO_OUT=$(mktemp -d)
export MPLCONFIGDIR="$DEMO_OUT/.mpl"
export XDG_CACHE_HOME="$DEMO_OUT/.cache"
python3 -B "$SKILL_DIR/examples/spatial-multiomics-atlas/render.py" \
  --output "$DEMO_OUT/atlas"
```

建议在虚拟环境中按需安装。无需另一个 skill、图像模型、账号、下载数据或 GPU。脚本使用自身位置寻找辅助工具，因此完整目录移到别处后仍可运行。

实际输出：

```text
atlas/
  spatial-multiomics-atlas.pdf
  spatial-multiomics-atlas.svg
  spatial-multiomics-atlas.png
```

终端摘要包含 `panels: 14`、`donors: 12`、`cells: 17280`、`width_mm: 183`、`height_mm: 170`、`text_overflows: 0`，并报告字体。写入已有输出目录会替换这些文件，保留版本时请选择新目录。

## 4. 解读成品与设计选择

![空间锚图、局部视图、分子比较与控制组成的十四面板教学图](preview/spatial-multiomics-atlas.png)

空间大图是入口，同源 ROI 连接局部视图。高而窄的 donor × assay 矩阵与配对汇总并置，较宽的空间 profile 留出连续变化的阅读空间。后续面板包含 locus、细胞组成、invariant control、sign-flip null 和边界宽度敏感性。

面板面积随信息任务变化，不是每种图都占一格。空间位置和 assay 比较共用明确的对象对应关系，局部看起来漂亮不能替代整体叙事。

[legend.md](legend.md)解释各面板的变换、单位、尺度与 null。尤其注意：

- marker 矩阵按完整 cell-level feature 变化缩放，不能把 invariant control 的微小变化夸大；
- assay 变化用各自 control donor SD 标准化，共享颜色不表示可比较的分子浓度；
- 人工轨迹不应解读成真实基因组位置或机制证据。

## 5. 复现合成输入，或迁移到自己的项目

如需从生成器重新创建教学输入，仍写到前面新建的临时目录：

```bash
python3 -B "$SKILL_DIR/examples/spatial-multiomics-atlas/generate.py" \
  "$DEMO_OUT/synthetic-tables"
python3 -B "$SKILL_DIR/examples/spatial-multiomics-atlas/render.py" \
  --data "$DEMO_OUT/synthetic-tables" --output "$DEMO_OUT/regenerated-atlas"
```

换成真实研究时，先明确科学问题与独立样本，再调整字段映射、样本连接、显示变换、面板设计和图注。不要将真实数据硬塞进固定教学 donor 和特征约定；如果新研究存在缺失，应说明实际处理，而不是补造配对。

## 6. 文件与使用限制

PDF/SVG 的图形与 colourbar 保留为矢量，PNG 为 300-dpi 预览。脚本和数据是可编辑源；本例不提供 PPTX。修改 Python 场景后重跑即可改变排布，直接编辑导出 SVG 则不会反向更新脚本。

正文标注为 5–6.2 pt，面板字母与教学标题为 8 pt。Arial 可用时使用 Arial，否则报告 DejaVu Sans。这里的版面尺寸是教学选择，不代表任何期刊的通用投稿要求。

自动文字边界检查通过仍不排除图内重叠，需要实际打开成品，在目标插入尺寸核对文字、色条、面板标识与比较关系。

进一步看[原生可编辑模型图](../advanced-method-diagrams/README.md)、[18-panel 示例](../multimodal-18-panel/README.md)或[密集复合图设计](../../references/dense-compound-design.md)。
