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
                self.assertIn("row_text", [row.text for row in rows])
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


if __name__ == "__main__":  
    unittest.main() 