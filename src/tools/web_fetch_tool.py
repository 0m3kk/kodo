from playwright.async_api import async_playwright
from html2text import html2text


class WebFetchTools:
    """
    A class for fetching web content using a headless browser.
    """

    def __init__(self):
        """Initializes the WebFetchTools."""
        pass

    async def fetch_page_content(
        self, url: str, limit: int = -1, offset: int = 0, convert_to_text: bool = False
    ) -> str:
        """
        Fetches the full HTML content of a given URL using a headless browser.

        Args:
            url: The URL to fetch.

        Returns:
            The HTML content of the page as a string, or an error message.
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                content = await page.content()
                await browser.close()
                if convert_to_text:
                    content = html2text(content)
                if offset > 0:
                    content = content[offset:]
                if limit > -1:
                    content = content[:limit]
                return content
        except Exception as e:
            return f"Error fetching URL {url} with headless browser: {e}"
