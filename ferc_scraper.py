import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
import os
from tkinter import *
import tkinter as tk
import datetime as dt

tod = dt.datetime.today()
theDate = "{}/{:02d}/{}".format(tod.month, tod.day, tod.year)
download_link = "https://elibrary.ferc.gov/idmws"
path = r'downloaded_emails/'

class WritableStringVar(tk.StringVar):
    def write(self, added_text):
        new_text = self.get() + added_text
        self.set(new_text)

    def clear(self):
        self.set("")
class BrickSetSpider(scrapy.Spider):
    name = "ferc_spider"
    start_urls = ['https://elibrary.ferc.gov/idmws/search/fercgensearch.asp']

    def parse(self, response):
        query = FormRequest.from_response(response,
                                          formdata={
                                              "FROMdt": theDate,
                                              "TOdt": theDate,
                                              "firstDt": "1/1/1904",
                                              "LastDt": "12/31/2017",
                                              "DocsStart": "0",
                                              "DocsLimit": "200",
                                              "SortSpec": "filed_date desc accession_num asc",
                                              "datefield": "filed_date",
                                              "dFROM": theDate,
                                              "dTO": theDate,
                                              "dYEAR": "1",
                                              "dMONTH": "1",
                                              "dDAY": "1",
                                              "date": "between",
                                              "NotCategories": "submittal, issuance",
                                              "category": "submittal",
                                              "libraryall": "",
                                              "library": "oil",
                                              "docket": "",
                                              "subdock_radio": "all_subdockets",
                                              "class": "999",
                                              "type": "Tariff Filing",
                                              "textsearch": "",
                                              "description": "description",
                                              "fulltext": "fulltext",
                                              "DocsCount": "200"
                                          },
        callback=self.parse_query)
        yield query

    def parse_query(self, response):
        print ('in parse_query')
        page_rows = response.xpath('//tr[@bgcolor and not(@bgcolor="navy")]').extract()
        popup = False
        pop_items = []
        for row in page_rows:
            sel = Selector(text=row)
            columns = sel.xpath('body/tr/td').extract()
            sel3 = Selector(text = columns[3])
            column3 = sel3.xpath("//*[not(name()='a')]/text()").extract()
            sel4 = Selector(text=columns[4])
            column4 = sel4.xpath("//*[not(name()='a')]/text()").extract()
            description = [element.replace("\r\n", "") for element in column3 if element.replace("\r\n", "") != ""]
            name = description[0].split(" submits ")[0]

            sel5 = Selector(text=columns[5])
            column5_link = download_link + sel5.xpath("//a/@href").extract()[-1].replace("..","")

            fileid = column5_link.split('=')[1]
            fold = path + name
            uniq_path = fold + '/' + fileid + ".pdf"
            if os.path.isdir(fold):
                if not os.path.exists(uniq_path):
                    urllib.request.urlretrieve(column5_link, uniq_path)
                    popup = True
                    #pop_items += pop_items + name + '_' + fileid + "/n "
                    pop_items.append(name + '_' + fileid)
            else:
                os.mkdir(fold)
                urllib.request.urlretrieve(column5_link, fold + '/' + fileid + ".pdf")
                popup = True
                #pop_items += pop_items + name + '_' + fileid + "/n "
                pop_items.append(name + '_' + fileid)

        if popup:
            root = Tk()
            root.configure(background='light blue')
            root.title("New Files")
            root.geometry("350x450")

            textvar = WritableStringVar(root)
            label = tk.Label(root, textvariable=textvar)
            label.pack()
            for item in pop_items:
                print(item, file=textvar)
            root.mainloop()
