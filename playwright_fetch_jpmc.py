import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_jpmc_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = await context.new_page()

        print("🌐 Navigating to JPMorgan Oracle Cloud Portal...")
        url = "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions?location=Bengaluru"
        await page.goto(url, wait_until="networkidle", timeout=30000)

        await page.wait_for_timeout(5000)

        page_title = await page.title()
        print(f"📄 Page Title: {page_title}")

        # Extract requisition cards
        job_cards = await page.query_selector_all(".requisition-list-item, .job-tile, [data-qa='requisitionTile']")
        print(f"Found {len(job_cards)} job elements on page.")

        # Take screenshot for proof
        await page.screenshot(path="jpmc_portal_screenshot.png")
        print("📸 Saved portal screenshot to jpmc_portal_screenshot.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_jpmc_jobs())
