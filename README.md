# Career Optimization Copilot

国内求职AI助手(Copilot Skill) — JD评估、Tracker管理、简历定制、STAR面试素材结构化。

## About

一个 VS Code Copilot Chat 的自定义 Skill，提供端到端的求职辅助：
- 粘贴JD文本或URL → 自动10维度打分评估
- 一句话加入tracker → 维护CSV格式的职位追踪表
- 基于原始简历生成定制版本（严格不添加虚构内容）
- 将零散经历整理为标准STAR结构的面试故事

## Getting Started

### Prerequisites

- [VS Code](https://code.visualstudio.com/) 1.99+
- [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) 扩展（需有效订阅）
- Python 3.10+（用于 SPA 页面抓取，可选）

### Installation

1. **Clone Skill 到 Copilot skills 目录**

   ```bash
   # Windows
   git clone https://github.com/<your-username>/career-opt-copilot.git "%USERPROFILE%\.copilot\skills\career-opt-copilot"

   # macOS / Linux
   git clone https://github.com/<your-username>/career-opt-copilot.git ~/.copilot/skills/career-opt-copilot
   ```

2. **初始化求职工作区**

   在你希望存放简历和求职材料的文件夹中创建以下结构：

   ```bash
   mkdir -p job-search/{jds,reports,tailored,interview-prep}
   ```

   然后创建必要的文件：

   ```bash
   # 职位追踪表
   echo "id,company,role,url,score,status,applied_date,response_date,notes" > job-search/tracker.csv

   # 原始简历（用你自己的内容替换）
   touch job-search/cv_cn.md job-search/cv_en.md

   # STAR 面试素材库
   echo "# 面试STAR素材库" > job-search/interview_stories.md
   ```

3. **（可选）安装 SPA 页面抓取依赖**

   部分招聘网站需要 Playwright 渲染 JS 后才能抓取内容：

   ```bash
   pip install playwright
   playwright install chromium
   ```

   > ⚠️ **已知限制**：Boss直聘检测 CDP 协议，即使使用 stealth 模式也会跳转 about:blank，只能手动粘贴 JD 文本。详见 [references/spa-scraping-notes.md](references/spa-scraping-notes.md)。

4. **验证安装**

   在 VS Code 中打开求职工作区，启动 Copilot Chat，输入：

   ```
   评估这个JD：[粘贴任意 JD 文本]
   ```

   如果 Copilot 返回10维度评分表格，说明 Skill 已生效。

### File Structure

```
career-opt-copilot/
├── SKILL.md                        # Skill 定义与 Workflow 指令
├── README.md                       # 本文件
└── references/
    └── spa-scraping-notes.md       # SPA 页面抓取经验 & WLB 参考资源
```

### Workspace Layout

Skill 操作的目标文件位于用户求职工作区下：

```
job-search/
├── tracker.csv           # 职位追踪表 (single source of truth)
├── cv_cn.md / cv_en.md   # 原始简历（不可修改）
├── interview_stories.md  # STAR 素材库
├── jds/                  # JD 原文存档
├── reports/              # 评估报告
├── tailored/             # 定制简历
└── interview-prep/       # 面试准备材料
```

## Usage

### 触发示例

| 场景 | 触发语 |
|------|--------|
| 评估职位 | `评估这个JD：[粘贴文本]` |
| 加入追踪 | `加入` / `加入tracker` |
| 定制简历 | `定制简历，针对#6 XX公司AI产品经理` |
| 面试素材 | `帮我整理这段经历为STAR格式` |
| 抓取JD | `试试抓取这个链接：[URL]` |

### 评估输出格式

```markdown
## 评估：[公司] [职位]（[城市]）

### 10维度评分
| 维度 | 分数 | 说明 |
|------|------|------|
| 角色匹配 | x.x | ... |
| ...      | ... | ... |

### 综合评分：X.X / 5.0
### 关键Gap / 差异化亮点
```

## Workflow Overview

| # | Workflow | 说明 |
|---|---------|------|
| 1 | JD评估 | 解析JD → 读取简历 → 10维度评分 → 综合建议 |
| 2 | 加入Tracker | 追加CSV行，自增ID，默认status=evaluating |
| 3 | 简历定制 | 基于原始简历重排/强调/精简，禁止凭空添加 |
| 4 | STAR整理 | 结构化 → 识别不足 → 补充 → 完整版+面试tips |
| 5 | JD抓取 | fetch_webpage 或 fetch_jd.py (Playwright+Edge) |

## Roadmap

- [ ] 支持批量JD对比（多个JD并排打分）
- [ ] 自动生成Cover Letter
- [ ] 面试日程管理（tracker增加interview_date列）
- [ ] 集成搜索引擎MCP获取公司WLB信息

## Acknowledgments

- [career-ops](https://github.com/santifer/career-ops) — 项目灵感来源
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) — README结构参考
- [Playwright](https://playwright.dev/) — SPA页面自动化抓取
- [955.WLB](https://github.com/formulahendry/955.WLB) / [996.ICU](https://github.com/996icu/996.ICU) — WLB参考数据
