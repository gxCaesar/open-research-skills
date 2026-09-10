# 这些 skill 有没有用：我们自己测了两次，两次都打平

[仓库首页](../README.md) · [第一案](#case-1) · [第二案](#case-2) · [两案合看](#together) · [这不能说明什么](#limits)

大多数工具作者不会公开这样一份东西。我们公开，是因为**"用了会更好"是一个可以被检验的断言，
而我们检验的结果不支持它**。

## 怎么测的

两个案例，同一套设计：

- **同一份任务、同一份材料，两个互不知情的执行者。** 一个只拿到材料，一个额外拿到被测 skill。
  对照臂的零假设是**「不做 X」，不是「把 X 做错」** —— 它有全部机会把事情做对，只是没人告诉它要做。
- **端点在开跑之前冻结**，两个分支各自的可发表断言都先写下来。只有一个分支有东西可写的实验，
  会持续产生调判据的压力；两句话都写下之后，「调到通过为止」就没有落脚点。
- **跨模型家族的盲评**，评审只看到中性标签，映射存在它拿不到的地方。
- **平局是有效结论**，报成「在此规模下无法区分」，不报成「被测对象没问题」。

<a id="case-1"></a>

## 第一案：把一个研究项目打成发布包

材料是一个普通的、有点乱的工作目录：标定表在项目目录之外、一个环境变量未设时**不报错**
而是静默算出另一个数、脚本路径按当前工作目录解析。作者记录里写着 `effect = 0.6253`。

任务：打一个别人下载后能跑出这个数的包。

**主结局：两个包都做到了。** 从隔离副本、干净环境、只按各自写的命令：两边都跑出 `0.6253`，
**都不需要任何介入**。

盲评判核心平局，但在文档准确性上找出 4 条确认缺陷，**全部在没用 skill 的那一份**
（把某个数说成"未校正差值"而实际不是、声称某个常数唯一而同一个包后文自相矛盾、
README 说可从任意目录运行而实际不能、残留内部路径）。用了 skill 的那份**校验入口带真实比较分支**：
把常数改错，它 exit 1；另一份只是并排打印。

这一案有两个我们自己发现并写进报告的缺陷，都削弱它：

**端点是半循环的。** 那个常数在材料里从未记录，两臂都只能从目标值反解，所以"复现出被报告的数"
测的是"能不能打中一个照着调的靶"。盲评还证明反解不唯一：`0.84995` / `0.85` / `0.85001`
都打印同一个四位小数。

**两臂并发跑、共用工作区，交叉阅读排除不掉。** 对照臂的包有约 9 分钟对另一臂可读。
反向证据是实测的：两个包 8 个同名文件里**逐字节相同的只有 1 个**，而那一个是两边都原样拷贝的
源数据。这不能证明没有交叉阅读，只能说明所有可观测产物与独立工作一致。

这两条就是做第二案的理由。

<a id="case-2"></a>

## 第二案：这个方向的数据够不够

材料是五个数据集和一份目录说明。问题：**基线打分能不能预测扰动响应。**

陷阱是真实的：其中两个数据集**两列都有**，目录说明也写着"看起来是现成的"。
但逐样本共存计数是 **0** —— 一个是两个子研究按行拼接，一个是两侧样本编号命名空间不同。
**列层面与样本层面给出相反的答案。**

正确答案是一个可以被任何人重数的数：**7050 行里，同时带两个变量的样本 = 0**。

**主结局：两臂都对。** 都报出逐样本共存为 0，都没掉进"两列都有"的陷阱，
都没有把方向判死（都指出这死在"数据获取"层而不是"任务"层，并给出解封路径）。

跨家族盲评：**核心判断及其可检验依据平局。** 确认缺陷 6 条，**两边都有**
（没用 skill 的 3 条、用了的 2 条、1 条两份共有），评审明写「缺陷不按条数合成总分」。

<a id="together"></a>

## 两案合看

| | 第一案 | 第二案 |
|---|---|---|
| 主结局 | 平局 | 平局 |
| 端点 | 半循环（我们自己发现的缺陷） | 非循环，答案可被任何人重数 |
| 盲评 | 核心平局，4 条缺陷全在对照臂 | 核心平局，缺陷两边都有 |

**结论：在这两个任务上，一个有能力的通用 agent 不用这些 skill 也得到了同样正确的答案。**

skill 可归因的差异是**结构** —— 三个判词分开记录、击杀点名死在哪一层、报击杀前先跑一次
repair table。**但结构也会被填错**：第二案里，用了 skill 的那一臂照规定产出了 repair table，
而它那句「4/4 可翻案」被评审判为建立在一个未经证实的断言之上。

**可审计的形状本身也能装错东西，而且装错之后更难被发现，因为它看起来是合规的。**

<a id="limits"></a>

## 这不能说明什么

- **不能说明用了论文会更好。** 两案都只测一件具体的事，都没测稿件质量。
- **不能说明 skill 提升了判断准确性。** 两案主结局都是平局。
- **不能外推到「用 skill 的人 vs 不用的人」。** 两臂都是能力很强的通用 agent，
  在无人提示下自己找出了材料里的全部陷阱。这是明显更难的对照。
- **每案 n=1，材料是合成的。** 演示一个机制，不估计效应量。

## 顺带得到的三条方法学教训

它们对任何做类似检验的人都成立，与本仓库无关：

1. **阳性对照必须用被测材料的真实格式构造，否则它验的是自己。** 第二案的数据是 CRLF 行尾，
   裸 `awk -F,` 会把行尾字符当成最后一列的值，给出与真相**完全相反**的计数；
   而第一版对照 fixture 是 LF 写的，于是**对照通过而真实计数是错的**。
2. **测量工具会漏报，而漏报和"没问题"长得一样。** 第一案里我们的命令提取器两次过窄，
   一度得出"两个包都没能复现"这个事实上错误的答案。两次修正都对两臂同等生效，原始输出全部留档。
3. **盲评的隔离要靠构造证明，不能靠评审自述。** 第二案在盲化时发现一份交付里含有直接暴露
   身份的字面路径；处理办法是对两臂施加同一条改写规则并记录改写次数，而不是悄悄删掉。

---

## English summary

We ran two pre-registered before/after evaluations of these skills. **Both were ties on
every primary endpoint.** We are publishing them because "using this makes the work
better" is a checkable claim, and our check does not support it.

**Design, both cases.** Same task and same material given to two agents that could not
see each other. One got the material only; the other also got the skill under test. The
control arm's null is *not doing X*, never *doing X badly* — it had every chance to get
the task right, just nobody told it to. Endpoints were frozen before either arm ran, with
**both publishable statements written in advance**, so there was nowhere for "tune until
it passes" to stand. Review was blind and from a different model family, with the mapping
held outside the reviewer's input.

**Case 1 — packaging a project for release.** A messy working directory: a calibration
table outside the project, an environment variable that silently computes a different
number when unset, paths resolved from the current directory. Both packages reproduced the
reported figure from an isolated copy, in a clean environment, **with zero intervention**.
The blind reviewer called the core question a tie and then found four confirmed documentation
defects, all four in the arm without the skill. One structural difference held up when actually
run: the skill-built package's verification entry point has a real comparison branch and
exits 1 on a wrong constant; the other only prints values side by side. Two flaws in this
case are ours: the endpoint was semi-circular (the constant was never recorded, so both
arms back-solved it from the target), and the arms ran concurrently in a shared workspace,
so cross-reading cannot be excluded.

**Case 2 — is the data adequate for this direction.** Five datasets; the question is
whether a baseline score can predict a perturbation response. Two datasets carry **both
columns**, and the catalogue says so — but per-sample co-occurrence is **0**: one is two
sub-studies concatenated by row, the other has different sample-ID namespaces on the two
sides. Column level and sample level give opposite answers. The correct answer is a number
anyone can recount: **0 of 7050 rows carry both variables.** Both arms got it right, both
avoided the trap, both correctly killed the *data-source* layer rather than the task. Blind
review: core judgment a tie, six confirmed defects **split across both arms**, with the
reviewer noting explicitly that defects are not summed into a score.

**What the skills demonstrably add is structure** — separately recorded verdicts, a named
kill layer, a repair table run before reporting a kill. **And in case 2 that structure was
filled in wrongly**: the skill-guided arm produced the prescribed repair table, and its
"4 of 4 reversible" count rested on an assertion the reviewer found unverified. An
auditable shape can hold the wrong content, and is then harder to catch, because it looks
compliant.

**Limits.** These cases do not show that using the skills produces better papers — neither
tested manuscript quality. They do not show improved judgment; both primaries tied. They
do not generalise from agents to people: both arms were capable general agents that found
every planted trap unprompted, which is a much harder control than a human baseline. Each
case is n=1 on synthetic material — a mechanism demonstration, not an effect size.

**Three method lessons that hold for anyone running this kind of check.** A positive
control must be built in the real format of the material under test, or it only validates
itself: case 2's CSVs are CRLF, and a bare `awk -F,` returns counts that are the exact
opposite of the truth, while the first control fixture was written with LF and therefore
passed while the real count was wrong. A measurement instrument that under-reports looks
exactly like a clean result: our command extractor was too narrow twice in case 1 and once
produced a factually wrong answer; both widenings applied to both arms and every original
output is on record. And blinding must be proven by construction, not by the reviewer's
own account: case 2's blinding pass found a literal identifying path inside one
deliverable, fixed by applying one rewrite rule to both arms and recording the rewrite
counts, not by quietly deleting it.
