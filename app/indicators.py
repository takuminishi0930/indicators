from function import *

nikkeiStockAverage = str(GetIndicator('https://s.minkabu.jp/stock/100000018/daily_bar',4,'%Y/%m/%d')).replace(',','')
iyoginStockAverage = GetIndicator('https://s.minkabu.jp/stock/8385/daily_bar',4,'%Y/%m/%d')
nyDow = str(GetIndicator('https://nikkeiyosoku.com/nydow/data/',4,'%Y/%m/%d')).replace(',','')
japaneseGovernmentBonds10 = GetIndicator('https://www.bb.jbts.co.jp/ja/historical/main_rate.html',4,'%Y/%m/%d')
usGovernmentBonds10 = GetIndicator('https://irbank.net/usa/10year',1,'%m/%d')
WTI = GetIndicator('https://jp.investing.com/commodities/crude-oil-historical-data',1,'%Y年%m月%d日')
dollarYen,euroYen = GetDollarYenEuroYen()
csv()
