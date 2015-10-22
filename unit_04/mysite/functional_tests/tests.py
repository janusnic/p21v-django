# -*- coding:utf-8 -*-

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Посетим нашу главную страницу 
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        # Проверим, содержит ли заголовок страницы фразу 'Сделай сам - Your To-Do list'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Сделай сам - Your To-Do list', header_text)

        # Содержит ли поле ввода приглашение 'Добавить в список дел'?
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Добавить в список дел'
        )
       
        inputbox.send_keys('Купить бочку апельсинов')

        # При нажатии клавиши enter на странице появится новый URL и новый 
        # пункт '1: Купить бочку апельсинов' списка дел

        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/todo/.+')
        self.check_for_row_in_list_table('1: Купить бочку апельсинов')

        
        import time
        time.sleep(10)

        
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сменить колеса Дрону налету')
        inputbox.send_keys(Keys.ENTER)

        # Страница снова обновляется и мы видим новые элементы списка дел
        self.check_for_row_in_list_table('1: Купить бочку апельсинов')
        self.check_for_row_in_list_table('2: Сменить колеса Дрону налету')

        # Пришел новый пользователь на страницу

        ## Мы используем новую сессию для пользователя 
        # чтобы он работал только со своим списком дел
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Новый пользователь зашел на страницу. 
        # На странице находится список дел, которые ему не принадлежат
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить бочку апельсинов', page_text)
        self.assertNotIn('Сменить колеса Дрону налету', page_text)

        # Пользователь Chatlanyn решил добавить новый пукт в список дел 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить гравицапу')
        inputbox.send_keys(Keys.ENTER)

        # Он получает собственный уникальный URL
        chatl_list_url = self.browser.current_url
        self.assertRegex(chatl_list_url, '/todo/.+')
        self.assertNotEqual(chatl_list_url, edith_list_url)

        # Чужой список ему недоступен
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить бочку апельсинов', page_text)
        self.assertIn('Купить гравицапу', page_text)
        
        self.fail('Тест завершен!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
