from time import sleep

import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
from ..items import FairfaxItem

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 


class FairfaxSpider(scrapy.Spider):
    name = 'fairfax_comps'
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
        streetNumber = str(input('Please type in house number: '))
        streetName = str(input('Please type in street: '))
        self.driver = webdriver.Chrome('/Users/DanCassin/Development/scrapy_projects/chromedriver')
        self.driver.get('https://icare.fairfaxcounty.gov/ffxcare/search/commonsearch.aspx?mode=address')
        search_address = self.driver.find_element_by_xpath('//*[(@id = "inpNumber")]').send_keys(streetNumber)
        search_street = self.driver.find_element_by_xpath('//*[(@id = "inpStreet")]').send_keys(streetName + '\ue007')
        sleep(2)

        comp_selector = Selector(text = self.driver.page_source)
        comp_page = self.driver.find_element_by_css_selector('#DTLNavigator_lbNbhdSearchThis span')
        comp_page.click()

        page_total_selector = Selector(text = self.driver.page_source)
        total_pages = ''.join(page_total_selector.css('#ml+ b::text').extract())
        total_pages = int(''.join([i for i in total_pages if i.isdigit()]))

        first_result = self.driver.find_element_by_css_selector('.SearchResults:nth-child(3) td:nth-child(1) div')
        first_result.click()
        sleep(2)

        while FairfaxSpider.current_page <= total_pages:
            profile_selector = Selector(text = self.driver.page_source)
            address = profile_selector.css('#Parcel tr:nth-child(1) .DataletData').css('::text').extract()
            lot_sqft = profile_selector.css('tr:nth-child(7) .DataletData').css('::text').extract()
            sleep(0.5)

            try:
                sales_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(2) span')
            except:
                sales_page = self.driver.find_element_by_css_selector('.sel+ .unsel span')

            sales_page.click()
            sleep(2)
            sales_selector = Selector(text = self.driver.page_source)
            sale_date = sales_selector.css('#datalet_div_0 tr:nth-child(2) .DataletData:nth-child(1)').css('::text').extract()
            sale_amount = sales_selector.css('#datalet_div_0 tr:nth-child(2) .DataletData:nth-child(2)').css('::text').extract()
            sleep(0.5)

            values_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(3) span')
            values_page.click()
            sleep(2)
            values_selector = Selector(text = self.driver.page_source)
            current_land = values_selector.css('#Values tr:nth-child(2) .DataletData').css('::text').extract()
            current_building = values_selector.css('#Values tr:nth-child(3) .DataletData').css('::text').extract()
            sleep(0.5)

            tax_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(4) span')
            tax_page.click()
            sleep(2)
            tax_selector = Selector(text = self.driver.page_source)
            general_fund_taxes = tax_selector.css('body tr:nth-child(4) td:nth-child(3)').css('::text').extract()
            special_tax_dist = tax_selector.css('body tr:nth-child(4) td:nth-child(4)').css('::text').extract()
            sleep(0.5)

            residential_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(5) span')
            residential_page.click()
            sleep(2)
            residential_selector = Selector(text = self.driver.page_source)
            style = residential_selector.css('#datalet_div_1 tr:nth-child(2) .DataletData').css('::text').extract()
            total_basement_area = residential_selector.css('tr:nth-child(6) .DataletData').css('::text').extract()
            bedrooms = residential_selector.css('tr:nth-child(15) .DataletData').css('::text').extract()
            full_baths = residential_selector.css('tr:nth-child(16) .DataletData').css('::text').extract()
            half_baths = residential_selector.css('tr:nth-child(17) .DataletData').css('::text').extract()
            construction_quality = residential_selector.css('tr:nth-child(21) .DataletData').css('::text').extract()
            condition_grade = residential_selector.css('tr:nth-child(22) .DataletData').css('::text').extract()
            sleep(0.5)

            structure_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(8) span')
            structure_page.click()
            sleep(2)
            structure_selector = Selector(text = self.driver.page_source)
            liv_area_sqft = structure_selector.css('#datalet_div_1 tr:nth-child(1) .DataletData').css('::text').extract()
            sleep(0.5)

            #profile page at bottom so it stays as the .sel class for the next page
            profile_page = self.driver.find_element_by_css_selector('#sidemenu .unsel:nth-child(1) span')
            profile_page.click()
            sleep(2)

            next_button = self.driver.find_element_by_css_selector('#DTLNavigator_imageNext')
            next_button.click()
            sleep(1)


            items['address'] = address
            items['lot_sqft'] = lot_sqft
            items['sale_date'] = sale_date
            items['sale_amount'] = sale_amount
            items['style'] = style
            items['total_basement_area'] = total_basement_area
            items['bedrooms'] = bedrooms
            items['full_baths'] = full_baths
            items['half_baths'] = half_baths
            items['construction_quality'] = construction_quality
            items['condition_grade'] = condition_grade
            items['general_fund_taxes'] = general_fund_taxes
            items['special_tax_dist'] = special_tax_dist
            items['current_land'] = current_land
            items['current_building'] = current_building
            items['liv_area_sqft'] = liv_area_sqft
            
            yield items

            FairfaxSpider.current_page+=1
            


        
