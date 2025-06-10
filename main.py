import requests
from bs4 import BeautifulSoup

urlDownload = 'https://edata.omron.com.au/eData/'
url = 'https://edata.omron.com.au/eData/manuals.html'
headers = ''
 
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a')

manDat = []
for link in links:
    try:
        target = link.attrs['target']
    except KeyError:
        continue    # Value does not contain a file

    try:
        manName = link.parent.find_previous_sibling('td').text
    except AttributeError:
        manName = link.text

    manDat.append({
                  'parentSection': link.parent.parent.parent.tr.td.text,
                  'fileName': link.text,
                  'href': link.attrs['href'],
                  'manName': manName
    })


