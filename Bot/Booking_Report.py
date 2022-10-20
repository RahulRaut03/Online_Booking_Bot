# This file is going to include to method that will parse
# The specific data that we need from each one the deal boxes
from selenium.webdriver.remote.webelement import WebElement       #import webdriver
from selenium.webdriver.common.by import By


class BookingReport:

    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        #call to below function
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        #this will return the list of 25 hotels from the search box
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR, 'div[class="a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942"]')


    def pull_deal_box_attributes(self):
        collection = []  # create a list
        for deal_box in self.deal_boxes:
            # #Pull the hotel name
            hotel_name = deal_box.find_element(By.CSS_SELECTOR,
                                               'div[data-testid="title"]').get_attribute('innerHTML').strip()
            #print(hotel_name)
            #pull the hotel price
            hotel_price = deal_box.find_element(By.CSS_SELECTOR,
                                                 'span[class="fcab3ed991 bd73d13072"]').get_attribute('innerHTML').strip()


            if 'nbsp' in hotel_price:
                hotel_price = hotel_price[0] +  hotel_price[7:]

            # print(hotel_price)
            #pull the hotel Score
            hotel_score = deal_box.find_element(By.CSS_SELECTOR,
                                                 'div[class="b5cd09854e d10a6220b4"]').get_attribute('innerHTML').strip()
            #print(hotel_score)
            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )
        return collection



