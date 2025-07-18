import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os

class ScrapingAgent:
    """
    An agent that scrapes text content and takes a screenshot of a given URL.
    """
    def __init__(self, screenshot_dir="outputs/screenshots"):
        self.screenshot_dir = screenshot_dir
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    async def scrape(self, url: str, chapter_name: str) -> tuple[str, str]:
        """
        Scrapes the text content from the URL and takes a screenshot.

        Args:
            url: The URL of the chapter to scrape.
            chapter_name: A name for the chapter, used for the screenshot filename.

        Returns:
            A tuple containing the extracted text and the path to the screenshot.
        """
        print(f"ScrapingAgent: Fetching content from {url}")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle")

                # Take Screenshot
                screenshot_path = os.path.join(self.screenshot_dir, f"{chapter_name}.png")
                await page.screenshot(path=screenshot_path, full_page=True)
                print(f"ScrapingAgent: Screenshot saved to {screenshot_path}")

                # Extract Text Content using BeautifulSoup for better parsing
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')

                # This selector is specific to the wikisource page structure.
                # It might need adjustment for other sites.
                content_div = soup.find('div', class_='mw-parser-output')
                if content_div:
                    # Remove unwanted elements like tables of contents, navigation, etc.
                    for toc in content_div.find_all('div', id='toc'):
                        toc.decompose()
                    for nav in content_div.find_all('div', class_='noprint'):
                        nav.decompose()

                    text_content = content_div.get_text(separator='\n', strip=True)
                else:
                    # Fallback to body if the specific div isn't found
                    text_content = soup.body.get_text(separator='\n', strip=True)

                await browser.close()
                print("ScrapingAgent: Successfully extracted text content.")
                return text_content, screenshot_path
        except Exception as e:
            print(f"ScrapingAgent: An error occurred: {e}")
            return "", ""