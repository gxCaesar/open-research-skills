# 研究示例：配对分析与进阶打包演练

先阅读或运行 [细胞扰动配对分析](perturbation-comparison/README.md)。它直接提供六行
synthetic 教学分数和标准库脚本，计算每个任务的候选减基线、正负平局次数与平均差，
再生成结果段落。源码和输入在同一目录，独立复制后仍可运行。

以下保留原有 `run_demo.py`，用于理解记录工具和打包流程。它是进阶冒烟测试，
不是配对分析的依赖，也不是完整研究任务的主要成果。

## 运行进阶示例

从仓库根目录运行；独立安装后把 `SKILL_DIR` 改成实际安装目录：

```bash
SKILL_DIR="$PWD/skills/research-publication-pipeline"
DEMO_OUT=$(mktemp -d)
python3 -B "$SKILL_DIR/examples/run_demo.py" "$DEMO_OUT/record-demo" --with-public-release
```

需要 Python 3.9+，只使用标准库。无需依赖安装、网络、API key、远端机器或 agent 账户。
这是 macOS/Linux shell 写法，其他系统可提供等价的新输出路径。
`record-demo` 必须尚不存在且位于 skill 之外。程序拒绝覆盖既有目录。
若只检查记录、不要算术打包演练，省略 `--with-public-release`。

## 预期输出与实际计算

带该参数运行时，终端应包含：

```text
pilot: PASS
development: PASS
handoff: PASS
public-release: PASS
```

不带参数时只打印前三项。两种形式都打印 synthetic 用途提醒与输出位置。
成功退出码为 0。记录中的科学分数是固定夹具，不是该程序估计出的结果。

| 相对输出路径 | 实际内容 |
|---|---|
| `START_HERE.md` | 生成工作区的导航 |
| `results/public-release-example.json` | 加参数后实际计算的 `{"count": 3, "total": 6}` |
| `public-release/README.md` | 打包后实际执行的两条命令 |
| `public-release/src/example.py` | 对 `[1, 2, 3]` 计数并求和的代码 |
| `public-release/tests/test_example.py` | 非空和空输入两个测试 |
| `results/final-comparison.json` | 合成标记，不是实测科研比较 |

可阅读原有 [算术结果到段落的解释](result-to-paragraph.md)，了解软件运行结果与
科研结论之间的区别。程序本身不编写或渲染论文。

## 打包演练做了什么

`--with-public-release` 在输出目录下建立一个十文件的算术源码树，打包后解压到新临时目录，
使用当前 Python 解释器执行例子和两个测试。它检查 JSON 是否与 `count=3`、`total=6`
一致，再运行本地发布记录检查。命令失败或结果不匹配会导致非零退出。

实际命令观察保存在生成工作区，而不是源码包内。临时压缩包与解压目录在演练后自动清理。
这不是新建依赖环境，不执行项目记录中任意提供的命令，也不向外部服务发布任何内容。

## 解释边界

这个 synthetic 演示生成的来源、状态、科学数值与不确定性区间只是软件夹具。
它没有训练基线或候选方法，没有真实数据读取、locked-test 访问、完整论文、
图形渲染或公开发布。出现区间字段不表示计算过该区间，检查通过也不是科研复现。

不要把生成工作区当成公开研究证据。若要学习一个实际分析源码包怎样独立交付，
使用前面的 `perturbation-comparison` 教程；若要做真实研究，补真实数据、来源与实验，
而不是改掉夹具标签。
