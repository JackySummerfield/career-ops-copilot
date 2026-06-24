"""
fetch_jd.py - 使用Playwright抓取SPA页面的职位描述
用法: python fetch_jd.py [url]

支持蚂蚁、西门子等SPA渲染的招聘网站。
如遇验证码/登录拦截，会暂停等待用户手动操作后继续。

注意：Boss直聘(zhipin.com)检测CDP协议，Playwright无法绕过，只能手动复制粘贴。
"""

from playwright.sync_api import sync_playwright
import sys
import time
from pathlib import Path


# 隐藏Playwright自动化特征的JS脚本
STEALTH_JS = """
// 覆盖 navigator.webdriver
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

// 覆盖 chrome runtime
window.chrome = { runtime: {} };

// 覆盖 permissions
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
    Promise.resolve({ state: Notification.permission }) :
    originalQuery(parameters)
);

// 覆盖 plugins
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5],
});

// 覆盖 languages
Object.defineProperty(navigator, 'languages', {
    get: () => ['zh-CN', 'zh', 'en'],
});
"""


def fetch_jd(url: str, output_dir: str = "jds") -> str:
    with sync_playwright() as p:
        # 使用Edge浏览器，独立profile（避免与正在使用的Edge冲突）
        browser = p.chromium.launch(
            executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
            headless=False,
            channel="msedge",
            args=[
                "--disable-blink-features=AutomationControlled",  # 隐藏自动化标志
            ],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        )
        # 注入stealth脚本，在每个页面加载前执行
        context.add_init_script(STEALTH_JS)
        page = context.new_page()

        print(f"正在打开: {url}")
        page.goto(url, wait_until="domcontentloaded")

        # 等待页面内容加载，给JS渲染一点时间
        time.sleep(3)

        # 检查页面是否正常加载（简单判断：页面文本长度）
        body_text = page.inner_text("body")
        if len(body_text.strip()) < 100:
            print("\n⚠️  页面内容过少，可能遇到验证码或登录拦截")
            print("    请在浏览器中完成操作，然后回到终端按 Enter 继续...")
            input()
            time.sleep(2)
            body_text = page.inner_text("body")

        # 再次确认：让用户决定是否内容已加载完整
        print("\n页面已加载，请确认浏览器中职位详情已完整显示。")
        print("按 Enter 提取内容（如需等待加载，请先在浏览器中操作完毕）...")
        input()

        # 提取页面文本
        body_text = page.inner_text("body")

        # 获取页面标题
        title = page.title()

        browser.close()

    # 组装结果
    result = f"# {title}\n\nURL: {url}\n\n---\n\n{body_text}"

    # 保存到文件
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # 用时间戳+简化URL作为文件名
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"jd_{timestamp}.txt"
    filepath = output_path / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"\n✅ 已保存到: {filepath}")
    print(f"   文本长度: {len(body_text)} 字符")

    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("请输入职位URL: ").strip()

    if not url:
        print("❌ 未提供URL")
        sys.exit(1)

    content = fetch_jd(url)

    # 打印前500字符预览
    print("\n" + "=" * 60)
    print("预览（前500字符）:")
    print("=" * 60)
    print(content[:500])
    if len(content) > 500:
        print(f"\n... (共 {len(content)} 字符，完整内容已保存到文件)")
