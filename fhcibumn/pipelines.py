# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import print_function
from datetime import datetime
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import gspread


class FhcibumnPipeline:
    def process_item(self, item, spider):
        print("Start Write to Google Sheet")
        gc = gspread.service_account(filename='credential.json')
        sheet = gc.open('Daftar Vacancy Rekrutment Bersama BUMN 2022').sheet1
        sheet.append_row([item["tenant_name"], item["vacancy_name"], item["jenjang"], item["stream_name"], item["job_requirement"], item["job_url_detail"]])
        print("Finish")
        return item
