import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time

MAX_WAIT = 5

class NewVisitorTest(LiveServerTestCase):  
    def setUp(self):  
        self.browser = webdriver.Firefox()  

    def tearDown(self):  
        self.browser.quit()

    def wait_for_now_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try: 
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() -start_time > MAX_WAIT:
                    raise
                time.sleep(0.05)

    def test_can_start_a_todo_list(self):  
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)  

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)  
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID,"id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
        
        #she types "buy peacock feathers" into a text box
        #(edith's hobby is tying fly-fishing lures)
        inputbox.send_keys("buy peacock feathers")

        #when she hits enter, the page updates and now the page lists
        #"1: buy peacock feathers" as abn item in a to-do list table
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_now_in_list_table("1: buy peacock feathers")

        #there is stilla text box inviting her to add another item
        #she enters "use peacock feathers to make a fly"
        #(edith is very methodical)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_now_in_list_table("1: buy peacock feathers")
        self.wait_for_now_in_list_table("2: use peacock feathers to make a fly")

        #self.fail("Finish the test!")  

        [...]

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_list_at_different_urls(self):
        #edith starta new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table("1: buy peacock feathers")

        #she notices that her list has a unique url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        #we delete all the browsers cookies
        self.browser.delete_all_cookies()

        #francis visits the home page there is no sigh of ediths list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        #francis starts a new list by entering a new item, he is less interesting than edith
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table("1: buy milk")

        #francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        #again there is no trace of ediths list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("buy peacock feathers", page_text)
        self.assertIn("buy milk", page_text)

if __name__ == "__main__":  
    unittest.main() 