from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.data_factory import LoginCredentials

class LoginPage(BasePage):

    URL = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button   = page.locator("button[type='submit']")
        self.success_message = page.locator(".flash.success")
        self.error_message   = page.locator(".flash.error")

    def open(self) -> "LoginPage":
        self.navigate(self.URL)
        return self

    def login(self, creds: LoginCredentials) -> "LoginPage":
        self.username_input.fill(creds.username)
        self.password_input.fill(creds.password)
        self.login_button.click()
        return self

    def get_success_message(self) -> str:
        self.success_message.wait_for(state="visible")
        return self.success_message.inner_text()

    def get_error_message(self) -> str:
        self.error_message.wait_for(state="visible")
        return self.error_message.inner_text()

    def is_loaded(self) -> bool:
        return self.login_button.is_visible()