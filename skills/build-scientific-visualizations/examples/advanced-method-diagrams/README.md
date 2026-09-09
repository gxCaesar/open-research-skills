# 方法图案例：科学内容 → 可编辑的模型与机制图

两张原创教学图演示两种构图：模型总览与计算模块展开，以及空间对象与采样层级。每张均提供一页原生 PPTX、SVG、PDF 与 PNG，文字、形状、科学对象和连线可分别编辑，PPTX 未嵌入整张位图。

[输入：方法与图件 brief](method-brief.md) · [默认制作路线](../../references/image-concept-to-vector.md)

这是一个完整的资产复用与 authoring 教程，不是架构生成器。下面的命令只复制既有资产；新图需要 agent 与可用的图像/演示文稿制作能力。

## 1. 阅读输入，明确图要解释什么

先读 [method-brief.md](method-brief.md)。它区分三个输入、状态更新、训练监督与推理边界，也解释空间机制图中的 donor 配对。

两个示意图都是虚构设计，组织轮廓、矩阵颜色、token 数和 donor 标识不是测量。请勿据此推断 tensor 尺寸、attention 权重、真实样本数或方法效果。

## 2. 给 agent 一个有边界的制作任务

```text
使用 build-scientific-visualizations。
根据 method-brief.md 制作 conference 风格模型图：
上方展示输入到输出，下方展开交互模块，再单独说明训练与推理。
参考优秀示例的阅读顺序与留白，用默认概念稿到原生 PPTX 路线。
保持输入、条件和监督关系，不补造未定义的维度或性能。
交付可单独修改文字、形状与连线的 PPTX，另附 PDF/SVG 和图注。
```

默认路线是：核对科学内容 → 参考优秀构图 → GPT Image 2.5 概念稿 → 校正内容并重建原生 PPTX → 保存、重开与检查导出。已批准的图只需局部修改时直接改源文件，不需要重新生成概念稿。详见[制作路线及例外](../../references/image-concept-to-vector.md)。

## 3. 成品 A：模型总览与交互模块展开

![条件输入、两级状态更新、模块计算与训练推理边界](conference-conditioning-architecture.png)

[原生 PPTX](conference-conditioning-architecture.pptx) · [矢量 PDF](conference-conditioning-architecture.pdf) · [SVG](conference-conditioning-architecture.svg)

主面板区分 baseline state、perturbation 和 context。两组条件同时进入两个交互模块；细节面板展开 state query、共同 condition keys/values、attention、两次残差相加和 feed-forward 路径。Observed response 只进入训练 loss，不作为推理输入。

总览、局部运算和使用边界分开表达，读者不必在同一条长路径上寻找所有信息。实线、虚线与标签共同解释路由，不能仅凭颜色判断箭头。

## 4. 成品 B：空间机制与采样层级

![空间对象、匹配分子层和 donor 配对比较](nature-spatial-mechanism.png)

[原生 PPTX](nature-spatial-mechanism.pptx) · [矢量 PDF](nature-spatial-mechanism.pdf) · [SVG](nature-spatial-mechanism.svg)

上方从组织区域进入细胞与配对分子层，再连到 donor 内条件匹配。下方将条件化响应模型与独立比较单位分开。开放留白和生物轮廓承载科学对象，不将所有层级都画成一样的方框。

图 c 说明 cells 嵌套在 donor 内，比较使用 donor 层级汇总。图中没有可供检验的效果值或置信区间。

## 5. 在副本中练习编辑

从克隆仓库根目录执行；单独安装时将 `SKILL_DIR` 改为含 `SKILL.md` 的目录：

```bash
SKILL_DIR="$PWD/skills/build-scientific-visualizations"
DEMO_OUT=$(mktemp -d)
cp "$SKILL_DIR/examples/advanced-method-diagrams/conference-conditioning-architecture.pptx" \
  "$DEMO_OUT/conference-architecture-edit.pptx"
cp "$SKILL_DIR/examples/advanced-method-diagrams/nature-spatial-mechanism.pptx" \
  "$DEMO_OUT/nature-mechanism-edit.pptx"
```

用兼容编辑器打开副本：

1. 选中一个标签，将其替换为适合你研究的名称；不要把整个页面当图片编辑。
2. 移动一个模块，检查其进入和离开的全部连接。部分长路径由独立线段组成，可能需要分别调整，不承诺自动路由。
3. 对照 brief 检查科学关系，尤其是 condition 与 training-only 路径。
4. 保存并重新打开，再导出 PDF，在论文实际插入宽度检查阅读效果。

如果你的真实方法改变了运算或采样单位，需要重组对象与连接，不能只换标签。修改 PPTX 不会同步更新此目录已有的 PDF/SVG/PNG，交付前应重新导出。

## 6. 交付边界与后续

两张画布均宽 183 mm，使用 Arial，面板字母约为 8 pt；这些是设计示例，不是官方模板。具体期刊或会议的尺寸与图像政策需要另查当前要求。

概念参考由 AI 生成，随后重建为原生对象。当时工具没有返回后端模型身份，因此本例不认证某个 GPT Image 版本。已有原生文件的导出、保存重开和实际渲染检查记录；Microsoft PowerPoint GUI 编辑兼容性和期刊对 AI 辅助图的许可没有在此得到验证。矢量重绘不免除政策及披露要求。

想运行一个真正的数据到图件示例，使用[空间多组学 atlas](../spatial-multiomics-atlas/README.md)。想选择其他视觉方向，查看[两种风格与六套配色](../../references/diagram-style-profiles.md)。
