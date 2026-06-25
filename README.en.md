<div align="center">

[中文](README.md) · English

# 💼 Career Ops Copilot

#### A VS Code Copilot Skill for evaluating JDs, tracking applications, tailoring resumes, and preparing for interviews

![VS Code 1.99+](https://img.shields.io/badge/VS_Code-1.99+-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![GitHub Copilot](https://img.shields.io/badge/GitHub_Copilot-Skill-000?style=for-the-badge&logo=githubcopilot&logoColor=white)
![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

[Why This Exists](#-why-this-exists) · [What It Does](#-what-it-does) · [Quick Start](#-quick-start) · [Workflow](#-workflow-overview)

</div>

---

## 🤔 Why This Skill

Inspired by [career-ops](https://github.com/santifer/career-ops) and rebuilt for the **VS Code + GitHub Copilot** ecosystem, with extensions for the Chinese job market:

- **Copilot-native** — SKILL.md format, trigger phrases, and tool calls follow Copilot conventions
- **10-dimension JD evaluation** — Scores role fit, skill coverage, growth potential, salary, WLB, etc. independently to support application decisions
- **Interview prep generation** — STAR story structuring + HTML interview handbook (company background, common questions, counter-questions)
- **Multi-user isolation** — `users/<name>/` workspaces with gitignored personal data; the Skill itself is shareable
- **No-fabrication resume tailoring** — Only reorder, emphasize, and condense; never invent experiences
- **China job platform support** — SPA scraping for Boss Zhipin, Liepin, and similar platforms

## 📋 What It Does

| Feature | Trigger | Description |
|---------|---------|-------------|
| Evaluate JD | `Evaluate this JD: [text]` | 10-dimension scoring + overall rating + gap analysis |
| Track Jobs | `Add to tracker` | CSV-based job tracker with auto-increment ID and status management |
| Tailor Resume | `Tailor resume for #6 Company X` | Generate a customized resume from your master copy — strictly no fabrication |
| Interview Prep | `Structure this experience as STAR` | Turn scattered experiences into standard STAR format, generate interview handbook |
| Fetch JD | `Fetch this link: [URL]` | Auto-scrape job posting pages (SPA support via Playwright) |

## 🚀 Quick Start

**1. Clone to Copilot skills directory**

```bash
# Windows
git clone https://github.com/<your-username>/career-ops-copilot.git "%USERPROFILE%\.copilot\skills\career-ops-copilot"

# macOS / Linux
git clone https://github.com/<your-username>/career-ops-copilot.git ~/.copilot/skills/career-ops-copilot
```

**2. Initialize your workspace**

In Copilot Chat, type `Initialize job search workspace` and follow the prompts to fill in your resume.

**3. Verify**

Type `Evaluate this JD: [paste any JD]`. If you see a 10-dimension scoring table, you're all set.

> 💡 Some job sites (e.g. Boss Zhipin) require Playwright for scraping: `pip install playwright && playwright install chromium`. See [references/spa-scraping-notes.md](references/spa-scraping-notes.md) for details.

## ⚙️ Workflow Overview

```mermaid
graph LR
    A[User Profile Input] --> B[Master Resume]
    B --> C[Fetch JD]
    C --> D[10-Dim Evaluation]
    D --> E{Worth applying?}
    E -->|Yes| F[Add to Tracker]
    E -->|No| C
    F --> G[Tailor Resume]
    G --> H[Interview Prep]
```

> 💡 The master resume is a living document — enrich it after each interview debrief or new project.

## � Output Examples

<details>
<summary><b>Master Resume</b></summary>

```markdown
# San Zhang | Senior Product Manager

## Contact
- Phone: 138-xxxx-xxxx | Email: zhangsan@email.com
- Location: Beijing | Expected Salary: 80-100w CNY

## Target Role
AI Product Director / AI Platform Product Lead

## Professional Summary
6 years in product, focused on AI/data platforms. Skilled at 0-to-1 builds and scaled deployment.

## Core Skills
- Product strategy & roadmap
- LLM/NLP application deployment
- Cross-functional leadership (8-person team)
- A/B experimentation systems
- Data-driven decision making

## Experience

### Senior Product Manager | ABC Tech | 2022.03 - Present
- Built AI platform product from 0 to 1, grew DAU from 0 to 50K
- Managed 8-person product team, led cross-functional collaboration
- Drove LLM deployment, launched AI CS module, reduced human escalation by 40%

### Product Manager | DEF Internet | 2019.06 - 2022.02
- Owned e-commerce search & recommendation module, lifted GMV by 15%
- Designed A/B experiment platform supporting 200+ concurrent experiments

## Education
- M.S. | XX University, Computer Science | 2017-2019
- B.S. | XX University, Software Engineering | 2013-2017

## Project Highlights / STAR Library
(See interview_stories.md)

## Certifications & Other
- PMP Certified
- English: Fluent (IELTS 7.5)
```

</details>

<details>
<summary><b>10-Dimension Evaluation</b></summary>

```markdown
## Evaluation: ABC Tech — AI Product Director (Beijing)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Role Fit | 4.5 | Natural career progression from current role |
| Skill Coverage | 4.0 | LLM deployment experience matches well; lacks P&L ownership |
| Experience Level | 4.0 | Requires 5+ yrs, have 6 |
| Industry Fit | 3.5 | AI direction aligned, but to-B → to-C is a leap |
| Growth Potential | 4.5 | Reports to VP, team expansion planned |
| Salary Range | 4.0 | 80-120w CNY, meets expectations |
| Company Scale | 3.5 | Series B, some uncertainty |
| Location | 5.0 | Local |
| Culture Fit | 4.0 | Flat, engineering-driven |
| Competition | 3.0 | Role open 3 weeks, competitive |

**Overall: 4.05 / 5.0**

**Key Gap**: No standalone P&L responsibility
**Differentiator**: LLM deployment track record + A/B platform design
```

</details>

<details>
<summary><b>Interview Prep Material</b></summary>

```markdown
# Interview Prep: ABC Tech — AI Product Director

## Company Background
- ABC Tech, Series B, AI SaaS vertical, raised 200M CNY in 2023
- Core product: Enterprise AI platform serving finance/retail
- Team size: ~200 total, 20 in product

## Role Key Info
- Reports to: VP of Product
- Team: 5 direct reports, 8 dotted-line
- Core KPIs: AI module revenue, customer renewal rate

## STAR Stories (Matched to JD Requirements)

### Story 1: Launching LLM Customer Service (matches "AI deployment experience")
**S**: 30-person CS team, 2000+ daily tickets, high labor cost
**T**: Ship intelligent CS by Q3, reduce human escalation
**A**: Vendor evaluation → hybrid design → cross-team alignment → canary rollout
**R**: Human escalation 72%→40%, saving ~450K CNY/month

### Story 2: Building A/B Experiment Platform (matches "data-driven")
**S**: Teams running experiments without standardization, unreliable results
**T**: Build unified experiment platform
**A**: Define metrics framework → develop traffic splitting engine → establish review process
**R**: Supported 200+ concurrent experiments, decision efficiency up 60%

## Common Questions Prep
- Q: How do you drive a cross-functional project?
- Q: Describe a product decision that failed and your retrospective
- Q: How do you measure AI product ROI?

## Counter-Questions
- What are the top 3 priorities for this role in the next 6 months?
- What's the current tech debt / org debt on the team?
- What does the reporting line and decision-making process look like?
- What stage is AI module commercialization at?
```

</details>

## �🙏 Acknowledgments

- [career-ops](https://github.com/santifer/career-ops) — Original inspiration
- [Playwright](https://playwright.dev/) — SPA page scraping
- [955.WLB](https://github.com/formulahendry/955.WLB) / [996.ICU](https://github.com/996icu/996.ICU) — WLB reference data
