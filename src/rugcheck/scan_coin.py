import asyncio
import re
import time
from bs4 import BeautifulSoup
from pyppeteer import launch


class RugChecker:
    def __init__(self):
        self.mint_address = None
        self.url = None

    async def fetch_page_source(self):
        try:
            browser = await self.launch_browser()
            page = await browser.newPage()
            await page.goto(self.url, timeout=30000)
            await page.waitForSelector('body')
            content = await page.content()
            await browser.close()
            return content
        except Exception as e:
            print(f"Error fetching page source: {e}")
            return None

    async def launch_browser(self):
        return await launch(headless=True)

    async def check_rug(self, mint_address):
        self.mint_address = mint_address
        self.url = f"https://rugcheck.xyz/tokens/{self.mint_address}"

        retry_count = 3
        while retry_count > 0:
            page_source = await self.fetch_page_source()
            if page_source:
                soup = BeautifulSoup(page_source, 'html.parser')
                percentage_elements = soup.find_all(string=re.compile(r'\b\d+\.\d+%'))
                percentage_list = percentage_elements[3:]
                return percentage_list
            else:
                retry_count -= 1
                await asyncio.sleep(5)
        print("Failed to fetch page source after retries.")
        return None
