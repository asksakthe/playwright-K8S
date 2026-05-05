import os
import pytest
from playwright.sync_api import sync_playwright
from utils.config import Config
from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def config():
    return Config()

@pytest.fixture(scope="session")
def browser(config):
    os.makedirs("reports/screenshots", exist_ok=True)
    pw = sync_playwright().start()
    browser_type = getattr(pw, config.browser_type)
    b = browser_type.launch(headless=config.headless)
    yield b
    b.close()
    pw.stop()

@pytest.fixture(scope="function")
def page(browser, config):
    context = browser.new_context(base_url=config.base_url)
    context.set_default_timeout(config.timeout)
    p = context.new_page()
    yield p
    context.close()

@pytest.fixture(scope="function")
def login_page(page):
    return LoginPage(page)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        name = request.node.name
        path = f"reports/screenshots/FAIL_{name}.png"
        page.screenshot(path=path, full_page=True)
        print(f"\nScreenshot saved: {path}")