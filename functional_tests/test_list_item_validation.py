from .base import FunctionalTests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTests):
    def test_cannot_add_empty_list_items(self):
        # Edith acessa a página inicial e acidentalmente tenta submeter
        # um item vazio na lista. Ela tecla Enter na caixa de entrada vazia
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # O navegador impede e não carrega a página
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid").text
        )

        # Ela tenta novamente com um texto para o item, e o erro desaparece
        self.get_item_input_box().send_keys("Buy milk")
        self.wait_for(
            lambda: self.browser.find_elements(By.CSS_SELECTOR, "#id_text:valid")
        )

        # E finalmente ela pode enviar o formulário
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy milk")

        # De forma perversa, ela gora decide submeter um segundo item em
        # branco na lista
        self.get_item_input_box().send_keys(Keys.ENTER)

        # E novamente o navegador a impede
        self.wait_for_row_in_table("1: Buy milk")
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid").text
        )

        # E ela pode corrigir isso preenchendo o item com um texto
        self.get_item_input_box().send_keys("Make tea")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy milk")
        self.wait_for_row_in_table("2: Make tea")

    def test_cannot_add_dublicate_items(self):
        # Edith vai na página inicial e começa uma nova lista
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy wellies")

        # Ela acidentalmente tenta adicionar um item duplicado
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Ela vê uma mensagem de erro
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You've already got this in your list",
            )
        )
