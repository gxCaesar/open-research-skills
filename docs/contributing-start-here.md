# 从哪开始贡献

这个仓库不缺测试，缺的是**用它做过真事的人**告诉我们它在哪里不成立。

下面按「代价 → 价值」排序。第一条只要十分钟，而且是目前最有用的一条。

## 1. 用一次，把不成立的地方开成 issue（十分钟，最有价值）

装上，挑一个 skill，用您**真实的**材料跑一遍：

```bash
claude plugin marketplace add gxCaesar/open-research-skills
claude plugin install open-research-skills@open-research-skills
# Codex / Antigravity CLI：
git clone https://github.com/gxCaesar/open-research-skills.git
cd open-research-skills && bash scripts/install_skills.sh "$HOME/.agents/skills"
```

然后开一个 issue，只写三件事：

- **您想交付什么**（一张图 / 一段 Results / 一次撞车判断）
- **它给了您什么**
- **差在哪**

**"它对我的场景没用"是一条完整的 issue。** 不需要您给出修法。
我们最缺的正是这种——已有的 452 个测试证明校验器在工作，它们证明不了这些 skill 对您有用。

## 2. 报一个「检查其实没在检查」的缺陷（最欢迎）

这个仓库最在意的失效形状是：**某个检查报了零，是因为它没看，而不是因为没问题。**

已经抓到过好几个：一条测试因为维护者机器上装了 Poppler 而一直通过；匿名发布检查在任意层级
排除版本控制目录、却只查根目录，所以含作者邮箱的 `src/.git/config` 跑出 `failures=0`；
一条裁决满足了五条不同的评审发现。

如果您发现某个 checker 承诺的和它实际做的不一致，**那是这里最受欢迎的 issue**，
即使您只给出一句话和一个 `file:line`。

## 3. 提 PR

先跑本地三条（CI 会在干净机器上重跑一遍，Python 3.9 与 3.13）：

```bash
python3 -B scripts/run_tests.py            # 452 个测试
python3 scripts/check_public_content.py .  # 机器路径、私有账号名、内部控制文件
python3 scripts/check_rule_coverage.py     # 每条规则都有能让它开火的变异见证
```

**改了校验器就要配一条见证**，而且要**镜像**：放宽一条规则时，必须同时证明不合法的那一版仍然失败。
一个对什么都开火的检查等于没有检查。见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

**见证要放在检查器原先瞎掉的地方，不是它一直看得见的地方。** 例如版本控制那条见证现在建的是
嵌套目录而不是根目录，因为根目录是它从来没漏过的地方。

## 4. 加一个 venue 适配器

会议与期刊适配器都是**有日期的快照**，每条规则都记着来源。加一个新 venue，或更新一个过期的，
是范围清楚、容易验收的贡献。**查不到的规则要写成"未确立"，不要从兄弟会议继承一个看起来合理的。**

## 我们不需要的

- 泛泛的最佳实践重构
- 再加测试（[两次预注册评测都是平局](evidence.md)，这条轴上没有可测回报）
- 为没发生过的失败加闸门

## 语言

issue 和 PR **中文英文都可以**。十份手册目前是中文的，`README.en.md` 是英文入口。
