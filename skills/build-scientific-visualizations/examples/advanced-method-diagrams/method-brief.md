# 教学方法 brief：条件化细胞响应与空间采样关系

本文件定义本目录两张示意图的科学内容，便于读者理解和复用。它是虚构的制图输入，不是论文方法、代码实现或已验证机制。两张图共享部分概念，但没有共同实验队列，也不对应仓库其他案例的结果表。

## 模型图要回答的问题

给定 baseline cell profile、perturbation 和 context，如何更新状态并得到 predicted profile？观测响应在哪个阶段被使用？

| 对象 | 本教学设计中的定义 |
|---|---|
| Baseline cell profile | 推理时可用的基线状态；cell encoder 产生 state tokens |
| Perturbation | 已知扰动条件，经独立 encoder 表示 |
| Context | 已知背景条件，经独立 encoder 表示 |
| Interaction blocks | 示例画两级状态更新，两级都接收 perturbation 与 context 条件 |
| Expanded interaction | state 提供 query，组合条件提供 keys/values；attention 与 feed-forward 各有残差相加 |
| Decoder | 将更新后状态映射为 predicted profile |
| Observed response | 仅训练阶段为 reconstruction loss 提供参照，不作为推理输入 |

层数、token 数、矩阵大小和色深只说明示意布局；除图中明确给定的两级示范块之外，不据此填写真实实现的超参数。没有指定损失的数学形式，也没有实测预测效果。

希望的图件分工：a 展示总览，b 展开一个交互块，c 对比训练与推理输入。箭头需要区分运算、条件连接、预测、监督与局部展开指引。

## 空间机制图要回答的问题

怎样从组织区域关联到分子层，并保持 donor 内匹配和 donor 层级的比较？

组织与 ROI 提供空间背景；细胞中的 RNA/chromatin 图形帮助解释两种分子层。匹配关系使用相同 donor ID，control 与 stimulated 先在 donor 内匹配，再做 donor 层级汇总。Cells 嵌套于 donor，细胞点不自动成为独立生物重复。

图中区域、分子矩阵、donor 标识与细胞数量均为示意。它不保证真实数据具备这种配对；真实项目需要核对数据本身能否建立对应关系。

希望的图件分工：a 说明空间对象与配对分子层，b 说明条件化预测任务，c 说明比较单位。预测轮廓不是观察数据；采样层级图不添加虚构效果值。

## 交付与修改要求

文字、对象和连线在 PPTX 中独立可编辑，另附矢量导出与简洁 legend。改名不能改变对象身份；移动模块后重新检查连接。若实际方法或数据条件不同，先改 brief 中的定义，再改图。

[返回完整案例与成品](README.md)
