# README 配图与可编辑源文件

这组图用于展示科研绘图能力和十个 skill 的任务位置。先用 GPT 图像生成探索构图，再以可编辑的文字、自由曲线、形状和连线复刻；没有把生成图作为整页图片贴进 PPTX。图标和配色可以借鉴，科学内容须换成自己项目中有依据的内容。

## 下载 / Downloads

| 图件 / Figure | 可编辑源文件 | 矢量文件 | README 预览 |
|---|---|---|---|
| 空间机制示意 / Spatial mechanism | [PPTX](nature-spatial-mechanism-v2.pptx) | [PDF](nature-spatial-mechanism-v2.pdf) · [SVG](nature-spatial-mechanism-v2.svg) | [PNG](nature-spatial-mechanism-v2.png) |
| 条件化模型架构 / Conditioned architecture | [PPTX](conference-conditioning-architecture-v2.pptx) | [PDF](conference-conditioning-architecture-v2.pdf) · [SVG](conference-conditioning-architecture-v2.svg) | [PNG](conference-conditioning-architecture-v2.png) |
| 十项 skill 总览 / 中文 | [PPTX](skill-map-zh-v2.pptx) | [PDF](skill-map-zh-v2.pdf) · [SVG](skill-map-zh-v2.svg) | [浅色](skill-map-zh-v2.png) · [深色](skill-map-zh-v2-dark.png) |
| Ten-skill overview / English | [PPTX](skill-map-en-v2.pptx) | [PDF](skill-map-en-v2.pdf) · [SVG](skill-map-en-v2.svg) | [Light](skill-map-en-v2.png) · [Dark](skill-map-en-v2-dark.png) |

每份 PPTX 是一页独立画布，比例为 8:5。PNG 为 2400 × 1500 的导出预览；PDF 保留矢量对象并嵌入所用字体，SVG 保留矢量形状和文字。总览图另有[中文深色 SVG](skill-map-zh-v2-dark.svg) 和 [English dark SVG](skill-map-en-v2-dark.svg)。深色预览与浅色 PPTX 的内容和布局相同，仅改变配色。

## 打开后怎么学

1. 另存一份 PPTX，再尝试修改标签。文字是独立文本框，细胞和图标由原生形状及自由曲线组成，矩阵中的每一格都能改色。
2. 打开 PowerPoint 的“选择窗格”，或在 LibreOffice Impress 中逐个选择对象。先移动文字或单个模块；移动一个完整图标时，可框选组成它的形状后组合。
3. 修改连线路径时，连同端点一起选择。部分折线路径由多段线和小型不可见端点组成，不是会随任意模块自动重排的布局系统。
4. 先用“形状填充”“形状轮廓”和“编辑顶点”做一个小改动，再导出 PDF 或 PNG，对照原图检查文字是否被裁切、箭头是否仍指向正确对象。

英文图使用 Arial。中文总览使用 **苹方-简（PingFang SC）**，PPTX 不附带字体文件。没有该字体的设备可先用 PowerPoint 的“替换字体”换成已安装的中文无衬线字体，例如 Microsoft YaHei，再检查文字宽度。直接查看 PNG 或 PDF 不需要安装这些字体。

## 可以借鉴的设计

- 用蓝色表示基线状态，绿色表示响应，紫色表示上下文，金色表示扰动；颜色辅助区分，文字仍明确写出含义。
- 机制图从组织区域进入细胞组学，再连接预测模型和供体层面的比较单位，避免把所有内容挤成一条长流程。
- 架构图把条件输入、预测路径和仅训练时使用的观测响应分开；虚线的含义由附近标签说明。
- 总览图用任务图标建立视觉位置，区分“冷审自己的论文”和“受邀审稿”。工作流与科研绘图跨越多个阶段；箭头不是强制安装或执行顺序。

## 示例边界

细胞形态、矩阵颜色、token 数量和供体编号都是示意，不是实验测量、模型维度或真实注意力权重。架构只是教学例子，不能作为已验证方法引用。沿用版式时，不应把“观测响应仅用于训练”等关系直接套到没有相同定义的项目上。

构图探索中的无依据组织细节和装饰文字未保留。此处交付的是内容核对后的原生复刻，不是生成图的逐像素描摹。原有[机制与架构图教程](../../skills/build-scientific-visualizations/examples/advanced-method-diagrams/README.md)仍可用于对照学习。

## Editing notes in English

Each PPTX contains one native, editable 8:5 slide, not a flattened image. Text, cell outlines, tiles and connectors can be selected individually. Group the parts of an icon before moving it; segmented connectors include small invisible endpoint objects and do not automatically follow arbitrary modules.

The English figures use Arial. The Chinese overview uses PingFang SC under its Chinese family name, 苹方-简. Fonts are not bundled in the slides. Replace unavailable fonts with an installed equivalent and recheck text widths; PNG previews and the font-embedded PDFs can be viewed without those fonts installed.

The scientific figures are teaching schematics. Cell geometry, tile shading, donor IDs and token counts are illustrative. Reuse the visual structure only after replacing the content and relationships with those supported by your own project.
