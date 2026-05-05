from playwright.sync_api import Page

class BasePage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, path: str = "") -> None:
        self.page.goto(path)

    def get_title(self) -> str:
        return self.page.title()

    def take_screenshot(self, name: str) -> None:
        self.page.screenshot(
            path=f"reports/screenshots/{name}.png",
            full_page=True
        )