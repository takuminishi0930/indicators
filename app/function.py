import requests
from bs4 import BeautifulSoup
import pandas
import PyPDF2
import re
import urllib.request
import os
import datetime
import os

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
today = datetime.date.today()
oneWeekAgo = datetime.date.today()-datetime.timedelta(days=7)

#daysは最新の指標が1日前か2日前か、fromRightは日付インデックスから何個右が該当指標か、formatは日付の形式
def GetIndicator(url,fromRight,dateFormat):
    tempIndicator = BeautifulSoup(requests.get(url,headers=headers).text,'html5lib')('td')
    tempIndex = ''
    for index,i in enumerate(tempIndicator):
        if oneWeekAgo.strftime('%A')=='Saturday' or oneWeekAgo.strftime('%A')=='Sunday':
            tempIndex = ''
        elif oneWeekAgo.strftime(dateFormat)==i.get_text():
            tempIndex = index
            break
    if tempIndex!='':
        return tempIndicator[tempIndex+fromRight].get_text()
    else:
        return ''

def GetDollarYenEuroYen():
    Bank_of_Japan = BeautifulSoup(requests.get('https://www.boj.or.jp/statistics/market/forex/fxdaily/index.htm/',headers=headers).text,'html5lib')
    if oneWeekAgo.strftime('%A')=='Saturday' or oneWeekAgo.strftime('%A')=='Sunday':
        partURL=''
    else:
        partURL = str(re.findall('/statistics/market/forex/fxdaily/fxlist/fx{}.pdf'.format(oneWeekAgo.strftime('%y%m%d')),str(Bank_of_Japan))).strip('[]\'')
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
    if os.path.exists('static/csv/{}.csv'.format(oneWeekAgo.strftime('%Y-%m')))==True:
        csv = pandas.read_csv('static/csv/{}.csv'.format(oneWeekAgo.strftime('%Y-%m')),index_col=0,dtype=str)
        if oneWeekAgo.strftime('%A')=='Saturday' or oneWeekAgo.strftime('%A')=='Sunday':
            csv.at['{}'.format(oneWeekAgo),'日経平均'] = ''
            csv.at['{}'.format(oneWeekAgo),'当行株価'] = ''
            csv.at['{}'.format(oneWeekAgo),'NYダウ'] = ''
            csv.at['{}'.format(oneWeekAgo),'対米ドル'] = ''
            csv.at['{}'.format(oneWeekAgo),'対ユーロ'] = ''
            csv.at['{}'.format(oneWeekAgo),'日本国債10年'] = ''
            csv.at['{}'.format(oneWeekAgo),'米国国債10年'] = ''
            csv.at['{}'.format(oneWeekAgo),'WTI先物期近物'] = ''
        else:
            csv.at['{}'.format(oneWeekAgo),'日経平均'] = nikkeiStockAverage
            csv.at['{}'.format(oneWeekAgo),'当行株価'] = iyoginStockAverage
            csv.at['{}'.format(oneWeekAgo),'NYダウ'] = nyDow
            csv.at['{}'.format(oneWeekAgo),'対米ドル'] = dollarYen
            csv.at['{}'.format(oneWeekAgo),'対ユーロ'] = euroYen
            csv.at['{}'.format(oneWeekAgo),'日本国債10年'] = japaneseGovernmentBonds10
            csv.at['{}'.format(oneWeekAgo),'米国国債10年'] = usGovernmentBonds10 
            csv.at['{}'.format(oneWeekAgo),'WTI先物期近物'] = WTI
        csv.to_csv('static/csv/{}.csv'.format(oneWeekAgo.strftime('%Y-%m')))
    else:
        columns = ['日付','日経平均','当行株価','NYダウ','対米ドル','対ユーロ','日本国債10年','米国国債10年','WTI先物期近物']
        df = pandas.DataFrame(data=[[oneWeekAgo,nikkeiStockAverage,iyoginStockAverage,nyDow,dollarYen,euroYen,japaneseGovernmentBonds10,usGovernmentBonds10,WTI]],columns=columns)
        df.to_csv('static/csv/{}.csv'.format(oneWeekAgo.strftime('%Y-%m')),index=False)
