import scrapy
from scrapy.utils.response import open_in_browser
from ..items import FairfaxItem


class FairfaxSpider(scrapy.Spider):
    name = 'fairfax_original'
    start_urls = ['https://icare.fairfaxcounty.gov/ffxcare/search/commonsearch.aspx?mode=address']
    streetName = 'Kings Park'
    page = 1

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,formdata={ 
            #'__VIEWSTATE':'/wEPDwUJLTgxMDY5OTM2DxQrAAJkZxYCZg9kFgQCBQ8PFgIeB1Zpc2libGVoZBYCZg9kFgJmD2QWAgIBD2QWAgIBD2QWAgIBDxBkZBYAZAIHDw8WAh8AaGRkZA==',
            #'__EVENTVALIDATION' :'/wEWCAL/k9GbBALq6fr+DwKw9e7KCwKNs9bAAwLYyu+sAwLE8frfBwK5mc2yBwLunJLZAQ==',
            #'PageNum':'',
            #'SortBy':'PARID',
            #'SortDir': 'asc',
            #'PageSize':50,
            'hdAction':'Search',
            #'hdIndex': '',
            #'sIndex':-1,
            #'hdListType':'PA',
            #'hdJur': '', 
            #'inpNumber': '',
            #'inpUnit': '',
            'inpStreet':str(FairfaxSpider.streetName),
            #'inpSuffix1':'',
            #'selSortBy':'PARID' ,
            #'selSortDir': 'asc' ,
            #'selPageSize':50 ,
            #'searchOptions$hdBeta': '',
            'btSearch':'SEARCH',
            'mode':'ADDRESS',
            #'mask': '',
        }, callback=self.start_scraping)
        
        
    def start_scraping(self, response):
        open_in_browser(response)
        total_pages = ''.join(response.css('#ml+ b::text').extract())
        total_pages = int(''.join([i for i in total_pages if i.isdigit()]))
        print(total_pages)
    
        if FairfaxSpider.page == 1:
            #first_page = response.css('.SearchResults:nth-child(3) td:nth-child(1) div').css('::attr(href)')
            #print(f'href link for first page: {first_page}')
            yield response.follow('https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1', callback=self.start_scraping)
            #open_in_browser(response)
        elif FairfaxSpider.page <= total_pages:
            pass

        FairfaxSpider.page+=1
