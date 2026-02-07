import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

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
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

# Métodos y localizadores de la prueba 1
class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def wait_for_load_page(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.from_field))

# Métodos y localizadores de la prueba 2
class UrbanRoutesModes:
    flash_mode = (By.XPATH, '//*[contains(text(), "Flash")]')
    taxi_button = (By.XPATH, '//*[contains(text(),"Pedir un taxi")]')
    confort_rate = (By.XPATH, '//*[contains(text(), "Comfort")]')

    def __init__(self, driver):
        self.driver = driver

    def clic_flash_mode_button(self):
        self.driver.find_element(*self.flash_mode).click()

    def clic_taxi_button(self):
        self.driver.find_element(*self.taxi_button).click()

    def clic_confort_rate_button(self):
        self.driver.find_element(*self.confort_rate).click()

    def wait_for_load_page_mode(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.flash_mode))

    def wait_for_load_rate_mode(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.confort_rate))

    def verification_mode_buttons(self):
        taxi = self.driver.find_element(*self.taxi_button)
        assert taxi.get_attribute("type") == 'button', f'Se espera que sea tipo "button", pero se obtuvo {taxi.get_attribute("type")}'
        confort_text = self.driver.find_element(*self.confort_rate).text
        assert confort_text == 'Comfort', 'El texto del botón no coincide con "Comfort"'

# Métodos y localizadores de la prueba 3
class UrbanRoutesPhone:
    phone_button = (By.CLASS_NAME, 'np-text')
    phone_field = (By.ID, 'phone')
    next_button = (By.XPATH, '//*[contains(text(), "Siguiente")]')
    code_field = (By.ID, 'code')
    confirm_button = (By.XPATH, '//*[contains(text(), "Confirmar")]')

    def __init__(self, driver):
        self.driver = driver

    def clic_phone_button(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)

    def get_phone(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def clic_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def set_code(self, confirmation_code):
        self.driver.find_element(*self.code_field).send_keys(confirmation_code)

    def get_code(self):
        return self.driver.find_element(*self.code_field).get_property('value')

    def clic_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def wait_for_load_number_dialog(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.phone_field))

    def wait_for_load_code_dialog(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.code_field))

    def verification_phone_buttons(self):
        phone = self.driver.find_element(*self.phone_button)
        assert phone.get_attribute("class") == 'np-text', f'Se espera que la clase sea "np-text", pero se obtuvo {phone.get_attribute("class")}'
        next = self.driver.find_element(*self.next_button)
        assert next.get_attribute("type") == 'submit', f'Se espera que sea tipo "submit", pero se obtuvo {next.get_attribute("type")}'
        confirm = self.driver.find_element(*self.confirm_button)
        assert confirm.get_attribute("type") == 'submit', f'Se espera que sea tipo "submit", pero se obtuvo {confirm.get_attribute("type")}'

# Métodos y localizadores de la prueba 4
class UrbanRoutesCard:
    card_button = (By.CLASS_NAME, 'pp-text')
    add_card_button = (By.XPATH, '//*[contains(text(), "Agregar tarjeta")]')
    card_field = (By.ID, 'number')
    code_field = (By.NAME, 'code')
    area_click = (By.CLASS_NAME, 'card-second-row')
    add_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    close_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')

    def __init__(self, driver):
        self.driver = driver

    def clic_card_button(self):
        self.driver.find_element(*self.card_button).click()

    def clic_add_card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def set_card(self, card_number):
        self.driver.find_element(*self.card_field).send_keys(card_number)

    def get_card(self):
        return self.driver.find_element(*self.card_field).get_property('value')

    def set_code(self, code_number):
        self.driver.find_element(*self.code_field).send_keys(code_number)

    def get_code(self):
        return self.driver.find_element(*self.code_field).get_property('value')

    def clic_on_other_area(self):
        self.driver.find_element(*self.area_click).click()

    def clic_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def clic_close_button(self):
        self.driver.find_element(*self.close_button).click()

    def wait_for_load_method_dialog(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.add_card_button))

    def wait_for_load_card_dialog(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.card_field))

    def verification_card_buttons(self):
        card_text = self.driver.find_element(*self.card_button).text
        assert card_text == 'Método de pago', 'El texto del botón no coincide con "Método de pago"'
        add_card = self.driver.find_element(*self.add_card_button)
        assert add_card.get_attribute("class") == 'pp-title', f'Se espera que la clase sea "pp-title", pero se obtuvo {add_card.get_attribute("class")}'
        area = self.driver.find_element(*self.area_click)
        assert (area.get_attribute("class") == 'card-second-row'), f'Se espera que la clase sea "card-second-row", pero se obtuvo {area.get_attribute("class")}'
        button_add = self.driver.find_element(*self.add_button)
        assert button_add.get_attribute("type") == 'submit', f'Se espera que sea tipo "submit", pero se obtuvo {button_add.get_attribute("type")}'
        button_close = self.driver.find_element(*self.close_button)
        assert (button_close.get_attribute("class") == 'close-button section-close'), f'Se espera que la clase sea "close-button section-close", pero se obtuvo {button_close.get_attribute("class")}'

