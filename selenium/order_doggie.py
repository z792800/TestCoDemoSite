from selenium import selenium
import unittest, time, re

class order_doggie(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://ws6.test-rig.com:7080")
        self.selenium.start()
    
    def test_order_doggie(self):
        sel = self.selenium
        sel.open("/petstoreWeb/shop/Controller.jpf")
        sel.click("link=Sign In")
        sel.wait_for_page_to_load("30000")
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Dogs")
        sel.wait_for_page_to_load("30000")
        sel.click("link=K9-CW-01")
        sel.wait_for_page_to_load("30000")
        sel.click("xpath=(//a[contains(text(),'Add to Cart')])[2]")
        sel.wait_for_page_to_load("30000")
        sel.type("name={actionForm.cart.lineItems[0].quantity}", "3")
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")
        sel.click("css=#Netui_Form_0 > a > img")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Proceed to Checkout")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("$465.87", sel.get_text("css=b > span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("K9-CW-01", sel.get_text("xpath=//td[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Adult Female", sel.get_text("xpath=//td[3]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Continue")
        sel.wait_for_page_to_load("30000")
        time.sleep(10)
        sel.select_window("null")
        sel.click("name=wlw-radio_button_group_key:{actionForm.order.billingAddress}")
        sel.click("name=wlw-radio_button_group_key:{actionForm.order.shippingAddress}")
        sel.click("link=Continue")
        sel.wait_for_page_to_load("30000")
        sel.type("name={actionForm.order.creditCard}", "1212121212121212")
        sel.type("name={actionForm.order.exprDate}", "08/16")
        sel.click("link=Continue")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("901 San Antonio Road", sel.get_text("xpath=//table[@id='orderTable']/tbody/tr[7]/td[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("901 San Antonio Road", sel.get_text("xpath=//table[@id='orderTable']/tbody/tr[7]/td[3]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("3", sel.get_text("xpath=//table[@id='orderTable']/tbody/tr[14]/td/table/tbody/tr[2]/td[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("$465.87", sel.get_text("xpath=//table[@id='orderTable']/tbody/tr[14]/td/table/tbody/tr[3]/td/b/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Continue")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Thank you, your order has been submitted.", sel.get_text("css=b"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Adult Female", sel.get_table("css=table.tableborder.1.1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Sign Out")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
