---
name: career-ops-copilot
description: 'Job search assistant: evaluate JDs with 10-dimension scoring, manage tracker.csv, tailor resumes, structure STAR interview stories, and fetch JD from web pages. Triggers: 评估JD, 看岗位, job evaluation, 加入tracker, 定制简历, tailored resume, STAR, 面试故事, interview story, 求职, job search, evaluate position, 保存JD'
argument-hint: 'Paste JD text or URL, or ask for resume tailoring / interview prep'
user-invocable: true
disable-model-invocation: false
---

# Career Optimization Copilot

求职全流程助手：JD评估 → Tracker管理 → 简历定制 → 面试准备。

Auto-switch response language based on user input language.

## Multi-user & Workspace

所有用户数据存放在 `users/<username>/` 下（整个 `users/` 目录被 gitignore，个人数据不会上传）。

### 目录结构

```
career-ops-copilot/
├── SKILL.md                          # 本文件（工作流定义）
├── README.md                         # 项目说明
├── .gitignore                        # 排除 users/ 个人数据
├── references/                       # 公开参考资料
│   └── spa-scraping-notes.md
├── util/                             # 工具脚本（可公开）
│   └── fetch_jd.py
└── users/                            # 所有用户数据（gitignored）
    └── <username>/                   # 每个用户独立工作区
        ├── profile.md                # 求职偏好（核心目标、目标维度）
        ├── resume/
        │   ├── cv_cn.md              # 母版中文简历（素材库，可迭代补充）
        │   └── cv_en.md              # 母版英文简历（素材库，可迭代补充）
        ├── tracker.csv               # 职位追踪表 (single source of truth)
        ├── interview_stories.md      # 通用STAR素材库
        ├── self_introduction.md      # 自我介绍（可选）
        └── jobs/                     # 每个目标职位一个子目录
            └── {company}_{role}/
                ├── eval.md           # 评估报告 + JD原文
                ├── timeline.md       # 状态变迁时间线
                ├── cv_cn.md          # 定制中文简历（按需）
                ├── cv_en.md          # 定制英文简历（按需）
                └── interview_prep.md # 面试准备（按需）
```

### 路径约定

以下用 `<USER>` 表示当前用户目录 `users/<username>/`：

| 用途 | 路径 |
|------|------|
| 求职偏好 | `<USER>/profile.md` |
| 母版简历 | `<USER>/resume/cv_cn.md` / `cv_en.md`（素材库，可迭代补充） |
| 追踪表 | `<USER>/tracker.csv` |
| STAR素材 | `<USER>/interview_stories.md` |
| 职位目录 | `<USER>/jobs/{company}_{role}/` |

### 用户识别

1. 列出 `users/` 下的子目录。
2. 如果**只有一个**用户目录 → 自动选中。
3. 如果有**多个** → 通过 `vscode_askQuestions` 让用户选择。
4. 如果 `users/` **为空或不存在** → 触发 Workflow 0 初始化。

## Workflow 0: 初始化用户工作区

新用户首次使用时，或用户主动说"初始化"时触发。

### Steps

1. 通过 `vscode_askQuestions` 询问用户名（建议用英文，如 `JackyTao`）
2. 创建 `users/<username>/` 及子目录 `resume/`、`jobs/`
3. 创建空文件：`tracker.csv`（含表头）、`interview_stories.md`（含标题）
4. **构建母版简历** — 询问用户是否有现成简历：
   - **有简历** → 用户粘贴文本或提供文件路径 → 读取后按「四大板块」结构重组为母版简历，保存到 `resume/cv_cn.md` / `cv_en.md`
   - **无简历** → 创建含模板骨架的 `resume/cv_cn.md`（见下方模板），引导用户逐步填写各板块
5. **采集求职偏好** — 通过 `vscode_askQuestions` 引导用户从以下 6 个维度中选择 **2 个核心目标**，并记录到 `<USER>/profile.md`：
   - 薪资 / 岗位层级 / 行业 / 城市 / 稳定性 / 成长空间
   - 可附带简短说明（如"涨薪30%+"、"一线城市"）
6. 完成后确认工作区就绪

### 母版简历四大板块模板

母版简历是**素材库**，不是直接投递用的简历。每次定制简历时从中裁剪。

