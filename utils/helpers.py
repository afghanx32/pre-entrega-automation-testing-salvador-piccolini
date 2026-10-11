from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME_INPUT = (By.CSS_SELECTOR, "#user-name")
PASSWORD_INPUT = (By.CSS_SELECTOR, "#password")
LOGIN_BUTTON = (By.CSS_SELECTOR, "#login-button")
INVENTORY_TITLE = (By.CSS_SELECTOR, ".title")
APP_LOGO = (By.CSS_SELECTOR, ".app_logo")

INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
FIRST_PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
# Selector más robusto para el primer botón "Add to cart"
FIRST_ADD_BUTTON = (By.CSS_SELECTOR, ".btn_inventory")
CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
CART_ITEM = (By.CLASS_NAME, "cart_item")

BASE_URL = "https://www.saucedemo.com"
INVENTORY_URL_FRAGMENT = "/inventory.html"
CART_URL_FRAGMENT = "/cart.html"
TIMEOUT = 10


def login_as_standard_user(driver, username="standard_user", password="secret_sauce"):
    wait = WebDriverWait(driver, TIMEOUT)
    driver.get(BASE_URL)
    wait.until(EC.visibility_of_element_located(USERNAME_INPUT)).send_keys(username)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)
    driver.find_element(*LOGIN_BUTTON).click()
    wait.until(EC.url_contains(INVENTORY_URL_FRAGMENT))


def add_first_product_to_cart(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(EC.visibility_of_element_located(INVENTORY_ITEMS))
    product_name = driver.find_elements(*FIRST_PRODUCT_NAME)[0].text
    
    # Busca los botones de inventario y hace clic en el primero
    add_button = wait.until(EC.element_to_be_clickable(FIRST_ADD_BUTTON))
    add_button.click()
    
    # Espera a que aparezca el badge en el carrito
    wait.until(EC.visibility_of_element_located(CART_BADGE))
    wait.until(EC.text_to_be_present_in_element(CART_BADGE, "1"))
    return product_name


def go_to_cart_and_get_names(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    driver.find_element(*CART_LINK).click()
    wait.until(EC.url_contains(CART_URL_FRAGMENT))
    wait.until(EC.visibility_of_element_located(CART_ITEM))
    return [el.text for el in driver.find_elements(*FIRST_PRODUCT_NAME)]