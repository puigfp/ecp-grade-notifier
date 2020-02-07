# std
import logging
import urllib
import os

# 3p
from tenacity import retry, before_sleep_log, stop_after_attempt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

ECP_SSO_USERNAME = os.environ["ECP_SSO_USERNAME"]
ECP_SSO_PASSWORD = os.environ["ECP_SSO_PASSWORD"]

NOTES_ET_DOSSIER_URL = os.environ["NOTES_ET_DOSSIER_URL"]
NOTES_ET_DOSSIER_GRADES_PAGE = os.environ["NOTES_ET_DOSSIER_GRADES_PAGE"]

logging.basicConfig()
logger = logging.getLogger("fetch-grades")
logger.setLevel(logging.DEBUG)


def get_browser(headless=False):
    options = Options()
    options.headless = headless
    return webdriver.Firefox(options=options)


@retry(
    stop=stop_after_attempt(2), before_sleep=before_sleep_log(logger, logging.WARNING)
)
def fetch_grades_table(username, password, page):
    browser = get_browser(headless=True)
    try:
        # try to load grades webpage
        browser.get(NOTES_ET_DOSSIER_URL)

        # we get redirected to the login page -> we fill the login form and submit it
        login_form = browser.find_element_by_xpath("//form")

        username_field = login_form.find_element_by_name("username")
        username_field.send_keys(username)

        password_field = login_form.find_element_by_name("password")
        password_field.send_keys(password)

        login_form.submit()

        # wait for grade page to load
        WebDriverWait(browser, 3).until(
            expected_conditions.url_contains(NOTES_ET_DOSSIER_URL)
        )

        # go to grades page
        browser.get(urllib.parse.urljoin(NOTES_ET_DOSSIER_URL, page))

        # extract grades table
        table = browser.find_element_by_xpath("//table[@summary='Affichage des notes']")

        return table.text
    finally:
        # whatever happens, close the browser (we don't want to leak a firefox process)
        browser.close()


if __name__ == "__main__":
    print(
        fetch_grades_table(
            ECP_SSO_USERNAME, ECP_SSO_PASSWORD, NOTES_ET_DOSSIER_GRADES_PAGE
        )
    )