```markdown
# [姓名] — 母版简历

## 一、个人总结
<!-- 不是技能罗列，而是能力主张——用一句话概括你能为雇主做什么 -->
- 将复杂的业务需求转化为可落地的产品设计
- 用数据驱动决策，从海量运营数据中提炼可执行洞察
- 主导跨职能团队从0到1交付自动化/数字化项目
- ...（3~6条，每条是"动词+对象+价值"结构）

## 二、基础经历
<!-- 每段工作经历：公司、岗位、时间、职责范围 -->

### [公司A] | [岗位] | [起止时间]
- 职责范围概述...

## 三、项目案例 & 个人故事

### A. 项目案例
<!-- 适合写在提交版简历里，重在完整展示项目全貌、突出JD所需的能力和经验 -->
<!-- 按 STAR 结构：Situation → Task → Action → Result（Result务必量化） -->

#### 项目1：[项目名称]
- **S**: 背景/痛点...
- **T**: 目标...
- **A**: 关键行动...
- **R**: 量化结果...

### B. 个人故事
<!-- 适合面试准备，应对结构化提问（如宝洁八大问） -->
<!-- 可以是某个项目中的一件事，也可以是一个完整项目，重在体现个人能力/品质 -->
<!-- 同样用 STAR 结构，但侧重个人角色和决策过程 -->

#### 故事1：[简短标题]（对应维度：[如"说服他人"]）
- **S**: 当时的情境...
- **T**: 我需要解决的问题...
- **A**: 我具体做了什么（强调个人决策和行动）...
- **R**: 最终结果和收获...

## 四、作品与成果
<!-- 个人可展示的作品、链接、证明材料 -->
- GitHub: [链接]
- 个人网站/博客: [链接]
- 开源项目: [项目名] - [链接] - [简述]
- 论文: [标题], [期刊], [年份], [DOI链接]
- 其他: 专利、获奖证书、演讲视频等
```

### profile.md 格式

```markdown
# 求职偏好

## 核心目标（2个）
1. [维度]: [具体说明]
2. [维度]: [具体说明]

## 补充信息
- 目标城市: ...
- 可接受薪资范围: ...
- 其他偏好: ...
```

### tracker.csv 表头
```
id,company,role,url,score,status,last_updated,notes
```

- `status`: 记录当前最新状态（见下方状态值）
- `last_updated`: 最近一次状态变更的日期 (YYYY-MM-DD)

### Status 值

| 状态 | 含义 |
|------|------|
| `evaluating` | 评估中，尚未投递 |
| `applied` | 已投递 |
| `interviewing` | 面试中（具体轮次见 timeline.md） |
| `offer` | 已收到offer |
| `rejected` | 被拒 |
| `withdrawn` | 主动放弃 |

> 面试的具体轮次、名称（HR面/业务面/群面/终面等）和细节全部记录在 timeline.md 中，tracker.csv 只用 `interviewing` 表示"正在面试流程中"。

### timeline.md 格式

每个职位目录下的 `timeline.md` 记录完整状态变迁历史：

```markdown
# Timeline: [公司] [职位]

| 日期 | 事件 | 备注 |
|------|------|------|
| 2026-06-20 | 评估 | 综合分4.2 |
| 2026-06-21 | 投递 | 通过官网投递 |
| 2026-06-25 | 面试-第1轮 | HR电话面，聊了30min，问了离职原因 |
| 2026-06-28 | 面试-第2轮 | 业务主管面，技术问题为主 |
| 2026-07-02 | 面试-第3轮 | VP终面，聊职业规划 |
| 2026-07-05 | offer | 薪资package确认 |
```

### 命名规范
- 用户目录名：英文，如 `JackyTao`、`AliceWang`
- 职位子目录：`{company}_{role}`，小写英文，空格用下划线

## Workflow 0.5: 母版简历迭代补充

用户随时可通过对话补充母版简历内容。触发词：“添加项目”“补充成果”“更新简历”“新增经历”“添加故事”“STAR”。

### Rules

1. 读取当前 `<USER>/resume/cv_cn.md`，理解现有结构
2. 将用户提供的新内容按四大板块归类，追加到对应位置：
   - 新能力主张 → “一、个人总结”
   - 新工作经历 → “二、基础经历”
   - 新项目案例 → “三 → A. 项目案例”（按 STAR 结构）
   - 新个人故事 → “三 → B. 个人故事”（按 STAR 结构，标注对应面试维度）
   - 新作品/链接 → “四、作品与成果”
