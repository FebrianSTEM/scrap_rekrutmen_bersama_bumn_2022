from html.parser import HTMLParser
from bs4 import BeautifulSoup
import scrapy
import json
import gspread # for connection to google sheet


class QuotesSpider(scrapy.Spider):
    name = "job_bumn"

    ITEM_PIPELINES = {
        'fhcibumn.pipelines.FhcibumnPipeline': 300,
    }

    def start_requests(self):
        url = "https://rekrutmenbersama.fhcibumn.id/job/loadRecord/"
        yield scrapy.Request(url=url, method="GET", callback=self.parse)

    def parse(self, response):
        '''
            forgot how to write desc so 
            bare me for a while
            response : 

            return json 

        '''
        json_response = json.loads(response.text)
        jobs = json_response["data"]["result"]

        result = {}
        header_sheet = ["Perusahaan","Pekerjaan","Pendidikan","Category Perkerjaan","Requirement","Link Pendaftaran", "Created"]

        gc = gspread.service_account(filename='credential.json')
        sheet = gc.open('Daftar Vacancy Rekrutment Bersama BUMN 2022').sheet1
        sheet.clear()
        sheet.append_row(header_sheet)

        for job in jobs:
            url_detail = f'https://rekrutmenbersama.fhcibumn.id/job/detail/{job["vacancy_id"]}'
            result = job
            result["job_url_detail"] = url_detail
            yield scrapy.Request(url  = url_detail, method="GET", callback=self.parse_job, 
                                meta = result)

    def parse_job(self, response):
        '''
            response

            return html file of detail job page

            yield : expeceted json
        '''

        result = response.meta
        soup = BeautifulSoup(response.body)
        job_requirement = soup.find("div", {"class": "col-md-12 mt-0"}).text
        result["job_requirement"] = job_requirement
        
        yield result;