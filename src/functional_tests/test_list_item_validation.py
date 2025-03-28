from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )
        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys("purchase  milk")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table("1: purchase milk")
        
        
        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # She receives a similar warning on the list page
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")  
        )
        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys("make tea")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table("2: make tea")
        
    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table("1: Buy wellies")

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        # self.wait_for(
        #     lambda: self.assertEqual(
        #         self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
        #         "You've already got this in your list",
        #     )
        # )
    
    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Banter too thick")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table("1: Banter too thick")
        self.get_item_input_box().send_keys("Banter too thick")
        self.get_item_input_box().send_keys(Keys.ENTER)
        # self.wait_for(  
        #     lambda: self.assertTrue(  
        #         self.browser.find_element(
        #             By.CSS_SELECTOR, ".invalid-feedback"
        #         ).is_displayed()  
        #     )
        # )

        # She starts typing in the input box to clear the error
        #self.get_item_input_box().send_keys("a")

        # She is pleased to see that the error message disappears
        # self.wait_for(
        #     lambda: self.assertFalse(
        #         self.browser.find_element(
        #             By.CSS_SELECTOR, ".invalid-feedback"
        #         ).is_displayed()  
        #     )
        # )