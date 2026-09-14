from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def extract_web_text(url):

    with sync_playwright() as p:

        browser = p.firefox.launch()

        page = browser.new_page()

        page.goto(
            url,
            wait_until="networkidle"
        )

        html = page.content()

        browser.close()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    return soup.get_text(
        separator=" ",
        strip=True
    )