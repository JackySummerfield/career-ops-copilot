# SPA页面抓取经验 & WLB参考资源

## SPA抓取限制

### Boss直聘 (zhipin.com) — 无法自动化
*Source: 2026-06-03 — job search session*

Boss直聘检测CDP（Chrome DevTools Protocol）连接本身，属于深层反爬机制：
- Playwright headed + stealth JS（`--disable-blink-features=AutomationControlled`、覆盖`navigator.webdriver`/`chrome.runtime`/`plugins`/`languages`）→ 仍跳转 about:blank
- 复用Edge User Data → 冲突（about:blank）
- 独立profile + 反检测 → 仍被检测

**结论：Boss直聘只能手动复制粘贴JD文本。**

### 可成功抓取的平台
- ✅ 阿里云招聘 (careers.aliyun.com) — 静态渲染
- ✅ 猎聘 (liepin.com) — 静态渲染
- ✅ Workday系统 (如液化空气) — 静态渲染
- ❌ Boss直聘 — CDP检测
- ❌ 蚂蚁招聘 — SPA（未尝试Playwright）
- ❌ 西门子 — SPA（未尝试Playwright）
- ❌ Bosch — SPA（未尝试Playwright）

### fetch_jd.py 设计要点
- 使用 `playwright` + Edge (msedge channel)
- 独立profile目录（不冲突用户正在使用的Edge）
- 验证码处理：检测内容长度 < 200字符 → 暂停等待用户手动处理 → 用户按Enter继续
- stealth注入：在 `page.goto()` 前用 `add_init_script()` 覆盖fingerprint

---

## GitHub WLB参考项目
*Source: 2026-06-03 — job search session*

| 项目 | 内容 | 链接 |
|------|------|------|
| **955.WLB** | 955公司白名单（相对不加班） | [formulahendry/955.WLB](https://github.com/formulahendry/955.WLB) |
| **996.ICU** | 996公司黑名单（含证据） | [996icu/996.ICU](https://github.com/996icu/996.ICU) |

**使用建议**：
- 作为求职时WLB的辅助参考，不作为评分维度（同公司不同BU差异大）
- 脉脉/看准网/Glassdoor 等点评网站均有反爬，`fetch_webpage` 无法抓取
- 训练数据中的公开信息（截止2025年）可给出大致WLB估计+置信度
