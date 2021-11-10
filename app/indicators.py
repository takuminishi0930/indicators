import requests
from bs4 import BeautifulSoup
import pandas
import PyPDF2
import re
import urllib.request
import os
import datetime

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
today = datetime.date.today()
yesterday = datetime.date.today()-datetime.timedelta(days=1)
twoDaysAgo = datetime.date.today()-datetime.timedelta(days=2)
threeDaysAgo = datetime.date.today()-datetime.timedelta(days=3)
fourDaysAgo = datetime.date.today()-datetime.timedelta(days=4)

#daysは最新の指標が1日前か2日前か、fromRightは日付インデックスから何個右が該当指標か、formatは日付の形式
def GetIndicator(url,days,fromRight,dateFormat):
    tempIndicator = BeautifulSoup(requests.get(url,headers=headers).text,'html5lib')('td')
    tempIndex = ''
    for index,i in enumerate(tempIndicator):
        if days==1:
            if today.strftime('%A')=='Saturday' or today.strftime('%A')=='Sunday':
                tempIndex = ''
            elif today.strftime('%A')=='Monday' and threeDaysAgo.strftime(dateFormat)==i.get_text():
                tempIndex = index
            elif yesterday.strftime(dateFormat)==i.get_text():
                tempIndex = index
        elif days==2:
            if today.strftime('%A')=='Monday' or today.strftime('%A')=='Sunday':
                tempIndex = ''
            elif today.strftime('%A')=='Tuesday' and threeDaysAgo.strftime(dateFormat)==i.get_text():
                tempIndex = index
            elif twoDaysAgo.strftime(dateFormat)==i.get_text():
                tempIndex = index 
    if tempIndex!='':
        return tempIndicator[tempIndex+fromRight].get_text()
    else:
        return ''

nikkeiStockAverage = str(GetIndicator('https://s.minkabu.jp/stock/100000018/daily_bar',1,4,'%Y/%m/%d')).replace(',','')
iyoginStockAverage = str(re.findall('\d{3}',GetIndicator('https://s.minkabu.jp/stock/8385/daily_bar',1,4,'%Y/%m/%d'))).strip('[]\'')
nyDow = str(GetIndicator('https://nikkeiyosoku.com/nydow/data/',2,4,'%Y/%m/%d')).replace(',','')
japaneseGovernmentBonds10 = GetIndicator('https://www.bb.jbts.co.jp/ja/historical/main_rate.html',1,4,'%Y/%m/%d')
usGovernmentBonds10 = GetIndicator('https://irbank.net/usa/10year',2,1,'%m/%d')
WTI = GetIndicator('https://jp.investing.com/commodities/crude-oil-historical-data',2,1,'%Y年%m月%d日')

Bank_of_Japan = BeautifulSoup(requests.get('https://www.boj.or.jp/statistics/market/forex/fxdaily/index.htm/',headers=headers).text,'html5lib')
partURL = str(re.findall('/statistics/market/forex/fxdaily/fxlist/fx{}.pdf'.format(yesterday.strftime('%y%m%d')),str(Bank_of_Japan))).strip('[]\'')
if partURL!='':
    URL = 'https://www.boj.or.jp'+partURL
    urllib.request.urlretrieve(URL,str(re.findall('fx\d{6}.pdf',URL)))
    with open(str(re.findall('fx\d{6}.pdf',URL)),'rb') as f:
        result = re.findall('\d{3}[.]\d{2}[-]\d{2}',PyPDF2.PdfFileReader(f).getPage(0).extractText())
    if today.strftime('%A')!='Sunday' and today.strftime('%A')!='Saturday':
        dollarYen = result[2]
        euroYen = result[3]
    else:
        dollarYen = ''
        euroYen = ''
    os.remove(str(re.findall('fx\d{6}.pdf',URL)))
else:
        dollarYen = ''
        euroYen = ''
    
csv = pandas.read_csv('static/csv/indicators.csv',index_col=0,dtype=str)
if today.strftime('%A')=='Monday':
    csv.at['{}'.format(threeDaysAgo),'日経平均'] = nikkeiStockAverage
    csv.at['{}'.format(threeDaysAgo),'当行株価'] = iyoginStockAverage
    csv.at['{}'.format(threeDaysAgo),'対米ドル'] = dollarYen
    csv.at['{}'.format(threeDaysAgo),'対ユーロ'] = euroYen
    csv.at['{}'.format(threeDaysAgo),'日本国債10年'] = japaneseGovernmentBonds10
    csv.to_csv('static/csv/indicators-backup.csv')
elif today.strftime('%A')=='Tuesday':
    csv.at['{}'.format(fourDaysAgo),'NYダウ'] = nyDow
    csv.at['{}'.format(fourDaysAgo),'米国国債10年'] = usGovernmentBonds10
    csv.at['{}'.format(fourDaysAgo),'WTI先物期近物'] = WTI
else:
    csv.at['{}'.format(yesterday),'日経平均'] = nikkeiStockAverage
    csv.at['{}'.format(yesterday),'当行株価'] = iyoginStockAverage
    csv.at['{}'.format(twoDaysAgo),'NYダウ'] = nyDow
    csv.at['{}'.format(yesterday),'対米ドル'] = dollarYen
    csv.at['{}'.format(yesterday),'対ユーロ'] = euroYen
    csv.at['{}'.format(yesterday),'日本国債10年'] = japaneseGovernmentBonds10
    csv.at['{}'.format(twoDaysAgo),'米国国債10年'] = usGovernmentBonds10 
    csv.at['{}'.format(twoDaysAgo),'WTI先物期近物'] = WTI
csv.to_csv('static/csv/indicators.csv')
