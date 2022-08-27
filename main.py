import requests
from bs4 import BeautifulSoup

request_uis = requests.get("https://uis.edu.co/uis-programas-pregrado-es/")
request_uts = requests.get("https://www.uts.edu.co/sitio/oferta-academica-2/")
request_unab = requests.get("https://unab.edu.co/pregrados/")

soup_uis = BeautifulSoup(request_uis.content, 'html.parser')
soup_uts = BeautifulSoup(request_uts.content, 'html.parser')
soup_unab = BeautifulSoup(request_unab.content, 'html.parser')

h4_tags = soup_uis.find_all('h4')

ul_tags = soup_uts.find_all('ul')
ul_tags = ul_tags[22:26]

h2_tags = soup_unab.find_all('h2')
h2_tags = h2_tags[:39]

print('---------------- UNAB --------------------')
for tag in h2_tags:
    tag_content = tag.a.string
    tag_link = tag.a['href']
    print(f'{tag_content} -> {tag_link}')

print('---------------- UTS --------------------')
for tag in ul_tags:
    for li in tag.find_all('li'):
        li_content = li.a.string
        if li_content != None:
            print(li_content)

print('---------------- UIS --------------------')
for tag in h4_tags:
    print(tag.a.string)
