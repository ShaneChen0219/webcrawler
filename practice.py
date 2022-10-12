from os import times
import numpy as np
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import jsons
import pandas as pd

class webcrawler():
    def __init__(self,url):
        self.url = url
        self.record_str = []

    def __call__(self):
        # Banned from the website
        header = {"User-Agent":"Chrome/41.0.2227.0"}
        # Get the html architecture
        req_html = requests.get(self.url,headers = header).text #每個動作都是一種request 有分get單向傳去網站sever跟post雙向有輸入條件 然後轉為text
        bs4_html = BeautifulSoup(req_html,"html.parser") #爬蟲常用套件BeautifulSoup 把HTML讀成Dictionary(parameter, 原始格式)
        # find the result box
        result = bs4_html.find(id="__next")
        tbody = result.find_all("tbody")
        stock_per_day = tbody[1].find_all("tr")
        for items in stock_per_day:
            item = items.find_all("td")
            times = item[0].find("time").text #.text是取<a> </a> .get()是取class裡面的值
            # time = datetime.fromtimestamp(float(item[0].get("datetime")))
            # time_str = datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
            price = float(item[1].text)
            open = float(item[2].text)
            high = float(item[3].text)
            low = float(item[4].text)
            vol = str(item[5].text)
            change = item[6].text


            #print(time,price,open,high,low,vol,change)
            
            #self.record_str.append({'time':time_str,'price':price,'open':open,'high':high,'low':low,'vol':vol,'change':change})
            self.record_str.append([times,price,open,high,low,vol,change])

        result = self.list2json(self.record_str)
        return self.record_str   

    def time_filter(self,time_start,time_end):
        """
            input: string. the standard is YYYYMMDDHH.
        """
        start = datetime.strptime(time_start,"%Y%m%d%H")
        end = datetime.strptime(time_end,"%Y%m%d%H")
        time_f = [] 

        for stock in self.record_str:
            if datetime.strptime(stock[0],'%Y-%m-%d %H:%M:%S') >= start and datetime.strptime(stock[0],'%Y-%m-%d %H:%M:%S') <= end:
                time_f.append(stock)
    
        return self.list2json(time_f)

    def list2json(self,list):
        json_list = jsons.dumps(list)
        return json_list

    def excel(self,a):
        df = pd.DataFrame(a)
        return df



    
if __name__ == "__main__":
     #執行__init__(這是預設的)
     ss = webcrawler(url="https://cn.investing.com/equities/tesla-motors-historical-data") 
     #執行__call__(這是預設的)
     web = ss()
    #  print(web)
    #  time = ss.time_filter("2022070100","2022072000")
    #  print(time)
     df = pd.DataFrame(web)
     writer = pd.ExcelWriter("TEST.xlsx")
     df.to_excel(writer)
     writer.save()

    #  toexcel1 = pd.ExcelWriter("TEST.xlsx")
    #  web.to_excel()
