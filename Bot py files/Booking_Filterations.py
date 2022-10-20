#This file will include a class with instance methods.
#That will be responsible to interact with our website
#After we have some results, to apply filters
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver       #import webdriver




class BookingFilteration:                   #create the class
    def __init__(self, driver:WebDriver):   #d
        self.driver = driver                #create the driver variable for this class


    def apply_star_rating(self, *star_vals): # * is used to take multiple values in same variable

        #locate the star rating filter box
        star_filter_box = self.driver.find_element(By.XPATH, '//*[@id="left_col_wrapper"]/div[2]/div/div/div[2]/div[6]')
        #create a list containing all the tags of that star rating filter box
        star_child_ele = star_filter_box.find_elements(By.CSS_SELECTOR, '*')
        #print(len(star_child_ele))


        for star_val in star_vals:          #execute for loop for all passed values
            for star_ele in star_child_ele: #iterate through all the elements in star_child_ele
                if str(star_ele.get_attribute('innerHTML')).strip()  == f'{star_val} stars':
                    star_ele.click()        #click on checkbox of the rating if the values are matched



    def sort_price_lower_first(self):
        #click on sort by option
        sort_ele = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        sort_ele.click()
        self.driver.implicitly_wait(15)
        #click on Price (Lowest First) option
        price_lowest_ele = self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]')
        price_lowest_ele.click()




