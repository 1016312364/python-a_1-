from bs4 import BeautifulSoup
import urllib.request as u
import requests
from datetime import datetime
import requests
import random
from bs4 import BeautifulSoup
import smtplib,time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
def getWeather():
    response = requests.get('http://www.weather.com.cn/weather1d/101280101.shtml#dingzhi_first')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'html.parser')
    #print(soup)
    tagToday = soup.find('p',class_="tem")
    try:
        temperatureHigh=tagToday.span.string
    except AttributeError:
        temperatureHigh=tagToday.find_next('p', class_="tem").span.string.replace('℃','')
    finally:
        a =[]
        temperatureLow=tagToday.span.string.replace('℃','')
        for ul in soup.find_all('p',class_="tem"):
            a.append(ul.span.string)
        temperatureHigh =a[0]
        temperatureLow = a[1]
        #print(temperatureLow)
        weather=soup.find('p', class_="wea").string
        tagWind=soup.find('p',class_="win")
        winL=tagWind.span.string
        today = datetime.now()
        today = str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日'
        content =( '早安! 亲~\n'+\
                  '今天是:  '+today+'\n'+\
                  '广州温度:  '+temperatureLow+'℃-'+temperatureHigh+'℃\n'+\
                  '天气:  '+weather+'\n'+\
                  '风级:  '+winL)
        return content
print(getWeather())
def getlloverwords():
    texts = []
    for i in range(1,70):
        url = 'https://www.duanwenxue.com/huayu/tianyanmiyu/list_{}.html'.format(i)
        response = requests.get(url)
        #response.encoding = 'utf-8'
        #soup = BeautifulSoup(response.text,'html.parser')
        #print(soup)
        texts.append(response.text)
        #print(texts)
    articles = []
    #print(texts)
    for text in texts:
        #print(text)
        soup = BeautifulSoup(text,'html.parser')
        #print(soup)
        arttis = soup.find('div', class_='list-short-article').ul.li.p.find_all('a', {'target': "_blank"})  # 寻找情话内容
        #  通过列表推导式以及for循环获取到每个a标签里面的text内容并通过strip去除空格
        #print(arttis)
        articles.extend([arttis[i].text.strip() for i in range(len(arttis))])
    todaywords = articles[random.randint(0, len(articles)-1)]   # 随机选取其中一条情话
    return todaywords
print(getlloverwords())
def _format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))
def sendemail(toaddr='',message=''):
    fromaddr = 'aaa'
    password = 'aaaj'
    smtp_server = 'aaa'
    msg = MIMEText(message,'plain','utf-8')
    msg['From'] = _format_addr('亲亲<%s>'%fromaddr)
    msg['To'] = _format_addr('亲亲<%s>'%toaddr)
    msg['Subject'] = Header('每日晨间问候','utf-8').encode()
    server = smtplib.SMTP(smtp_server,25)
    server.set_debuglevel(1)
    server.login(fromaddr,password)
    server.sendmail(fromaddr,[toaddr],msg.as_string())
    server.quit()
    return
def dailymorning():
    message = getWeather()+'\n'+\
              '今日份的土味情话:\n'+\
              getlloverwords()
    sendemail(toaddr='lijianjun1393@gmail.com',message = message)
    
if __name__ == '__main__':
    dailymorning()
