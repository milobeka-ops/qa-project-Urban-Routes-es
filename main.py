import time
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
                if code:
                    return code
        except WebDriverException:
            time.sleep(1)
            continue
        time.sleep(1)

    if not code:
        raise Exception("No se encontró el código de confirmación del teléfono.\n"
                        "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
    return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    smart_button = (By.CLASS_NAME, 'button.round')
    comfort_card = (By.XPATH, "//div[text()='Comfort']")
    phone_button = (By.CLASS_NAME, 'np-text')
    phone_input = (By.ID, 'phone')
    next_button = (By.XPATH, "//button[text()='Siguiente']")
    code_input = (By.ID, 'code')
    confirm_button = (By.XPATH, "//button[text()='Confirmar']")
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.CLASS_NAME, 'pp-plus')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, "//input[@id='code' and @placeholder='12']")
    card_submit_button = (By.XPATH, "//button[text()='Agregar']")
    close_payment_modal_button = (By.XPATH,
                                  "//div[@class='payment-picker open']//button[@class='close-button section-close']")
    driver_comment_input = (By.ID, 'comment')
    blanket_tissue_switch = (By.XPATH,
                             "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div//span[@class='slider round']")
    blanket_tissue_checkbox = (By.XPATH, "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div//input")
    ice_cream_plus_button = (By.XPATH, "//div[@class='r-counter-container']//div[@class='counter-plus']")
    ice_cream_count_value = (By.XPATH, "//div[@class='r-counter-container']//div[@class='counter-value']")
    order_taxi_button = (By.XPATH, "//button[@class='smart-button']//span[contains(text(), 'Pedir un taxi')]")
    driver_modal = (By.CLASS_NAME, 'order-body')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.from_field))
        element.send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_smart_button(self):
        self.driver.find_element(*self.smart_button).click()

    def select_card_comfort(self):
        self.driver.find_element(*self.comfort_card).click()

    def click_phone_button(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone(self, phone_number):
        phone_field = self.driver.find_element(*self.phone_input)
        phone_field.send_keys(phone_number)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def set_code(self, code):
        self.driver.find_element(*self.code_input).send_keys(code)

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_button).text

    def click_payment_method(self):
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card(self):
        self.driver.find_element(*self.add_card_button).click()

    def set_card_number(self, card_number):
        self.driver.find_element(*self.card_number_input).send_keys(card_number)

    def set_card_code(self, card_code):
        card_code_field = self.driver.find_element(*self.card_code_input)
        card_code_field.send_keys(card_code)
        card_code_field.send_keys(Keys.TAB)

    def click_card_submit(self):
        self.driver.find_element(*self.card_submit_button).click()

    def click_close_payment_modal(self):
        self.driver.find_element(*self.close_payment_modal_button).click()

    def get_payment_method_text(self):
        return self.driver.find_element(*self.payment_method_button).text

    def set_driver_comment(self, comment):
        self.driver.find_element(*self.driver_comment_input).send_keys(comment)

    def get_driver_comment(self):
        return self.driver.find_element(*self.driver_comment_input).get_property('value')

    def click_blanket_tissue_switch(self):
        self.driver.find_element(*self.blanket_tissue_switch).click()

    def is_blanket_tissue_selected(self):
        return self.driver.find_element(*self.blanket_tissue_checkbox).is_selected()

    def add_ice_creams(self, count=2):
        plus_btn = self.driver.find_element(*self.ice_cream_plus_button)
        for _ in range(count):
            plus_btn.click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ice_cream_count_value).text)

    def click_order_taxi(self):
        self.driver.find_element(*self.order_taxi_button).click()

    def is_driver_info_displayed(self):
        element = WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located(self.driver_modal))
        return element.is_displayed()

    def is_driver_info_displayed(self):
        element = WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located(self.driver_modal))
        return element.is_displayed()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_card_comfort(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()

    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()
        routes_page.click_phone_button()
        routes_page.set_phone(data.phone_number)
        routes_page.click_next_button()

        time.sleep(1)

        code = retrieve_phone_code(self.driver)

        routes_page.set_code(code)
        routes_page.click_confirm_button()

        assert routes_page.get_phone_number() == data.phone_number

    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()

        routes_page.click_payment_method()
        routes_page.click_add_card()
        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)
        routes_page.click_card_submit()
        routes_page.click_close_payment_modal()

        assert 'Tarjeta' in routes_page.get_payment_method_text()

    def test_comment_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()

        routes_page.set_driver_comment(data.message_for_driver)

        assert routes_page.get_driver_comment() == data.message_for_driver

    def test_order_blanket_and_tissues(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()

        routes_page.click_blanket_tissue_switch()

        assert routes_page.is_blanket_tissue_selected() == True

    def test_add_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()

        routes_page.add_ice_creams(2)

        assert routes_page.get_ice_cream_count() == 2

    def test_order_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()

        # Flujo de teléfono
        routes_page.click_phone_button()
        routes_page.set_phone(data.phone_number)
        routes_page.click_next_button()

        time.sleep(1)

        code = retrieve_phone_code(self.driver)
        routes_page.set_code(code)
        routes_page.click_confirm_button()

        # Pedir taxi
        routes_page.click_order_taxi()

        # Aserción final
        assert routes_page.is_driver_info_displayed() == True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()