# 教学示范：从方法简述到可读论文片段

以下是为这个案例编写的教学输出，不是脚本生成、真实投稿文本或实际模型研究。
英文段落保留教学限定；中文说明解释写作取舍。
输入见 [case-brief.md](case-brief.md)，数值见 [scores.csv](scores.csv)。

## 文章提纲

| 部分 | 段落要完成的工作 | 可用材料 / 未完成材料 |
|---|---|---|
| Introduction | 说明为什么要考察扰动信息与逐任务差异 | 概念问题；没有经过文献验证的新颖性结论 |
| Method | 解释状态表示、扰动描述和响应输出的关系 | 方法简述；实现与训练配方缺失 |
| Evaluation | 说明匹配比较应如何支撑问题 | 目前只有构造得分；真实协议与实验未运行 |
| Results | 保留六个任务的方向差异，避免平均数掩盖失败 | 六行 CSV，可直接逐行检查 |
| Limitations | 说明什么不能由这张表推出 | 无训练、无抽样模型、无机制或泛化验证 |

这不是适用于所有论文的强制章节顺序。此处把未完成方法与已有教学表分开，
是为了防止读者把漂亮的方法解释误当成运行证据。

## Abstract

Predicting cellular responses to perturbation motivates models that relate an initial
cell state to a specified intervention. Explaining such a model also requires showing
where its comparisons improve and where they do not. This teaching example outlines a
candidate predictor that would use both a baseline state representation and a perturbation
descriptor, alongside a baseline that would omit the descriptor. Neither model is
implemented or trained here. Instead, six manually constructed task-score pairs illustrate
how to report heterogeneous comparisons. The candidate score is higher on four tasks
and lower on two, with a mean paired difference of 0.005 arbitrary score units.
The example connects a method brief to scoped results, an observation plot and explicit
limitations without turning the proposed computation into an empirical finding.
These values support a reporting exercise, not a claim of predictive effectiveness,
mechanism identification or generalization to biological systems.

## Method explanation excerpt

The proposed comparison asks what changes when a response predictor has access to a
perturbation descriptor in addition to a baseline cell-state representation. The
descriptor-bearing candidate and the state-only baseline define the conceptual contrast.
A real evaluation would need to hold the relevant data, split, tuning and scoring
conditions comparable. No such implementation or evaluation is supplied in this
teaching fixture, and the constructed task scores are not outputs of these predictors.

这一段先解释对象、改变的计算输入与比较关系，而不列虚构模块名或超参数。
“would” 与 “proposed” 是方法状态的限定，不应为了显得果断而删掉。

## Results

In six illustrative tasks, the candidate score is higher on four tasks and lower on two.
The paired differences are 0.02, 0.01, -0.01, 0.02, 0.01 and -0.02 in task order,
giving a mean paired difference of 0.005 arbitrary score units.
The scatter plot displays every task using its baseline and candidate values.
The positive mean does not imply a uniform advantage: task-3 and task-6 retain
negative differences. Because the scores were constructed for this example, they do
not measure the proposed predictor's performance.

## Figure legend

**Constructed task-score comparison.** Each point corresponds to one row of
`scores.csv`. The horizontal and vertical axes show baseline and candidate scores,
respectively, in arbitrary units. All six tasks are displayed. No fitted line, error
bar, statistical test or sampling uncertainty is shown. The points are teaching
values, not predictions from a trained cellular-response model.

## Limitations

The example has no trained model, biological dataset, sampling model or uncertainty
estimate. The task labels do not identify independently sampled biological units.
The constructed score differences therefore cannot establish statistical significance,
the effect of conditioning on perturbation information, or generalization to unseen
perturbations, donors or experimental settings. Those questions remain untested.
The present contribution is an example of evidence-bounded writing, not a method result.

## 修改前后与修改原因

| 修改前 | 修改后 | 原因 |
|---|---|---|
| “consistently outperforms ... across all tasks” | “higher on four tasks and lower on two” | 全部六行中存在两个负差 |
| 方法设想被叙述成已经验证的机制 | 明确 proposed comparison，未实现、未训练 | CSV 与设想模型没有实验生产关系 |
| 用平均数暗示可靠泛化 | 保留 0.005，说明无抽样模型与独立验证 | 数值描述不等于总体推断 |

[after.tex](after.tex) 仍是用于源检查的短修正版，不包含上面的全部教学段落。
脚本不会生成本文件；两者用途不同。模拟回复见 [reviewer-response.md](reviewer-response.md)。
