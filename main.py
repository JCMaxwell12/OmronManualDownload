import requests
import os
from bs4 import BeautifulSoup


def sanitize(string):
    return "".join(x for x in string if x.isalnum())


urlDownload = 'https://edata.omron.com.au/eData/'
url = 'https://edata.omron.com.au/eData/manuals.html'
headers = ''
savePath = './'
dryRun = True
 
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a')



manDat = []
parentSection = '.'
for link in links:
    try:
        if link.parent.parent.td.attrs['valign'] == 'top':
            parentSection = link.parent.parent.td.text
    except:
        pass

    try:
        target = link.attrs['target']
    except KeyError:
        continue    # Value does not contain a file

    try:
        manName = link.parent.find_previous_sibling('td').text
    except AttributeError:
        manName = link.text
    
    manDat.append({
                  'parentSection': parentSection,
                  'fileName': link.text,
                  'href': link.attrs['href'],
                  'manName': manName
    })


for man in manDat:
    dir = savePath + sanitize(man['parentSection']) + '/'
    fileName = dir + sanitize(man['manName'] + man['fileName'])

    if os.path.exists(fileName):
        continue

    if not os.path.isdir(dir):
        os.mkdir(dir)

    if dryRun:
        print(f'''Downloading {urlDownload + man['href']}
        To {fileName}\n''')
        continue

    manResponse = requests.get(urlDownload + man['href'])

    with open(fileName, 'wb') as file:
        file.write(manResponse.content)
