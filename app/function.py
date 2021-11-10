#daysは最新の指標が1日前か2日前か、fromRightは日付インデックスから何個右が該当指標か、formatは日付の形式
def GetIndicator(url,fromRight,dateFormat):
    tempIndicator = BeautifulSoup(requests.get(url,headers=headers).text,'html5lib')('td')
    tempIndex = ''
    for index,i in enumerate(tempIndicator):
        if today.strftime('%A')=='Monday' or today.strftime('%A')=='Sunday':
            tempIndex = ''
        elif today.strftime('%A')=='Tuesday' and fourDaysAgo.strftime(dateFormat)==i.get_text():
            tempIndex = index
        elif twoDaysAgo.strftime(dateFormat)==i.get_text():
            tempIndex = index 
    if tempIndex!='':
        return tempIndicator[tempIndex+fromRight].get_text()
    else:
        return ''