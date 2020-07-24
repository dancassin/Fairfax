# For reference: https://towardsdatascience.com/web-scraping-a-less-brief-overview-of-scrapy-and-selenium-part-ii-3ad290ce7ba1

from time import sleep

import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
from ..items import FairfaxItem

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 


class FairfaxSpider(scrapy.Spider):
    name = 'fairfax'
    start_urls = ['https://icare.fairfaxcounty.gov/ffxcare/search/commonsearch.aspx?mode=address']
    current_page = 1
    
    def parse(self, response):
        items = FairfaxItem()

        self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--incognito")
        options.add_argument("--disable-extensions")
        options.add_argument(" --disable-gpu")
        options.add_argument(" --disable-infobars")
        options.add_argument(" -–disable-web-security")
        options.add_argument("--no-sandbox") 		
        caps = options.to_capabilities()
        streetName = str(input('Please type in street: '))
        self.driver = webdriver.Chrome('/Users/DanCassin/Development/scrapy_projects/chromedriver')
        self.driver.get('https://icare.fairfaxcounty.gov/ffxcare/search/commonsearch.aspx?mode=address')
        search_city = self.driver.find_element_by_xpath('//*[(@id = "inpStreet")]').send_keys(streetName + '\ue007')
        sleep(2)

        page_total_selector = Selector(text = self.driver.page_source)
        total_pages = ''.join(page_total_selector.css('#ml+ b::text').extract())
        total_pages = int(''.join([i for i in total_pages if i.isdigit()]))

        first_result = self.driver.find_element_by_css_selector('.SearchResults:nth-child(3) td:nth-child(1) div')
        first_result.click()
        sleep(2)

        while FairfaxSpider.current_page <= total_pages:
            address_selector = Selector(text = self.driver.page_source)
            address = address_selector.css('#Parcel tr:nth-child(1) .DataletData').css('::text').extract()
        
            sales_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(2) span')
            sales_page.click()
            sleep(3)
            sales_selector = Selector(text = self.driver.page_source)
            sale_date = sales_selector.css('#datalet_div_0 tr:nth-child(2) .DataletData:nth-child(1)').css('::text').extract()
            sale_amount = sales_selector.css('#datalet_div_0 tr:nth-child(2) .DataletData:nth-child(2)').css('::text').extract()

            values_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(3) span')
            values_page.click()
            sleep(3)
            values_selector = Selector(text = self.driver.page_source)
            current_land = values_selector.css('#Values tr:nth-child(2) .DataletData').css('::text').extract()
            current_building = values_selector.css('#Values tr:nth-child(3) .DataletData').css('::text').extract()

            tax_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(4) span')
            tax_page.click()
            sleep(2)
            tax_selector = Selector(text = self.driver.page_source)
            #general_fund_taxes = tax_selector.css('body tr:nth-child(4) td:nth-child(3)').css('::text').extract()
            special_tax_dist = tax_selector.css('body tr:nth-child(4) td:nth-child(4)').css('::text').extract()
            sleep(0.5)

            #profile page at bottom so it stays as the .sel class for the next page
            profile_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(1) span')
            profile_page.click()
            sleep(2)

            next_button = self.driver.find_element_by_css_selector('#DTLNavigator_imageNext')
            next_button.click()
            sleep(1)

            items['address'] = address
            items['sale_date'] = sale_date
            items['sale_amount'] = sale_amount
            items['general_fund_taxes'] = general_fund_taxes
            items['special_tax_dist'] = special_tax_dist
            items['current_land'] = current_land
            items['current_building'] = current_building
            
            yield items

            FairfaxSpider.current_page+=1
            


        
