import pytest
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password", [
    ("Sojib", "!@#$%^&*"),
    ("Sojib", "WrongPassword"),
    ("WrongUserName", "Wrong!@#$%^&*"),


])
def test_login(driver, username, password):
    driver.get("http://127.0.0.1:8000/user/login/")

    # Find form fields and button
    username_field = driver.find_element(By.ID, "id_username")
    password_field = driver.find_element(By.ID, "id_password")
    submit_button =  driver.find_element(By.CSS_SELECTOR, ".btn")

    username_field.send_keys(username)
    password_field.send_keys(password)
    submit_button.click()

    time.sleep(1)


