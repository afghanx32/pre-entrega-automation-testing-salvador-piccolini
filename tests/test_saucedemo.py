from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    login_as_standard_user,
    add_first_product_to_cart,
    go_to_cart_and_get_names,
    INVENTORY_TITLE,
    APP_LOGO,
    INVENTORY_URL_FRAGMENT,
    CART_BADGE,
    CART_URL_FRAGMENT,
    TIMEOUT,
)


def test_login_exitoso(driver):
    login_as_standard_user(driver)
    wait = WebDriverWait(driver, TIMEOUT)
    assert INVENTORY_URL_FRAGMENT in driver.current_url
    titulo = wait.until(EC.visibility_of_element_located(INVENTORY_TITLE)).text
    assert titulo == "Products"
    logo = wait.until(EC.visibility_of_element_located(APP_LOGO)).text
    assert logo == "Swag Labs"


def test_carrito_agregar_producto(driver):
    login_as_standard_user(driver)
    wait = WebDriverWait(driver, TIMEOUT)
    add_first_product_to_cart(driver)
    badge = wait.until(EC.visibility_of_element_located(CART_BADGE)).text
    assert badge == "1"


def test_carrito_navegar_y_verificar_producto(driver):
    login_as_standard_user(driver)
    expected_name = add_first_product_to_cart(driver)
    cart_names = go_to_cart_and_get_names(driver)
    assert CART_URL_FRAGMENT in driver.current_url
    assert expected_name in cart_names