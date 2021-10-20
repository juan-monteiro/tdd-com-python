from .base import FunctionalTests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTests):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith ouviu falar de uma nova aplicação online interessante para
        # lista de tarefas. Ela decide verificar sua homepage.
        self.browser.get(self.live_server_url)

        # Ela percebe que o título da pagina e o cabeçalho mencionam listas de
        # tarefas (to-do)
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente.
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # Ela digita "Buy peacock feathers" (Comprar penas de pavão) em uma caixa
        # de texto (o hobby de Edith é fazer iscas para pesca com fly)
        inputbox.send_keys("Buy peacock feathers")

        # Quando ela teclar enter, a página é atualizada, e agora a página lista
        # "1: Buy peakock feathers" como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy peacock feathers")

        # Ainda continua havendo uma caixa de texto convidando-a a acrescentar outro
        # item. Ela insere "Use peacock feathers to make a fly" (usar penas de pavão
        # para fazer um fly - Edith é bem metódica).
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use the peacock feathres to make it fly")
        inputbox.send_keys(Keys.ENTER)

        # A página é atualizada novamente e agora mostra os dois itens em duas lista.
        self.wait_for_row_in_table("1: Buy peacock feathers")
        self.wait_for_row_in_table("2: Use the peacock feathres to make it fly")

        # Satisfeita, ela volta a dormir

    def test_multiple_users_can_start_list_at_different_urls(self):
        # Edith inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        intputbox = self.browser.find_element_by_id("id_new_item")
        intputbox.send_keys("Buy peacock feathers")
        intputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy peacock feathers")

        # Ela percebe que sua lista tem um URL único
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Agora um novo usuário, Francis, chega ao site.

        ## Eusamos uma nova sessão do navegador para garantir que nenhuma informação
        ## de Edith está vindo de cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox(options=self.options)

        # Francis acessa a página inicial. Não há nenhum sinal da lista de Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Fracins inicia uma nova lista inserido um item novo. Ele
        # é menos interessante que Edith...

        intputbox = self.browser.find_element_by_id("id_new_item")
        intputbox.send_keys("Buy milk")
        intputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy milk")

        # Francis obtém seu próprio URL exclusivo
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Novamente, não há nenhum sinal da lista de Edith
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfeitos, ambos voltam a dormir
