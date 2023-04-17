"""This script serves as an example on how to use Python 
   & Playwright to scrape/extract data from Google Maps"""
   
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse


@dataclass
class Business:
    """holds business data
    """
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None

@dataclass
class BusinessList:
    """holds list of Business objects, 
       and save to both excel and csv
    """
    business_list : list[Business] = field(default_factory=list)
    
    def dataframe(self):
        """transform business_list to pandas dataframe 

        Returns: pandas dataframe
        """
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="_")
    
    def save_to_excel(self, filename):
        """saves pandas dataframe to excel (xlsx) file

        Args:
            filename (str): filename
        """   
        self.dataframe().to_excel(f'{filename}.xlsx', index=False)
    
    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """
        self.dataframe().to_csv(f'{filename}.csv', index=False)


def main():
    
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto('https://www.google.com/maps', timeout=60000)
        # wait is added for dev phase. can remove it in production
        page.wait_for_timeout(5000)
        
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)
        
        page.keyboard.press('Enter')
        page.wait_for_timeout(5000)
        
        #################  
        ### scrolling ###
        #################
        page.hover('(//div[@role="article"])[1]')
        # If you needed more data, change 7 by a bigger number
        for i in range(7): 
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)
        
        listings = page.locator('//div[@role="article"]').all()
        
        business_list = BusinessList()
        
        # getting first five only
        for listing in listings[:5]:
        
            listing.click()
            page.wait_for_timeout(5000)
            
            name_xpath = '//h1[contains(@class, "fontHeadlineLarge")]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            
            business = Business()
            business.name = page.locator(name_xpath).inner_text()
            business.address = page.locator(address_xpath).inner_text()
            business.website = page.locator(website_xpath).inner_text()
            business.phone_number = page.locator(phone_number_xpath).inner_text()
                        
            business_list.business_list.append(business)
        
        # saving to both excel and csv just to showcase the features.
        business_list.save_to_excel('google_maps_data')
        business_list.save_to_csv('google_maps_data')
        
        browser.close()
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-l", "--location", type=str)
    args = parser.parse_args()
    
    if args.location and args.search:
        search_for = f'{args.search}  {args.location}'
    else:
        # in case no arguments passed:
        # scraper will search for this on Google Maps
        search_for = 'dentist new york'
        
    main()