3. 如用户提供的描述不够结构化，主动追问补充（特别是结果/数字）
4. 同步更新 `cv_en.md`（如用户同时维护英文版）
5. 修改后向用户确认变更内容

### STAR 结构化流程

当用户描述一段经历时（可能不完整）：

1. 按 Situation → Task → Action → Result 结构化
2. 识别不足（缺数字、缺结果、逻辑不清），提问补充
3. 用户补充后，输出完整 STAR 版本
4. **链接面试维度** — 建议该故事可用于哪些结构化问题（见下方维度参考）
5. 归入母版简历“三 → B. 个人故事”部分

### 结构化提问维度参考（宝洁八大问 + 通用）
- 领导力/带团队达成目标
- 分析复杂问题
- 创新解决问题
- 说服他人/影响决策
- 面对挫折/逆转
- 跨文化/跨团队协作
- 资源受限下交付
- 诚信/道德困境

---

## Workflow 1: JD评估

### Input
用户提供：JD文本（粘贴） 或 URL。

### Steps

1. **解析JD** — 如果是URL，先尝试 `fetch_webpage` 抓取。如果失败（SPA页面），告知用户粘贴文本。已知 Boss直聘 无法抓取（CDP检测），参见 [references/spa-scraping-notes.md](references/spa-scraping-notes.md)。
2. **读取简历与偏好** — 读取 `<USER>/resume/cv_cn.md`、`cv_en.md` 和 `<USER>/profile.md`，了解用户背景和求职核心目标。
3. **10维度评分** — 输出标准表格：

| 维度 | 分数 | 说明 |
|------|------|------|
| 角色匹配 | x.x | JD核心职责与经验重合度 |
| 技能覆盖 | x.x | 必备技能覆盖率 |
| 经验年限 | x.x | 年限匹配度 |
| 行业契合 | x.x | 行业背景加分 |
| 成长空间 | x.x | 对职业发展帮助 |
| 薪资预估 | x.x | 与预期匹配度 |
| 公司规模 | x.x | 体量与稳定性 |
| 地理位置 | x.x | 通勤/搬迁接受度 |
| 文化契合 | x.x | 工作风格 |
| 竞争难度 | x.x | 预估竞争激烈程度 |

4. **综合评分** — 加权平均，附一句话建议（≥3.5建议申请，<3.0建议跳过）
5. **Gaps & 亮点** — 列出关键gap和你的差异化优势
6. **薪资区间** — 如JD提供，标注；否则根据市场估算

### Output format
```markdown
## 评估：[公司] [职位]（[城市]）

### 10维度评分
[表格]

### 综合评分：X.X / 5.0
[一句话建议]

### 关键Gap
- ...

### 差异化亮点
- ...
```

## Workflow 2: 加入Tracker & 状态更新

### 加入Tracker

用户说"加入"/"保存"时：
1. 追加一行到 `<USER>/tracker.csv`（`id` 自增，`status` 默认 `evaluating`，`last_updated` 为当天）
2. 创建 `<USER>/jobs/{company}_{role}/eval.md`
3. 创建 `<USER>/jobs/{company}_{role}/timeline.md`，写入第一条记录

### 更新状态

用户说"更新状态"/"面试了"/"拿到offer"/"被拒了"等触发：
1. 更新 `tracker.csv` 中对应行的 `status` 和 `last_updated`
2. 在 `timeline.md` 末尾追加一行新记录（日期 + 新状态 + 用户提供的备注）
3. 如用户提供了面试细节（问了什么、感受如何），一并记录在备注中

> **不覆盖历史** — tracker.csv 只反映当前状态，timeline.md 保留完整轨迹。

## Workflow 3: 简历定制

### Rules
1. 基于 `<USER>/resume/cv_cn.md` / `cv_en.md`（母版简历）创建定制版本
2. **绝不添加母版简历中没有的经历、技能或描述** — 只能重排、强调、精简、改写
3. 定制策略：职位标题可适当调整措辞、重排经历顺序、突出相关技能、精简不相关内容
4. 中英文各生成一份
5. 保存到 `<USER>/jobs/{company}_{role}/cv_cn.md` / `cv_en.md`
6. 不写“求职意向”段落

### Rewriting Guidelines（简历改写三步法）

对母版简历中的每条经历描述，按以下三步进行改写优化：

