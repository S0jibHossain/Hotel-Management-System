import pytest
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    # Set up ChromeDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Allow elements to load
    yield driver
    driver.quit()


@pytest.mark.parametrize("username, email, password1, password2", [
    ("Sojib", "sojib@example.com", "password123", "password123"),  # Valid case
    ("JohnDoe", "johndoe@example.com", "pass123", "wrongpass"),  # Password mismatch
    ("TestUser", "testuser@example.com", "password321", "password321"),  # Another valid case
])
def test_user_registration(driver, username, email, password1, password2):
    # Navigate to registration page
    driver.get("http://127.0.0.1:8000/user/user_register/")

    # Find the form fields using their ID attributes
    username_field = driver.find_element(By.ID, "id_username")
    email_field = driver.find_element(By.ID, "id_email")
    password1_field = driver.find_element(By.ID, "id_password1")
    password2_field = driver.find_element(By.ID, "id_password2")
    submit_button = driver.find_element(By.CSS_SELECTOR, ".btn-register")

    # Input data into the form fields
    username_field.send_keys(username)
    email_field.send_keys(email)
    password1_field.send_keys(password1)
    password2_field.send_keys(password2)

    # Submit the form
    submit_button.click()

    # Wait for processing
    time.sleep(2)

