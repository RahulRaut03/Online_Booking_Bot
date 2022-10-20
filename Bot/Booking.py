import os
from selenium import webdriver                                  #import webdriver class
from selenium.webdriver.common.by import By
import Bot.constants as const                        # import constants.py file as const
from Bot.Booking_Filterations import BookingFilteration          #import Booking Filteration class here
from Bot.Booking_Report import BookingReport
from prettytable import PrettyTable             #to view data in better way
import pandas as pd                             #to convert data in csv file
import os


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\Users\Rahul\PycharmProjects\SeleniumCourse\chromedriver_win32", teardown=False):
        self.driver_path = driver_path       #provide the path for driver
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()     #create the instance of chromeoptions
        options.add_experimental_option('excludeSwitches', ['enable-logging'])       #used to ignore unwanted warnings and errors appearing on command line while executing the program
        super(Booking, self).__init__(options=options)     #instantaite the instance of chrome driver
        self.implicitly_wait(15)            #wait for 15 secs for the screen loads properlu
        self.maximize_window()              #maximize the window


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()     #close the chrome browser

    def land_first_page(self):
        self.get(const.Base_URL)    #taking url from Contants.py

    def change_currency(self, currency=None):
        currency_ele = self.find_element(By.CSS_SELECTOR, "button[data-tooltip-text = 'Choose your currency']")
        currency_ele.click()        #clicking on currency
        selected_cur_ele = self.find_element(By.CSS_SELECTOR, f"a[data-modal-header-async-url-param *= 'selected_currency={currency}']")
        selected_cur_ele.click()        #select the currency

    def select_placetogo(self, place_to_go):
        search_field = self.find_element(By.ID, 'ss')
        search_field.clear()            #clear the previous text in search field
        search_field.send_keys(place_to_go) #enter the place you want to go

        first_res = self.find_element(By.CSS_SELECTOR, "li[data-i='0']")
        first_res.click()               #click on the first result which you are getting after clicking on search

    def select_dates(self, check_in_date, check_out_date):
        check_in_ele = self.find_element(By.CSS_SELECTOR, f"td[data-date='{check_in_date}']")
        check_in_ele.click()            #select the check in date
        check_out_ele = self.find_element(By.CSS_SELECTOR, f"td[data-date='{check_out_date}']")
        check_out_ele.click()           #select the check out date


    def select_adults(self, adults=1):
        adult_sel_ele = self.find_element(By.ID, 'xp__guests__toggle')
        adult_sel_ele.click()   #click on adults selection section

        while True:             #execute the loop
            decrease_adult_ele = self.find_element(By.CSS_SELECTOR, 'button[aria-label = "Decrease number of Adults"]')
            decrease_adult_ele.click()          #click on decrease number of adults button
            #if the value of adults reaches 1 then we need to go out of while loop
            adults_val_ele = self.find_element(By.ID, 'group_adults')       #find the locator for value of adults
            val = adults_val_ele.get_attribute('value')       #should give value of adults

            if int(val) == 1:   #when the adults value is 1 then go out of loop
                break

        #find out  the locator of increase adults button
        increase_adult_ele = self.find_element(By.CSS_SELECTOR, 'button[aria-label = "Increase number of Adults"]')

        for i in range(adults-1):           #execute for loop
            increase_adult_ele.click()      #click on increase adults button

    def click_search(self):
        #find out the search button locator
        search_but = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_but.click()              #click on search button

    def apply_filterations(self):       #function for apply filters on search result
        #create the object of BookingFilteration class and pass the chromedriver object to that class
        filteration = BookingFilteration(driver=self)
        #call the functions in BookingFilteration class by the object of that class
        filteration.sort_price_lower_first()    #SORT THE RESULT FROM LOWEST PRICE FIRST
        filteration.apply_star_rating(4, 5)  #passing the multiple values to the function


    def report_results(self):
        #Get the locator of Hotel Boxes which contains all 25 elements
        hotel_boxes_list = self.find_element(By.CSS_SELECTOR, 'div[class="d4924c9e74"]')
        # Pass that locator to new class in the other file
        report = BookingReport(hotel_boxes_list)

        #create the prettytable object to see the table in good format
        table = PrettyTable(
                       field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table_vals = report.pull_deal_box_attributes()      #take the hotel data here
        table.add_rows(table_vals)                          #add hotel data in table
        print(table)                                        #print the table on console
        df = pd.DataFrame(table_vals)                       #create dataframe of the hotel data

        os.makedirs('Scraped Data', exist_ok=True)

        df.to_csv("Scraped Data/Hotel_information_CSV.csv", index=None, index_label=False, header=["Hotel Name", "Hotel Price", "Hotel Score"])

        with pd.ExcelWriter("Scraped Data/Hotel_information_Excel.xlsx") as writer:
            df.to_excel(writer, sheet_name="Data", index=False, header=["Hotel Name", "Hotel Price", "Hotel Score"])