| 步骤 | 规则 | 示例 |
|------|------|------|
| 1. 职责→问题 | 不写“负责XX”，改为“针对XX问题…” | “针对客户需求反复的问题，负责需求确认、进度同步和风险反馈，保障项目按节点推进” |
| 2. 过程→动作 | 少写“参与/协助/负责”，多用强动词 | 梳理、推动、搭建、优化、拆解、跟进、复盘、转化、主导、落地 |
| 3. 补充结果 | 每条必须有结果，哪怕结果不大也要有 | 缩短周期、减少返工、提高响应、完成交付、降低投诉、稳定客户关系 |

**关键词匹配**：JD 中出现的关键词，简历里也要体现（用母版中已有的素材重新组织语言）。

## Workflow 4: 面试准备

针对某个具体岗位生成全面的面试准备资料，输出为方便网页/移动端查看的 HTML 页面。
触发词：“面试准备”“prepare interview”“给我出个面试准备”。

### Input
- 目标职位（已在 tracker 中，或用户指定）
- 可选：面试轮次信息（如“一面”“HR面+业务面”“终面”）

### Steps

1. **读取背景资料**
   - `<USER>/resume/cv_cn.md`（母版简历，特别是个人总结 + 项目案例 + 个人故事）
   - `<USER>/jobs/{company}_{role}/eval.md`（JD原文 + 评估报告）
   - `<USER>/profile.md`（求职偏好）

2. **生成面试准备 HTML**，包含以下模块：

   | 模块 | 内容 |
   |------|------|
   | ① 公司速记卡 | 公司背景、业务、文化、近期新闻（可用 `fetch_webpage` 抓取官网） |
   | ② 岗位理解 | JD解读、核心能力要求、我的匹配点 |
   | ③ 自我介绍 | **1分钟版** + **3分钟版**（见下方结构） |
   | ④ STAR故事库 | 从母版简历“B. 个人故事”中挑选与本JD最相关的故事，按维度分组 |
   | ⑤ 高频问题 & 参考回答 | 专业题、业务情景题、行为面试题 |
   | ⑥ 反问清单 | 3-5个有质量的反问 |
   | ⑦ 临场 Checklist | 着装、资料、心态提醒 |

3. **保存** 到 `<USER>/jobs/{company}_{role}/interview_prep.html`

### 自我介绍结构

两个版本都包含三个部分，通过第二部分的详略控制时长：

| 部分 | 内容要求 |
|------|---------|
| 我是谁 | 姓名 + 教育背景（学校/专业/研究方向）+ 工作年限 + 当前公司/部门/职位 |
| 做过什么 & 解决过什么问题 | 与目标岗位最相关的核心能力、项目经历和关键成果 |
| 为什么看这个岗位 | 岗位匹配度 + 个人发展诉求（结合 profile.md 核心目标） |

**1分钟版**（约 200 字）：
- "我是谁"简明扼要
- "做过什么"只讲与岗位匹配的 2-3 个核心能力标签 + 1-2 个关键数字成果，不展开项目细节
- "为什么看这个岗位"一句话收尾

**3分钟版**（约 500-600 字）：
- "我是谁"可稍展开研究方向/职业脉络
- "做过什么"快速介绍与岗位最匹配的 1-2 个项目（背景→做了什么→成果），体现能力深度
- "为什么看这个岗位"可展开说对公司/岗位的理解和个人发展规划

### HTML 样式要求

- 响应式设计，移动端友好（max-width 限制，小屏自适应）
- 清晰的目录导航（锚点跳转）
- 视觉分区：信息卡片、引用框、警告框、提示框、STAR标签
- 字体：系统字体栈（-apple-system, PingFang SC, Microsoft YaHei 等）
- 单文件 HTML，无外部依赖，可直接用浏览器打开

## Workflow 5: JD抓取 (fetch_jd.py)

对于SPA页面，使用 `util/fetch_jd.py` 脚本（Playwright + Edge）：
```powershell
python util/fetch_jd.py "<url>"
```
**已知限制**：Boss直聘检测CDP协议，自动跳转about:blank，无法使用。详见 [references/spa-scraping-notes.md](references/spa-scraping-notes.md)。

## Important Notes

- 评估必须基于简历中的**实际经历**，不可虚构匹配度
- 分数需附具体理由，不能只给数字
- 定制简历严格基于母版简历内容，**禁止凭空添加母版中没有的经历**
- tracker.csv 是 single source of truth，每次操作后确认一致性
- 母版简历可迭代补充，但只能追加用户提供的真实经历，不可虚构
