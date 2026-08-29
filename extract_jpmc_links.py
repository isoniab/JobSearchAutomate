import asyncio
from playwright.async_api import async_playwright
import json

async def extract_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        page = await context.new_page()

        url = "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions?location=Bengaluru"
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)

        # Extract links and titles
        links = await page.evaluate('''() => {
            const results = [];
            const anchors = Array.from(document.querySelectorAll('a'));
            anchors.forEach(a => {
                if (a.href && (a.href.includes('job') || a.href.includes('requisitions') || a.innerText.length > 5)) {
                    results.push({
                        text: a.innerText.trim(),
                        href: a.href
                    });
                }
            });
            return results;
        }''')

        print(f"Extracted {len(links)} links from page:")
        for l in links[:15]:
            print(f"- [{l['text']}] -> {l['href']}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(extract_links())
