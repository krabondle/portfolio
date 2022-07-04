import fitz
import os
# import math
from datetime import datetime
import pandas as pd
current_path = os.listdir(os.getcwd())
uber_path = []
for i in current_path:
    if i.find('receipt') != -1 and i.find('pdf') != -1:
        uber_path.append(i)

amount = []
date = []
Order = []
# pdf_document = "uber-eats-receipt-64b4d26c-8efb-455f-bfbf-373495cb5079.pdf"
for pdf_document in uber_path:
    doc = fitz.open(pdf_document)
    # print ("number of pages: %i" % doc.pageCount)
    # print(doc.metadata)

    page1 = doc.loadPage(0)
    page1text = page1.getText()
    # print(page1text)
    line = page1text.split('\n')

    # print (line)
    dic = {}

    for i in line:
        if i.find('年') != -1 and i.find('月') != -1  and i.find('日') != -1 :
            # print(i)
            dic['date'] = datetime.strptime(i.replace('年','-').replace('月','-').replace('日','').replace(' ',''),"%Y-%m-%d")
        if i.find('訂購的電子明細。') != -1:
            # print(i)
            dic['store'] = i.replace('以下是您在','').replace('訂購的電子明細。','')
    
    if '總計' in line:
        # print(line.index('總計'))
        amount.append(line[line.index('總計')+1].replace('$',''))
        dic['amount'] = line[line.index('總計')+1].replace('$','')
    
    if '小計' in line:
        dic['subtotal'] = line[line.index('小計')+1].replace('$','')

    if '優惠' in line:
        dic['discount'] = line[line.index('優惠')+1].replace('$','')
    
    if '特別優惠' in line:
        dic['special_offer'] = line[line.index('特別優惠')+1].replace('$','')
        
    if '退款' in line:
        if '新的總計' in line:
            amount = line[line.index('新的總計')+1].replace('$','')
            dic['amount'] = line[line.index('新的總計')+1].replace('$','')
        if '退款' in line:
            refund = line[line.index('退款')+1].replace('$','')
            dic['refund'] = line[line.index('退款')+1].replace('$','')
        if '先前總計' in line:
            previous_total = line[line.index('先前總計')+1].replace('$','')
            dic['previous_total'] = line[line.index('先前總計')+1].replace('$','')

    block = []
    details = []
    if '總計' in line and '小計' in line:
        block = line[line.index('總計')+2:line.index('小計')]
        for i in range(len(block)):
            if block[i].isdigit() == True and block[i+2].find('$') != -1:
                # print(block[i+1])
                details.append({'items':block[i+1],'quantity':int(block[i]),'price':float(block[i+2].replace('$',''))})

    dic['detail'] = pd.DataFrame.from_dict(details)

    
    Order.append(dic)

df = pd.DataFrame.from_dict(Order)
try:
    df = df.sort_values('date')
except:
    pass


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',500)
pd.set_option('display.unicode.ambiguous_as_wide', True)


def calculation(x):
    y = x*0.01
    z= x*0.09
    return y,z


dataset = [float(i) for i in df['amount']]
other = [120]
dataset = dataset + other
sum_y = 0
sum_z = 0

for i in dataset:
    y , z = calculation(float(i))
    sum_y += y
    sum_z += z

balance = 300 - sum_z
balance2 = balance/0.09
print('--------------------------------')
print(df.drop(["detail"], axis=1).tail(1))
print('--------------------------------')
print(df['detail'].tail(1))
print('--------------------------------')
print(dataset)
print('其他 : ' + str(other))
# print('退款 : ' + str(refund))
print('--------------------------------')
print('筆數 : ' + str(len(dataset)))
print('消費總和 : ' + str(sum(dataset)))
print('1%回饋總和 : ' + str(int(sum_y)))
print('9%回饋總和 : ' + str(int(sum_z)))
print('全部回饋總和 : ' + str(int(sum_y+sum_z)))
print('剩餘回饋 : ' + str(balance))
print('下一筆最高花費 : ' + str(round(balance2,2)))