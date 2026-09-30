from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver


    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    smart_button = (By.CSS_SELECTOR, 'button.round')
    card_comfort = (By.XPATH, '//div[contains(@class, "tariff-picker")]//div[text()="Comfort"]')
    phone_button = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    next_button_phone = (By.XPATH, "//button[text()='Siguiente']")
    code_input = (By.ID, 'code')
    confirm_code_button = (By.XPATH, "//button[text()='Confirmar']")
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.CLASS_NAME, 'pp-plus-container')
    card_number_input = (By.ID, 'number')
    cvv_input = (By.XPATH, "//input[@id='code' and @placeholder='12']")
    link_card_button = (By.XPATH, "//button[text()='Agregar']")
    close_payment_modal_button = (By.XPATH, "//div[@class='payment-picker open']//button[@class='close-button section-close']")
    comment_input = (By.ID, 'comment')
    blanket_switch = (By.XPATH, "//span[@class='slider round']")
    ice_cream_plus_button = (By.XPATH, "//div[contains(text(), 'Helado')]/..//div[@class='counter-plus']")
    ice_cream_count = (By.XPATH, "//div[contains(text(), 'Helado')]/..//div[@class='counter-value']")
    order_button = (By.CLASS_NAME, 'smart-button-main')
    driver_modal = (By.CLASS_NAME, 'order-body')


    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        to_input = self.driver.find_element(*self.to_field)
        to_input.send_keys(to_address)
        to_input.send_keys(Keys.ENTER)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_smart_button(self):
        # Hace clic estándar en el botón "Pedir un taxi"
        button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.smart_button)
        )
        button.click()

    def select_card_comfort(self):
        card = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.card_comfort)
        )
        card.click()

    def is_comfort_selected(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.card_comfort)
        )
        parent_card = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'tcard')]")
        return "active" in parent_card.get_attribute("class")

    def click_phone_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.phone_button)).click()

    def set_phone(self, phone_number):
        phone_field = self.driver.find_element(*self.phone_input)
        phone_field.send_keys(phone_number)

    def click_next_phone(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.next_button_phone)).click()

    def set_code(self, code):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.code_input)).send_keys(code)

    def click_confirm_code(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.confirm_code_button)).click()

    def click_payment_method(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.payment_method_button)).click()

    def click_add_card(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_card_button)).click()

    def set_card(self, card_number, cvv):
        number_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.card_number_input)
        )
        number_field.send_keys(card_number)

        cvv_field = self.driver.find_element(*self.cvv_input)
        cvv_field.send_keys(cvv)
        cvv_field.send_keys(Keys.TAB)

    def click_link_card(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.link_card_button)).click()

    def close_payment_modal(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.close_payment_modal_button)).click()

    def is_card_added(self):
        payment_text = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.payment_method_button)).text
        return "Tarjeta" in payment_text or "Card" in payment_text

    def set_comment(self, comment):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.comment_input)).send_keys(comment)

    def get_comment(self):
        return self.driver.find_element(*self.comment_input).get_property('value')

    def click_blanket_switch(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.blanket_switch)).click()

    def is_blanket_selected(self):
        switch_input = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Manta')]/..//input")
        return switch_input.is_selected()

    def add_ice_cream(self, count=2):
        plus_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ice_cream_plus_button))
        for _ in range(count):
            plus_btn.click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ice_cream_count).text)

    def click_order_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.order_button)).click()

    def is_driver_info_displayed(self):
        element = WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located(self.driver_modal))
        return element.is_displayed()