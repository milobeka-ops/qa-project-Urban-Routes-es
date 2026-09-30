from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import data
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    driver = None

    def setup_method(self):
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()  # <-- Súper importante para evitar ocultamiento de elementos
        self.driver.implicitly_wait(10)
        self.driver.execute_cdp_cmd('Network.enable', {})

    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()
        assert routes_page.is_comfort_selected()

    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()
        routes_page.click_phone_button()
        routes_page.set_phone(data.phone_number)
        routes_page.click_next_phone()
        code = retrieve_phone_code(self.driver)
        routes_page.set_code(code)
        routes_page.click_confirm_code()

    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()
        routes_page.click_payment_method()
        routes_page.click_add_card()
        routes_page.set_card(data.card_number, data.card_code)
        routes_page.click_link_card()
        routes_page.close_payment_modal()
        assert routes_page.is_card_added()

    def test_write_driver_comment(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()
        routes_page.set_comment(data.message_for_driver)
        assert routes_page.get_comment() == data.message_for_driver

    def test_order_blanket_and_tissues(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()
        routes_page.click_blanket_switch()
        assert routes_page.is_blanket_selected()

    def test_order_two_ice_creams(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()
        routes_page.add_ice_cream(2)
        assert routes_page.get_ice_cream_count() == 2

    def test_order_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_smart_button()
        routes_page.select_card_comfort()

        routes_page.click_phone_button()
        routes_page.set_phone(data.phone_number)
        routes_page.click_next_phone()
        code = retrieve_phone_code(self.driver)
        routes_page.set_code(code)
        routes_page.click_confirm_code()

        routes_page.click_payment_method()
        routes_page.click_add_card()
        routes_page.set_card(data.card_number, data.card_code)
        routes_page.click_link_card()
        routes_page.close_payment_modal()

        routes_page.set_comment(data.message_for_driver)
        routes_page.click_blanket_switch()
        routes_page.add_ice_cream(2)
        routes_page.click_order_button()
        assert routes_page.is_driver_info_displayed()