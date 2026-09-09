# 教学输入：配对响应记录如何写进期刊稿

本案例为 AI-for-biology 响应预测研究的报告排练。
可以设想作者将来希望用细胞状态预测标本层面的响应，但本例没有模型、
细胞测量、真实标本或干预。下面的六行完全是手工构造值，不是预测性能或生物实验结果。

## 当前要回答的问题

不是“治疗是否有效”，而是：**怎样让正文、Methods、图注与数据说明准确表达同一组配对记录？**

[observations.csv](observations.csv) 每行一个构造标本，包含 baseline 与 follow_up 两个值。
两个值来自同一行的标本，不能把它们计为两个独立标本。

| specimen | baseline | follow_up |
|---|---|---|
| specimen-1 | 1.1 | 1.3 |
| specimen-2 | 1.5 | 1.4 |
| specimen-3 | 1.8 | 2.0 |
| specimen-4 | 2.0 | 2.1 |
| specimen-5 | 2.3 | 2.2 |
| specimen-6 | 2.5 | 2.8 |

所有数值为任意单位。四个标本 follow_up 较高，两个较低。
这里有六个构造标本、每个两个值；没有总体抽样或独立性证明，不计算 p 值、效应估计或区间。
图仅把 baseline 与 follow_up 作为一个点的横纵坐标，不拟合曲线、不画误差条。

## 作者提供的初稿问题

[before.md](before.md) 中的句子同时存在三个问题：

- 将十二个测量值写成十二个独立样本；
- 将四高两低的构造记录写成治疗改善和广泛泛化；
- 将随案例提供的 CSV 写成已公开存入外部仓库。

修订需要分别解决单位、解释和可用性，不是只替换一个更保守的形容词。
[after.md](after.md) 提供相互一致的 Results、Methods、Figure legend、Data availability 和 Limitations。

## 可交给 agent 的任务请求

```text
使用 $prepare-journal-manuscripts 完成一个 synthetic 配对记录教学修订。
读 case-brief.md、observations.csv、before.md 与 analysis-complete.json。
先指出样本单位、因果、泛化和数据存放的错误，再写英文 Results、Methods、
完整 Figure legend、Data Availability 和 Limitations。
保留六行全部数值与配对关系；不训练模型，不补 p 值、区间、伦理批件或 accession。
最后给出模拟编辑回复，明确哪些只是改了文字、哪些实验没有做。
```

这不是受控 agent 行为评测记录；提供的修订稿和回复是预先编写的示范输出。
让 agent 自己完成任务时，输出措辞可以不同，但不能改变输入事实和教学状态。

## 哪些检查真的可运行

图渲染器读取六行 CSV。统计 validator 检查报告字段；
缺少独立单位的记录应失败，完整记录应通过。数据 validator 检查清单字段。
它们不自动纠正文稿、不数原始标本、不判断真实因果设计，也不访问外部仓库。
脚本与输出位置见 [案例教程](README.md)。
