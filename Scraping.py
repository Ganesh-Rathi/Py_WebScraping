from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd


c_names = []
c_addr = []
c_webaddr = []
c_emailaddr = []
c_code = []
c_ContactNumber = []
c_TPOname = []
c_TPOnumber = []
c_district = []


region = ['Amravati', 'Aurangabad' , 'Mumbai', 'Nagpur', 'Nashik', 'Pune']

for i in range(6):
    page_link = "http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=" + str(i+1) + "&RegionName=" + region[i]



    page = requests.get(page_link)

    soup = BeautifulSoup(page.content,'html.parser')

    table = soup.find('table',{"class": "DataGrid"})

    college_tags = table.findChildren('td')

    link_tags = []
    links = []
    i = 3

    while True:
        if(i<=len(college_tags)):
            name = college_tags[i].text
            if "Engineering" in name or "Technology" in name or "Technical" in name or "Technological" in name:
                link_tags.append(college_tags[i-1])
        else:
            break

        i = i + 3


    print(link_tags)

    for tag in link_tags:
        a_tag = tag.find('a',{'href': re.compile("^frm")})
        links.append('http://dtemaharashtra.gov.in/' + a_tag.get('href'))




    for link in links:

        college = requests.get(link)


        soup = BeautifulSoup(college.content,'html.parser')
        print(soup)

        college_details = soup.find('table',{'class':'AppFormTable'})

        name_details = college_details.find('span',{"id": "ctl00_ContentPlaceHolder1_lblInstituteNameEnglish"})
        addr_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblAddressEnglish"})
        district_details = college_details.find('span', {"id" : "ctl00_ContentPlaceHolder1_lblDistrict"})
        webaddr_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblWebAddress"})
        email_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblEMailAddress"})
        ContactNum_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblPersonalPhoneNo"}).getText().split()
        TPO_name = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblRegistrarNameEnglish"})
        TPO_number = college_details.find('span',{"id": "ctl00_ContentPlaceHolder1_lblOfficePhoneNo"}).getText().split()

        if name_details.text!="" and addr_details.text!="" and district_details.text!="" and webaddr_details.text!="" and email_details.text!="" and ContactNum_details[0].isnumeric() and TPO_name.text!="" and TPO_number[0].isnumeric():

            c_names.append(name_details.text)
            c_addr.append(addr_details.text)
            c_district.append(district_details.text)
            c_webaddr.append(webaddr_details.text)
            c_emailaddr.append(email_details.text)
            c_ContactNumber.append(ContactNum_details[0])
            c_TPOname.append(TPO_name.text)
            c_TPOnumber.append(TPO_number[0])



college_data = {'College Name':c_names,'Address':c_addr, 'District':c_district ,'Website':c_webaddr, 'Email address':c_emailaddr, 'Contact Number': c_ContactNumber, 'TPO name': c_TPOname, 'TPO contact number':c_TPOnumber}


df = pd.DataFrame(college_data)

print(df)

df.to_csv('clgs.csv', index = False, header=True)





############visualization################################################




import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.read_csv("clgs.csv")

print(df)

fig1 ,ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

Region = df.groupby('Region').count()['College Name']

ax1.pie(Region, labels=Region.index , autopct='%1.1f%%')
ax1.set_title('No. of Colleges Region wise.')

Auto_By_Region = df.groupby(['Region','Autonomous Status']).count()['College Name']

auto = []
non_auto = []
print(type(Auto_By_Region))
for i in range(len(Auto_By_Region)):
    if(i%2==0):
        auto.append(Auto_By_Region[i])
    else:
        non_auto.append(Auto_By_Region[i])

print(auto, non_auto)

x = np.arange(len(Region.index))
width = 0.35

rect1 = ax2.bar(x - width/2, auto, width, label='Auto')
rect2 = ax2.bar(x + width/2, non_auto, width, label='Non Autonomous')
ax2.legend()
ax2.set_xticks(x)
ax2.set_xticklabels(Region.index)
ax2.set_ylabel('No. of Colleges')
ax2.set_title('No. of Autonmous and non-Autonomous per Region')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax2.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rect1)
autolabel(rect2)

fig2.tight_layout()
plt.show()

















































