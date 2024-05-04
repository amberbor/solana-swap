import asyncio
import re
import time
from bs4 import BeautifulSoup
from pyppeteer import launch


class RugChecker:
    def __init__(self):
        self.mint_address = None
        self.url = f"https://rugcheck.xyz/tokens/{self.mint_address}"

    async def fetch_page_source(self):
        browser = await self.launch_browser()
        page = await browser.newPage()
        await page.goto(self.url)
        await asyncio.sleep(5)  # Replaced asyncio.sleep with time.sleep
        content = await page.content()
        await browser.close()
        return content

    async def launch_browser(self):
        return await launch(headless=True)

    async def check_rug(self, mint_address):
        self.mint_address = mint_address
        self.url = f"https://rugcheck.xyz/tokens/{self.mint_address}"
        page_source = await self.fetch_page_source()

        soup = BeautifulSoup(page_source, 'html.parser')

        percentage_elements = soup.find_all(string=re.compile(r'\b\d+\.\d+%'))

        percentage_list = percentage_elements[3:]

        return percentage_list
