import asyncio
import re
import time
from bs4 import BeautifulSoup
from pyppeteer import launch

start_time = time.time()

async def fetch_page_source(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    # Wait for JavaScript to render (increase waiting time)
    # await page.waitForSelector('body', timeout=5000)
    await asyncio.sleep(1)  # Adjust the delay time as needed
    content = await page.content()
    await browser.close()
    return content

async def main():
    # URL of the website
    url = "https://rugcheck.xyz/tokens/DXcdWQp9QpvjSupD7hnX7BQxKKWsCaKXsaAxd9SFN3VM"

    # Fetch the page source asynchronously
    page_source = await fetch_page_source(url)

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all elements containing float percentage values (e.g., 0.00%)
    percentage_elements = soup.find_all(string=re.compile(r'\b\d+\.\d+%'))

    # Exclude the first two percentage elements
    percentage_list = percentage_elements[3:]

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    print(percentage_list)

# Run the event loop
asyncio.get_event_loop().run_until_complete(main())
