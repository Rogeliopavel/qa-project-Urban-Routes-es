from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

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
