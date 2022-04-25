import requests
from bs4 import BeautifulSoup
import pandas
import PyPDF2
import re
import urllib.request
import os
import datetime
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
fiveDaysAgo = datetime.date.today()-datetime.timedelta(days=5)

def GetLatestDay():
    latestDay=0
    for i in os.listdir("./static/csv"):
        date = os.path.splitext(os.path.basename(i))[0]
        if latestDay==0 or latestDay<date:
            latestDay = date
    csv = pd.read_csv("static/csv/{}.csv".format(latestDay),index_col=0)
    csv.index
    latestDay=0
    for i in csv.index:
        if latestDay==0 or latestDay<i:
            latestDay=i
    latestDay = datetime.datetime.strptime(latestDay, '%Y-%m-%d').date()

def GetSearchDay():
    searchDay=[]
    date = fiveDaysAgo
    while date>GetLatestDay():
        searchDay.append(date)
        date = date-datetime.timedelta(days=1)

#daysは最新の指標が1日前か2日前か、fromRightは日付インデックスから何個右が該当指標か、formatは日付の形式
def GetIndicator(url,fromRight,dateFormat,date):
    tempIndicator = BeautifulSoup(requests.get(url,headers=headers).text,'html5lib')('td')
    tempIndex = ''
    for index,i in enumerate(tempIndicator):
        if date.strftime(dateFormat)==i.get_text():
            tempIndex = index 
        break
    if tempIndex!='':
        return tempIndicator[tempIndex+fromRight].get_text()
    else:
        return ''

def GetDollarYenEuroYen():
    Bank_of_Japan = BeautifulSoup(requests.get('https://www.boj.or.jp/statistics/market/forex/fxdaily/index.htm/',headers=headers).text,'html5lib')
    if today.strftime('%A')=='Monday' or today.strftime('%A')=='Sunday':
        partURL=''
    elif today.strftime('%A')=='Tuesday':
        partURL = str(re.findall('/statistics/market/forex/fxdaily/fxlist/fx{}.pdf'.format(fourDaysAgo.strftime('%y%m%d')),str(Bank_of_Japan))).strip('[]\'')
    else:
        partURL = str(re.findall('/statistics/market/forex/fxdaily/fxlist/fx{}.pdf'.format(twoDaysAgo.strftime('%y%m%d')),str(Bank_of_Japan))).strip('[]\'')
    if partURL!='':
        URL = 'https://www.boj.or.jp'+partURL
        urllib.request.urlretrieve(URL,str(re.findall('fx\d{6}.pdf',URL)))
        with open(str(re.findall('fx\d{6}.pdf',URL)),'rb') as f:
            result = re.findall('\d{3}[.]\d{2}[-]\d{2}',PyPDF2.PdfFileReader(f).getPage(0).extractText())
            dollarYen = result[2][:4]+result[2][-2:]
            euroYen = result[3][:4]+result[3][-2:]
        os.remove(str(re.findall('fx\d{6}.pdf',URL)))
    else:
            dollarYen = ''
            euroYen = ''
    return dollarYen,euroYen

def csv(nikkeiStockAverage,iyoginStockAverage,nyDow,dollarYen,euroYen,japaneseGovernmentBonds10,usGovernmentBonds10,WTI):
    if os.path.exists('static/csv/{}.csv'.format(twoDaysAgo.strftime('%Y-%m')))==True:
        csv = pandas.read_csv('static/csv/{}.csv'.format(twoDaysAgo.strftime('%Y-%m')),index_col=0,dtype=str)
        if today.strftime('%A')=='Monday' or today.strftime('%A')=='Sunday':
            csv.at['{}'.format(twoDaysAgo),'日経平均'] = ''
            csv.at['{}'.format(twoDaysAgo),'当行株価'] = ''
            csv.at['{}'.format(twoDaysAgo),'NYダウ'] = ''
            csv.at['{}'.format(twoDaysAgo),'対米ドル'] = ''
            csv.at['{}'.format(twoDaysAgo),'対ユーロ'] = ''
            csv.at['{}'.format(twoDaysAgo),'日本国債10年'] = ''
            csv.at['{}'.format(twoDaysAgo),'米国国債10年'] = ''
            csv.at['{}'.format(twoDaysAgo),'WTI先物期近物'] = ''
        elif today.strftime('%A')=='Tuesday':
            csv.at['{}'.format(twoDaysAgo),'日経平均'] = ''
            csv.at['{}'.format(twoDaysAgo),'当行株価'] = ''
            csv.at['{}'.format(twoDaysAgo),'NYダウ'] = ''
            csv.at['{}'.format(twoDaysAgo),'対米ドル'] = ''
            csv.at['{}'.format(twoDaysAgo),'対ユーロ'] = ''
            csv.at['{}'.format(twoDaysAgo),'日本国債10年'] = ''
            csv.at['{}'.format(twoDaysAgo),'米国国債10年'] = ''
            csv.at['{}'.format(twoDaysAgo),'WTI先物期近物'] = ''
            csv.at['{}'.format(fourDaysAgo),'日経平均'] = nikkeiStockAverage
            csv.at['{}'.format(fourDaysAgo),'当行株価'] = iyoginStockAverage
            csv.at['{}'.format(fourDaysAgo),'NYダウ'] = nyDow
            csv.at['{}'.format(fourDaysAgo),'対米ドル'] = dollarYen
            csv.at['{}'.format(fourDaysAgo),'対ユーロ'] = euroYen
            csv.at['{}'.format(fourDaysAgo),'日本国債10年'] = japaneseGovernmentBonds10
            csv.at['{}'.format(fourDaysAgo),'米国国債10年'] = usGovernmentBonds10 
            csv.at['{}'.format(fourDaysAgo),'WTI先物期近物'] = WTI
        else:
            csv.at['{}'.format(twoDaysAgo),'日経平均'] = nikkeiStockAverage
            csv.at['{}'.format(twoDaysAgo),'当行株価'] = iyoginStockAverage
            csv.at['{}'.format(twoDaysAgo),'NYダウ'] = nyDow
            csv.at['{}'.format(twoDaysAgo),'対米ドル'] = dollarYen
            csv.at['{}'.format(twoDaysAgo),'対ユーロ'] = euroYen
            csv.at['{}'.format(twoDaysAgo),'日本国債10年'] = japaneseGovernmentBonds10
            csv.at['{}'.format(twoDaysAgo),'米国国債10年'] = usGovernmentBonds10 
            csv.at['{}'.format(twoDaysAgo),'WTI先物期近物'] = WTI
        csv.to_csv('static/csv/{}.csv'.format(twoDaysAgo.strftime('%Y-%m')))
    else:
        columns = ['日付','日経平均','当行株価','NYダウ','対米ドル','対ユーロ','日本国債10年','米国国債10年','WTI先物期近物']
        df = pandas.DataFrame(data=[[twoDaysAgo,nikkeiStockAverage,iyoginStockAverage,nyDow,dollarYen,euroYen,japaneseGovernmentBonds10,usGovernmentBonds10,WTI]],columns=columns)
        df.to_csv('static/csv/{}.csv'.format(twoDaysAgo.strftime('%Y-%m')),index=False)
