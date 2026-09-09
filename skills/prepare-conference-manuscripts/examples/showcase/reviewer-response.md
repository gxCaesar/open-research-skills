# 教学示范：模拟审稿回复

所有 reviewer comments 和回复均为这个 synthetic 案例虚构的练习材料，
不是私人审稿意见或真实投稿记录。下面已经“修改”的内容指随案例提供的教学文本；
没有新增实验。输入见 [case-brief.md](case-brief.md)。

## Comment 1：平均数是否掩盖了失败任务？

> The statement that the candidate consistently outperforms the baseline is not
> supported by all task-level values. Please report the unsuccessful comparisons.

**Response.** The original statement was too broad. We have replaced it with:
“In six illustrative tasks, the candidate score is higher on four tasks and lower
on two. The mean paired difference is 0.005 arbitrary score units.”
The revised Results also retain the negative differences for task-3 and task-6.
All six constructed pairs are shown in the figure; no task has been removed.

**对应修改：** [after.tex](after.tex) 的 Results；
[完整片段](manuscript-example.md) 的 Results 与 Figure legend。
**状态：** 教学文字已修改；没有新实验，也没有新的显著性结果。

## Comment 2：这些结果支持未见扰动上的泛化吗？

> Does the comparison demonstrate generalization to unseen perturbations or donors?

**Response.** No. The values are manually constructed and no predictor was trained.
They do not come from held-out perturbations or donors. We have stated this explicitly
in the Limitations and removed the implication of biological generalization.
A real evaluation would require an appropriate held-out design and observed results;
that work has not been performed in this example.

**对应修改：** [完整片段](manuscript-example.md) 的 Abstract、Method explanation excerpt 和 Limitations。
**状态：** 已收窄解释；泛化验证未运行。

## Comment 3：扰动描述确实带来了收益吗？

> Please provide an ablation showing that the perturbation descriptor explains the gain.

**Response.** This example does not establish a gain attributable to the descriptor.
The descriptor-bearing and state-only predictors are a conceptual contrast, not two
implemented systems. We now distinguish that proposed comparison from the constructed
score table. No ablation has been run, and we do not use these scores as mechanism
evidence.

**对应修改：** [完整片段](manuscript-example.md) 的 Method explanation excerpt 和 Limitations。
**状态：** 方法解释已澄清；没有把消融计划写成完成。

## 如何迁移到真实 rebuttal

保留“具体关切 → 证据 → 实际改动位置 → 未完成事项”的关联即可，不要复制虚构事实。
如果新分析确实已运行，应引用实际结果与修改位置；若未运行，不能用上述回复格式制造完成状态。
