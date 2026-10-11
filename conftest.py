import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.saucedemo.com"


@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Descomentar para CI sin pantalla
    options.add_argument("--window-size=1366,768")

    service = ChromeService(ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=service, options=options)
    _driver.implicitly_wait(0)

    yield _driver

    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        os.makedirs("reports", exist_ok=True)
        _driver.save_screenshot(f"reports/{request.node.name}.png")
    _driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)