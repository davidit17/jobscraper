
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 
import sqlite3
from datetime import date
import datetime


# In[13]:


#jobnet
l = []

for num in range(5):
        
        url = "https://www.jobnet.co.il/positionresults.aspx?p="+str(num)+"&subprofid=705" # Cyber 705
        r = requests.get(url)
        c = r.content
        soup=BeautifulSoup(c,"html.parser")
        jobs = soup.find_all("div",{'vocab' : 'http://schema.org/'})
        
        for i in range(len(jobs)) :
            m = {}
            date = jobs[i].find_all("a",{"class":"last"})[0].text.split()[-1] # date
            promoted = 'Yes' if jobs[i].find_all("div",{"class":"jobContainerTop GoldJob"}) else 'No'
            if (date != time.strftime("%d/%m/%Y") and promoted == 'No'): break


            
            m['company'] = jobs[i].find_all("span",{"class":"PositionCompanyName"})[0].text# company
            m['title'] =jobs[i].find_all("a",{"class":"title"})[0].text # title
            m['date'] = date # date
            m['desc'] =jobs[i].find_all("i",{"property":"description"})[0].text# desc
            m['skills'] =jobs[i].find_all("i",{"property":"skills"})[0].text# skills
            m['code'] = jobs[i].find_all("div",{"jobContainerDetails"})[0].find_all("i")[1].text# code
            m['promoted'] = promoted
            l.append(m)

print ("scraped")


# In[14]:


df=pd.DataFrame(l)
df


# In[15]:


promoted = df[df['promoted']=='Yes']
regular = df[df['promoted']=='No']


# In[23]:


#promoted[promoted['date']==time.strftime("%d/%m/%Y")] # only todays promoted 
promoted # active promoted


# In[17]:


regular


# In[24]:


promoted.to_html('promoted.html')
regular.to_html('regular.html')


# In[25]:


import smtplib
import imghdr
from email.message import EmailMessage
import account

EMAIL = account.mail
SENDTO = account.sendto
PASSWORD = account.password

msg = EmailMessage()
msg['Subject'] = 'Promoted job list'
msg['From'] = EMAIL
msg['To'] = SENDTO
msg.preamble = 'Promoted job list'
file ='promoted.html'


with open(file, 'rb') as f:
    attach = f.read()
msg.add_attachment(attach, maintype='text', subtype='html')

with smtplib.SMTP('smtp.mail.com', 587) as s:
    s.login(EMAIL, PASSWORD)
    s.send_message(msg)

