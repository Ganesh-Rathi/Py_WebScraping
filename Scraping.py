import requests
import os
import csv
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def selectregion(college):
    data = {'Amravati': '1', 'Aurangabad': '2', 'Mumbai': '3', 'Nagpur': '4', 'Nashik': '5', 'Pune': '6'}
    url = 'http://www.dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=' + data[college] + '&RegionName=' + college
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if (response.status_code != 200):
        print("Access denied")
        return False
    print(college, 'data getting feteched\n')
    soup = BeautifulSoup(response.content, 'html.parser')
    stat_table = soup.find_all('table', class_='DataGrid')
    stat_table = stat_table[0]
    count = 0
    with open('output.txt', 'w') as r:
        for row in stat_table.find_all('tr'):
            o = []
            for cell in row.find_all('td'):
                o.append(cell.text)

            if (len(o) < 2):
                continue

            elif ('technical' in o[2].lower() or 'engineering' in o[2].lower() or 'technological' in o[
                2].lower() or 'institute of technology' in o[2].lower()):
                r.write("    ".join(o))
                r.write('\n')
                count += 1

    return True


def selectcollege(code):
    url = 'http://dtemaharashtra.gov.in/frmInstituteSummary.aspx?InstituteCode=' + str(code)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if (response.status_code != 200):
        return False
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        stat_table = soup.find_all('table', class_='AppFormTable')

        stat_table = stat_table[0]
        with open('output1.txt', 'w') as r:
            for row in stat_table.find_all('tr'):
                for cell in row.find_all('td'):
                    r.write(cell.text.ljust(28))
                r.write('\n')
        file1 = open('output1.txt', 'r')
        Lines = file1.readlines()
        output = ['NULL'] * 11
        flag = 0
        for line in Lines:
            co = list(map(str, line.split()))

            if (len(co) == 2 and co[1] == "Code"):
                return False
            if (len(co) < 3):
                pass

            elif (co[1] == "Code"):
                output[0] = co[2]
            elif (co[1] == "Name"):
                output[1] = ' '.join(co[2:])
            elif (co[0] == "Address"):
                output[2] = ' '.join(co[1:])
            elif (co[0] == 'E-Mail'):
                output[3] = co[2]
            elif (co[0] == 'District'):
                output[4] = ' '.join(co[1:2])
            elif (co[0] == 'Name' and flag == 0):
                output[5] = ' '.join(co[1:])
                flag = 1

            elif (co[0] == "Office"):
                j = 0
                for i in range(len(co)):
                    if (j != 1 and co[i].isdigit() and len(co[i]) > 5):
                        output[6] = co[i]
                        j = 1
                    elif (j == 1 and co[i].isdigit() and len(co[i]) > 5):
                        output[7] = co[i]

            elif (co[0] == 'Name' and flag == 1):
                output[8] = ' '.join(co[1:])
            elif (co[0] == 'Status'):
                for i in range(len(co)):
                    if (co[i] == 'Autonomy'):
                        output[9] = co[i + 2]
                        break
            elif (co[0] == 'Year'):
                output[10] = co[3]
        return output


def recordsofcollege(college_region):
    if (selectregion(college_region)):

        no_of_college = 1
        with open('output.txt', 'r') as f:
            for line in f:
                cpp = list(map(str, line.split()))
                if (len(cpp) < 3):
                    pass
                elif (no_of_college > 180):
                    return
                elif (cpp[0].isdigit() and cpp[1].isdigit() and len(cpp) > 2):
                    o = selectcollege(cpp[1])
                    f = open('output2.txt', 'a+', newline='')
                    f.write('$'.join(o))
                    f.write('\n')
                    f.close()
                    no_of_college += 1

        return
    else:
        return None


f = open('output2.txt', 'w+', newline='')
f.close()
recordsofcollege("Amravati")
recordsofcollege("Aurangabad")
recordsofcollege("Mumbai")
recordsofcollege("Nagpur")
recordsofcollege("Nashik")
recordsofcollege("Pune")

with open('output.csv', 'w', newline='') as f1:
    fieldnames = ['SrNo', 'College_Code', 'Institue_Name', 'Address', 'Email', 'District', 'Principal_Name',
                  'Office_No', 'Personal_No', 'TPO_Name', 'Autonomy_Status', 'Year_of_Establishment']
    thewriter = csv.DictWriter(f1, fieldnames=fieldnames)
    thewriter.writeheader()
    f1.close()

no_of_college = 1
file = open('output2.txt', 'r')
for f in file:
    o = list(map(str, f.split('$')))
    if (o[0] != 'NULL' and o[1] != 'NULL' and o[2] != 'NULL' and o[3] != 'NULL' and o[4] != 'NULL' and o[
        5] != 'NULL' and o[6] != 'NULL' and o[7] != 'NULL' and o[8] != 'NULL' and o[9] != 'NULL' and o[10] != 'NULL'):
        with open('output.csv', 'a', newline='') as f1:
            fieldnames = ['SrNo', 'College_Code', 'Institue_Name', 'Address', 'Email', 'District', 'Principal_Name',
                          'Office_No', 'Personal_No', 'TPO_Name', 'Autonomy_Status', 'Year_of_Establishment']
            thewriter = csv.DictWriter(f1, fieldnames=fieldnames)
            thewriter.writerow(
                {'SrNo': no_of_college, 'College_Code': int(o[0]), 'Institue_Name': o[1], 'Address': o[2],
                 'Email': o[3], 'District': o[4], 'Principal_Name': o[5], 'Office_No': int(o[6]),
                 'Personal_No': int(o[7]), 'TPO_Name': o[8], 'Autonomy_Status': o[9],
                 'Year_of_Establishment': int(o[10])})
            f1.close()
            no_of_college += 1
file.close()
os.remove('output.txt')
os.remove('output1.txt')
os.remove('output2.txt')

x=[]
y=[]
year=[]
import requests
import os
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with open('output.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        y.append(row[5])
        x.append(row[10])
        year.append(row[11])

x.pop(0)
y.pop(0)
year.pop(0)

sns.scatterplot(y,x,90)


plt.title('District vs Autonomy_Status ')

plt.ylabel('Autonomy Status')
plt.xlabel('District')
plt.xticks(rotation='vertical')
plt.show()

l=sorted(list(set(y)))
r=[]
for i in l:
    r.append(y.count(i))

k=dict.fromkeys(list(set(y)),0)
for i,j in k.items():
    k[i]=y.count(i)

plt.figure(figsize = (15,7))
plt.plot(r,l,.35,color='orange')

plt.title('District vs No of colleges')
plt.ylabel('No of colleges')
plt.xlabel('District')
plt.xticks(rotation='vertical')
plt.show()














































