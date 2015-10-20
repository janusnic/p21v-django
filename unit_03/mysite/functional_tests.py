# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Посетим нашу главную страницу 
        self.browser.get('http://localhost:8000')

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

        # Напечатаем "Купить бочку апельсинов" в поле ввода
        inputbox.send_keys('Купить бочку апельсинов')

        # При нажатии клавиши enter страница изменится и появится пункт 
        # "1: Купить бочку апельсинов" в табличном списке 
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Купить бочку апельсинов' for row in rows),
            "New to-do item did not appear in table"
        )

        # Поле ввода снова содержит приглашение Добавить в список дел
        
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
