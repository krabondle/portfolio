import requests
import time
import json
from bs4 import BeautifulSoup
import requests
import csv

PTT_URL = 'https://www.ptt.cc'

def get_web_page(url):
    resp = requests.get(url=url,cookies={'over18':'1'})
    print(resp.status_code)
    if resp.status_code !=200:
        print('Invalid url:',resp.url)
        return  None
    else:
        return resp.text

def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html.parser')

    
    paging_div = soup.find('div','btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []  
    divs = soup.find_all('div','r-ent')
    for d in divs:
        if d.find('div','date').text.strip() == date: 
            
            push_count =0
            push_str =d.find('div','nrec').text
            if push_str:
                try:
                    push_count = int(push_str)    
                except ValueError:
                    

                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = 0

            
            if d.find('a'):     
                href = d.find('a')['href']
                title = d.find('a').text
                author = d.find('div','author').text if d.find('div','author') else ''
                articles.append({
                    'title': title,
                    'href' : href,
                    'push_count': push_count,
                    'author' : author
                })
    return articles, prev_url

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg['title'] +' author : ' +msg['author'] + ' link :' + PTT_URL+msg['href']}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    print(r)
    return r.status_code


token = 'gmYJmYxzqAIULnsw2uLUPP3cPzi0JzJUENnMwLky28f'
token2 = 'Ov3SNysBDbFpzZpD6MwvCdU2HSNNCUwDpQuymk5PFrD'
token3 = 'VrvmWjOp783iaH6mFhMpVCKiRWoUFuQOvzWoEUOVPqn'
token4 = 'bnMFrS2DhFswk0RQFu2LAt0e8tIX99cHldyQSqkmaRw'
token5 = 'Flx1DRjj6QFR65HCR0fG0rSwUQzW6Y5HomnmxL42DfW'

try:
    with open('/fadachai/record.csv') as csvfile:
        reader =  csv.reader(csvfile)
        x = list(reader)
        save = x[0]
except:
    save = []
    pass

while True:
    try :
        current_page = get_web_page(PTT_URL + '/bbs/Stock/index.html')
        if current_page:
            articles = [] 
            
            today = time.strftime("%m/%d").lstrip('0')
            
            current_articles, prev_url = get_articles(current_page, today)
            
            while  current_articles:
                articles += current_articles
                current_page =get_web_page(PTT_URL + prev_url)
                current_articles, prev_url =get_articles(current_page, today)
            
            # print('今天有',len(articles),'篇文章')
            threshold = -99
            # print('熱門文章(> %d 推):' %(threshold))
            
            #print('articles : ' + str(len(articles)))
            for a in articles:
                if a['author'] in ['gggping','zesonpso','Sunrisesky','aitt','j9771909','aqsw2000','d94425140','gn01765288','drgon'] or (a['push_count'] > 30 and a['title'].find('其他') != -1) or (a['push_count'] > 30 and a['title'].find('新聞') != -1) or (a['push_count'] > 60 and a['title'].find('心得') != -1):
                    #print('a ' + str(a))
                    if a['href'] not in save :
                        #print('b ' + str(a))
                        save.append(a['href'])
                        # print(save)
                        with open('/fadachai/record.csv', 'w') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(save)
                        lineNotifyMessage(token, a)
                        lineNotifyMessage(token2, a)
                        lineNotifyMessage(token3, a)
                        lineNotifyMessage(token4, a)
                        lineNotifyMessage(token5, a)
    except :
        pass
    finally:
        time.sleep(5)
