# 教学示范：给编辑的说明与修订回复

这是 synthetic 教学案例的示范写作示例，意见与回复均为虚构。
它没有真实期刊、编辑、投稿或作者声明；不得直接作为投稿信发送。
修订正文见 [after.md](after.md)，输入边界见 [case-brief.md](case-brief.md)。

## Cover-note excerpt

We provide a teaching example of consistent reporting for paired observations.
The accompanying excerpt aligns Results, Methods, the figure legend and the data
statement with six manually constructed specimen pairs. It makes no claim of a
treatment effect, population generalization or predictive performance.
The source table is supplied with the example, and the display includes every row.
The purpose is to show how the unit of reporting and the scope of interpretation
can remain consistent across a manuscript and its supporting material.

这个片段演示如何用事实说明稿件内容，不宣称适合某个期刊。
真实 cover letter 还需实际期刊与文章类型、已确认的贡献与读者关联、相关稿件等事实；
不能从本例补出“全体作者同意”“未在别处投稿”或伦理、资助声明。

## Editorial comment 1：独立样本数不清

> Please clarify whether the two measurements from each specimen were counted as
> independent samples, and reconcile the sample count throughout the manuscript.

**Response.** We have corrected the reporting unit. The table contains six constructed
specimens, each with a baseline and a follow-up value, not twelve independent specimens.
The revised Methods define one CSV row as one specimen, and the legend states
“n = 6 specimens, two measurements per specimen.” All six rows remain included.

**修改位置：** [after.md](after.md) 的 Results、Methods 与 Figure legend。
**完成状态：** 单位表述已修订；未增加样本或重新解释原值为真实标本。

## Editorial comment 2：因果解释超过设计

> The claim that treatment improves response and generalizes to a wider population
> requires evidence beyond the observations shown.

**Response.** The claim was unsupported and has been removed. No treatment was
administered and no population was sampled in this teaching example. The Results now
state that follow-up exceeds baseline for four constructed specimens and is lower for
two. The Limitations make clear that the values provide neither causal nor
generalization evidence. No new intervention study or inferential analysis was performed.

**修改位置：** [after.md](after.md) 的 Results 与 Limitations。
**完成状态：** 解释已收窄；没有新生物实验、假设检验或独立验证。

## Editorial comment 3：数据在哪里？

> Please identify the available source data rather than referring to an unspecified deposit.

**Response.** We have replaced the deposit claim with the actual access route.
The six-row synthetic table is supplied as `observations.csv` alongside this example.
No external repository accession or public deposit is claimed.

**修改位置：** [after.md](after.md) 的 Data availability；
[data-inventory.json](data-inventory.json) 指向同一文件。
**完成状态：** 已纠正数据说明；没有创建外部存储或验证外部访问。

## 作者交付前还应核对什么

真实返修应逐条关联完整意见与实际修改，并对照最后提交版本。
这里的 reviewer 文本只用于学习回应方式，不应混入真实评审记录。
本例未渲染完整稿件、制作 tracked-change 文档或发送任何材料；
“文字示范已提供”不等于“完成期刊返修提交”。