# Métodos y localizadores de la prueba 5
class UrbanRoutesMessage:
    message_field = (By.ID, 'comment')

    def __init__(self, driver):
        self.driver = driver

    def set_message(self, message_text):
        self.driver.find_element(*self.message_field).send_keys(message_text)

    def get_message(self):
        return self.driver.find_element(*self.message_field).get_property('value')

    def wait_for_load_message_page(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.message_field))

# Métodos y localizadores de la prueba 6
class UrbanRoutesSwitch:
    dropdown_list = (By.XPATH, '//*[contains(text(), "Requisitos del pedido")]')
    blank_hand_switch = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')

    def __init__(self, driver):
        self.driver = driver

    def clic_blank_hand_switch(self):
        self.driver.find_element(*self.blank_hand_switch).click()

    def wait_for_load_switch_page(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.dropdown_list))

    def verification_dropdown_list(self):
        dropdown_text = self.driver.find_element(*self.dropdown_list).text
        assert dropdown_text == 'Requisitos del pedido', 'El texto del encabezado no coincide con "Requisitos del pedido"'
        switch = self.driver.find_element(*self.blank_hand_switch)
        assert (switch.get_attribute("class") == 'slider round'), f'Se espera que la clase sea "slider round", pero se obtuvo {switch.get_attribute("class")}'

# Métodos y localizadores de la prueba 7
class UrbanRoutesIceCream:
    ice_cream_bucket_title = (By.XPATH, '//*[contains(text(), "Cubeta de helado")]')
    ice_cream_counter = (By.CLASS_NAME, 'counter-plus')

    def __init__(self, driver):
        self.driver = driver

    def clic_ice_cream_counter(self):
        self.driver.find_element(*self.ice_cream_counter).click()

    def wait_for_load_counter_page(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.ice_cream_bucket_title))

    def verification_ice_cream_counter(self):
        ice_cream_text = self.driver.find_element(*self.ice_cream_bucket_title).text
        assert ice_cream_text == 'Cubeta de helado', 'El texto del encabezado no coincide con "Cubeta de helado"'
        counter_text = self.driver.find_element(*self.ice_cream_counter).text
        assert counter_text == '+', 'El texto del botón no coincide con "+"'

# Métodos y localizadores de la prueba 8
class UrbanRoutesBookTaxi:
    reserve_button = (By.CLASS_NAME, 'smart-button-main')
    look_taxi_title = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver

    def clic_reserve_button(self):
        self.driver.find_element(*self.reserve_button).click()

    def wait_for_load_look_page(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.look_taxi_title))

    def verification_book_buttons(self):
        reserve_text = self.driver.find_element(*self.reserve_button).text
        assert reserve_text == 'Pedir un taxi', 'El texto de la clase no coincide con "Pedir un taxi"'
        look_text = self.driver.find_element(*self.look_taxi_title).text
        assert look_text == 'Buscar automóvil', 'El texto de la clase no coincide con "Buscar automóvil"'

