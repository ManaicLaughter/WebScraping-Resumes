# Import required packages.

import requests
import csv
from bs4 import BeautifulSoup
import urllib.request

urls=[]
for i in range (1,12):
	#URL of the website from which data will scraped
    URL='https://www.myvisajobs.com/CV/Candidates.aspx?P='+str(i)     
    page= requests.get(URL)
    html=page.content
    soup=BeautifulSoup(html,'html.parser')
    ab=soup.prettify()
    for b_tag in soup.find_all("b"):
        a_tag = b_tag.find('a')
        urls.append('https://www.myvisajobs.com'+a_tag.attrs['href'])
#Since I need data of 100 employees only. I will eliminate data of extra last 4 employees 
for i in range (0,4):
    urls.pop()

#Create headings for CSV files in which respective data will be stored.
row_list = [["SN", "Name", "Degree", "Career Level","Skills","Goal","Membership","Certification"]]


count = 0
for url in urls:
    single_user = []
    count = count + 1
    page1 = requests.get(url)
    html1 = page1.content
    soup1 = BeautifulSoup(html1,'html.parser')

    #Statements for extracting respective features from website table.

    #find() helps to locate our data using html elements like <span>, <td> etc and associated text in the bracket helps algorithm
    #to identify which <span>, <td> etc are we talking about for extracting data.

    #text() tells the program that we need text or string data.

    #Since I need to extract data present inside the heading. After using [find()] for locating element title.
    #find_next() is used to tell algorithm that I need data present in the next <td>.

    #Get names
    name = soup1.body.find("span", itemprop="name").text
    #Get Degree
    degree = soup1.body.find('td', text='Degree: ').find_next('td').text
    #Get Career Level
    career_level = soup1.body.find('td', text='Career Level: ').findNext('td').text
    #Get Skills
    skills = soup1.body.find('td', text='Skills: ').findNext('td').text
     
    #Here I have tried exception handling because as you manually go profiles present on the website
    #You will observe that many profile lack certain features.[For eg: Some might not have membershp details while some doesn't have
    #skills detail.] To handle this issue I have added exception code. On finding any profile with certain absent feature. The
    #algorithm will skip that feature for that particular profile.
    try:

        goal = soup1.body.find_all('td', text='Goal: ')
        for td in goal:
        	t = td.find_all_next('td', limit=1)
        	row = [i.text for i in t]
    	    	
    	
    except NameError:
    	pass

    try:

        membership = soup1.body.find_all('td', text='Membership: ')
        for td in membership:
        	t = td.find_all_next('td', limit=1)
        	mem = [i.text for i in t]
    	    	
    	
    except NameError:
    	pass
    	
    try:

        certification = soup1.body.find_all('td', text='Certification: ')
        for td in certification:
        	t = td.find_all_next('td', limit=1)
        	cert = [i.text for i in t]
    	    	
    	
    except NameError:
    	pass

    
    single_user.append(count)
    single_user.append(name)
    single_user.append(degree)
    single_user.append(career_level)
    single_user.append(skills)
    single_user.append(row)
    single_user.append(mem)
    single_user.append(cert)
    row_list.append(single_user)

print (row_list)
#save data in temp.csv file
with open('D:temp.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)