import requests
import os
from bs4 import BeautifulSoup
import re
from time import sleep
from random import randint


def sanitize(string):
    return re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", string)


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
        if link.parent.name == 'h1':
            product = link.parent.text;
    except:
        pass

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

    if parentSection == link.text:
        parentSection = '';
    
    manDat.append({
                  'product': sanitize(product),
                  'parentSection': sanitize(parentSection),
                  'fileName': sanitize(link.text),
                  'href': link.attrs['href'],
                  'manName': sanitize(manName)
    })


for man in manDat:
    dir = savePath + man['product'] + '/' + man['parentSection'] + '/'
    fileName = dir + man['manName'] + ' ' + man['fileName'] + '.pdf'

    if os.path.exists(fileName):
        continue

    if not os.path.isdir(dir):
        os.makedirs(dir)

    if dryRun:
        print(f'''Downloading {urlDownload + man['href']}
        To {fileName}\n''')
        continue

    manResponse = requests.get(urlDownload + man['href'])
    
    try:
        with open(fileName, 'wb') as file:
            file.write(manResponse.content)
    except:
        print(f'Could not download {fileName}')

    sleep(randint(2, 30))
