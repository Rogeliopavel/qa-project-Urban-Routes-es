import data
import helpers
import pages
from selenium import webdriver

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import ChromeOptions
        options = ChromeOptions()
        options.set_capability("goog:loggingPrefs",{'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    # Prueba 1, Ingresar direcciones
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = pages.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.wait_for_load_page()
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # Prueba 2, Seleccionar la tarifa "Confort"
    def test_select_confort_rate(self):
        routes_mode = pages.UrbanRoutesModes(self.driver)
        routes_mode.wait_for_load_page_mode()
        routes_mode.clic_flash_mode_button()
        routes_mode.clic_taxi_button()
        routes_mode.wait_for_load_rate_mode()
        routes_mode.clic_confort_rate_button()
        taxi = self.driver.find_element(*pages.UrbanRoutesModes.taxi_button)
        assert taxi.get_attribute("type") == 'button', f'Se espera que sea tipo "button", pero se obtuvo {taxi.get_attribute("type")}'
        confort_text = self.driver.find_element(*pages.UrbanRoutesModes.confort_rate).text
        assert confort_text == 'Comfort', 'El texto del botón no coincide con "Comfort"'

    # Prueba 3, Ingresar número de teléfono y recuperar el código de confirmación
    def test_set_phone_number_and_code(self):
        routes_phone = pages.UrbanRoutesPhone(self.driver)
        number_phone = data.phone_number
        routes_phone.clic_phone_button()
        routes_phone.wait_for_load_number_dialog()
        routes_phone.set_phone(number_phone)
        routes_phone.clic_next_button()
        routes_phone.wait_for_load_code_dialog()
        confirm_code = helpers.retrieve_phone_code(self.driver)
        routes_phone.set_code(confirm_code)
        routes_phone.clic_confirm_button()
        assert routes_phone.get_phone() == number_phone
        assert routes_phone.get_code() == confirm_code
        phone = self.driver.find_element(*pages.UrbanRoutesPhone.phone_button)
        assert phone.get_attribute("class") == 'np-text', f'Se espera que la clase sea "np-text", pero se obtuvo {phone.get_attribute("class")}'
        button_next = self.driver.find_element(*pages.UrbanRoutesPhone.next_button)
        assert button_next.get_attribute("type") == 'submit', f'Se espera que sea tipo "submit", pero se obtuvo {button_next.get_attribute("type")}'
        confirm = self.driver.find_element(*pages.UrbanRoutesPhone.confirm_button)
        assert confirm.get_attribute("type") == 'submit', f'Se espera que sea tipo "submit", pero se obtuvo {confirm.get_attribute("type")}'

    # Prueba 4, Ingresar tarjeta de pago y código
    def test_set_pay_card(self):
        routes_card = pages.UrbanRoutesCard(self.driver)
        number_card = data.card_number
        number_code = data.card_code
        routes_card.clic_card_button()
        routes_card.wait_for_load_method_dialog()
        routes_card.clic_add_card_button()
        routes_card.wait_for_load_card_dialog()
        routes_card.set_card(number_card)
        routes_card.set_code(number_code)
        routes_card.clic_on_other_area()
        routes_card.clic_add_button()
        routes_card.wait_for_load_method_dialog()
        routes_card.clic_close_button()
        assert routes_card.get_card() == number_card
        assert routes_card.get_code() == number_code
        card_text = self.driver.find_element(*pages.UrbanRoutesCard.card_button).text
        assert card_text == 'Método de pago', 'El texto del botón no coincide con "Método de pago"'
        add_card = self.driver.find_element(*pages.UrbanRoutesCard.add_card_button)
        assert add_card.get_attribute("class") == 'pp-title', f'Se espera que la clase sea "pp-title", pero se obtuvo {add_card.get_attribute("class")}'
        area = self.driver.find_element(*pages.UrbanRoutesCard.area_click)
        assert (area.get_attribute("class") == 'card-second-row'), f'Se espera que la clase sea "card-second-row", pero se obtuvo {area.get_attribute("class")}'
        button_add = self.driver.find_element(*pages.UrbanRoutesCard.add_button)
        assert button_add.get_attribute("type") == 'submit', f'Se espera que sea tipo "submit", pero se obtuvo {button_add.get_attribute("type")}'
        button_close = self.driver.find_element(*pages.UrbanRoutesCard.close_button)
        assert (button_close.get_attribute("class") == 'close-button section-close'), f'Se espera que la clase sea "close-button section-close", pero se obtuvo {button_close.get_attribute("class")}'

    # Prueba 5, Ingresar mensaje para el conductor
    def test_set_message(self):
        routes_message = pages.UrbanRoutesMessage(self.driver)
        text_message = data.message_for_driver
        routes_message.wait_for_load_message_page()
        routes_message.set_message(text_message)
        assert routes_message.get_message() == text_message

    # Prueba 6, Habilitar la opción "Manta y pañuelos"
    def test_clic_switch(self):
        routes_switch = pages.UrbanRoutesSwitch(self.driver)
        routes_switch.wait_for_load_switch_page()
        routes_switch.clic_blank_hand_switch()
        dropdown_text = self.driver.find_element(*pages.UrbanRoutesSwitch.dropdown_list).text
        assert dropdown_text == 'Requisitos del pedido', 'El texto del encabezado no coincide con "Requisitos del pedido"'
        switch = self.driver.find_element(*pages.UrbanRoutesSwitch.blank_hand_switch)
        assert (switch.get_attribute("class") == 'slider round'), f'Se espera que la clase sea "slider round", pero se obtuvo {switch.get_attribute("class")}'

    # Prueba 7, Pedir 2 helados
    def test_clic_ice_cream_counter(self):
        routes_counter = pages.UrbanRoutesIceCream(self.driver)
        routes_counter.wait_for_load_counter_page()
        routes_counter.clic_ice_cream_counter()
        routes_counter.clic_ice_cream_counter()
        ice_cream_text = self.driver.find_element(*pages.UrbanRoutesIceCream.ice_cream_bucket_title).text
        assert ice_cream_text == 'Cubeta de helado', 'El texto del encabezado no coincide con "Cubeta de helado"'
        counter_text = self.driver.find_element(*pages.UrbanRoutesIceCream.ice_cream_counter).text
        assert counter_text == '+', 'El texto del botón no coincide con "+"'

    # Prueba 8, Pedir un taxi
    def test_clic_reserve_button(self):
        routes_reserve = pages.UrbanRoutesBookTaxi(self.driver)
        routes_reserve.clic_reserve_button()
        routes_reserve.wait_for_load_look_page()
        reserve_text = self.driver.find_element(*pages.UrbanRoutesBookTaxi.reserve_button).text
        assert reserve_text == 'Pedir un taxi', 'El texto de la clase no coincide con "Pedir un taxi"'
        look_text = self.driver.find_element(*pages.UrbanRoutesBookTaxi.look_taxi_title).text
        assert look_text == 'Buscar automóvil', 'El texto de la clase no coincide con "Buscar automóvil"'

    # Prueba 9, Mostrar la informacion sobre el viaje (opcional)
    def test_clic_details_button(self):
        routes_details = pages.UrbanRoutesDetails(self.driver)
        routes_details.clic_details_button()
        routes_details.wait_for_load_details_page()
        button_details = self.driver.find_element(*pages.UrbanRoutesDetails.details_button)
        assert (button_details.get_attribute("alt") == 'burger'), f'Se espera que alt sea "burger", pero se obtuvo {button_details.get_attribute("alt")}'
        details_content_text = self.driver.find_element(*pages.UrbanRoutesDetails.details_content).text
        assert details_content_text == f'{data.address_from}\nLugar de recogida', f'Se espera que el contenido sea "{data.address_from}\nLugar de recogida", pero se obtuvo {details_content_text}'

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()