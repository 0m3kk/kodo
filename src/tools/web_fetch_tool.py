from playwright.async_api import async_playwright

class WebFetchTools:
    """
    A class for fetching web content using a headless browser.
    """

    def __init__(self):
        """Initializes the WebFetchTools."""
        pass

    async def fetch_page_content(self, url: str) -> str:
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
                return content
        except Exception as e:
            return f"Error fetching URL {url} with headless browser: {e}"