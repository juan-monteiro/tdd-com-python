import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        # Satisfeita, ela volta a dormir.
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

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
        time.sleep(1)
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # Ainda continua havendo uma caixa de texto convidando-a a acrescentar outro
        # item. Ela insere "Use peacock feathers to make a fly" (usar penas de pavão
        # para fazer um fly - Edith é bem metódica).
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use the peacock feathres to make it fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A página é atualizada novamente e agora mostra os dois itens em duas lista.
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use the peacock feathres to make it fly")

        # Edith se pergunta se o site lembrará de sua lista. Então ela nota que o
        # site gerou um URL único para ela -- há um pequeno texto explicativo para isso.
        self.fail("Finish the test!")

        # Ela acessa esse URL - sua lista de tarefas continua lá.