# Métodos y localizadores de la prueba 9
class UrbanRoutesDetails:
    details_button = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[2]/div[1]/div[2]/button/img')
    details_content = (By.CLASS_NAME, 'order-details-content')

    def __init__(self, driver):
        self.driver = driver

    def clic_details_button(self):
        self.driver.find_element(*self.details_button).click()

    def wait_for_load_details_page(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.details_content))

    def verification_details_content(self):
        button_details = self.driver.find_element(*self.details_button)
        assert (button_details.get_attribute("alt") == 'burger'), f'Se espera que alt sea "burger", pero se obtuvo {button_details.get_attribute("alt")}'
        details_content_text = self.driver.find_element(*self.details_content).text
        assert details_content_text == f'{data.address_from}\nLugar de recogida', f'Se espera que el contenido sea "{data.address_from}\nLugar de recogida", pero se obtuvo {details_content_text}'

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
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.wait_for_load_page()
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # Prueba 2, Seleccionar la tarifa "Confort"
    def test_select_confort_rate(self):
        routes_mode = UrbanRoutesModes(self.driver)
        routes_mode.wait_for_load_page_mode()
        routes_mode.clic_flash_mode_button()
        routes_mode.clic_taxi_button()
        routes_mode.wait_for_load_rate_mode()
        routes_mode.clic_confort_rate_button()
        routes_mode.verification_mode_buttons()

    # Prueba 3, Ingresar número de teléfono y recuperar el código de confirmación
    def test_set_phone_number_and_code(self):
        routes_phone = UrbanRoutesPhone(self.driver)
        number_phone = data.phone_number
        routes_phone.clic_phone_button()
        routes_phone.wait_for_load_number_dialog()
        routes_phone.set_phone(number_phone)
        routes_phone.clic_next_button()
        routes_phone.wait_for_load_code_dialog()
        confirm_code = retrieve_phone_code(self.driver)
        routes_phone.set_code(confirm_code)
        routes_phone.clic_confirm_button()
        routes_phone.verification_phone_buttons()
        assert routes_phone.get_phone() == number_phone
        assert routes_phone.get_code() == confirm_code

    # Prueba 4, Ingresar tarjeta de pago y código
    def test_set_pay_card(self):
        routes_card = UrbanRoutesCard(self.driver)
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
        routes_card.verification_card_buttons()
        assert routes_card.get_card() == number_card
        assert routes_card.get_code() == number_code

    # Prueba 5, Ingresar mensaje para el conductor
    def test_set_message(self):
        routes_message = UrbanRoutesMessage(self.driver)
        text_message = data.message_for_driver
        routes_message.wait_for_load_message_page()
        routes_message.set_message(text_message)
        assert routes_message.get_message() == text_message

    # Prueba 6, Habilitar la opción "Manta y pañuelos"
    def test_clic_switch(self):
        routes_switch = UrbanRoutesSwitch(self.driver)
        routes_switch.wait_for_load_switch_page()
        routes_switch.clic_blank_hand_switch()
        routes_switch.verification_dropdown_list()

    # Prueba 7, Pedir 2 helados
    def test_clic_ice_cream_counter(self):
        routes_counter = UrbanRoutesIceCream(self.driver)
        routes_counter.wait_for_load_counter_page()
        routes_counter.clic_ice_cream_counter()
        routes_counter.clic_ice_cream_counter()
        routes_counter.verification_ice_cream_counter()

    # Prueba 8, Pedir un taxi
    def test_clic_reserve_button(self):
        routes_reserve = UrbanRoutesBookTaxi(self.driver)
        routes_reserve.clic_reserve_button()
        routes_reserve.wait_for_load_look_page()
        routes_reserve.verification_book_buttons()

    # Prueba 9, Mostrar la informacion sobre el viaje (opcional)
    def test_clic_details_button(self):
        routes_details = UrbanRoutesDetails(self.driver)
        routes_details.clic_details_button()
        routes_details.wait_for_load_details_page()
        routes_details.verification_details_content()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()