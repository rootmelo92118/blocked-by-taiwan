import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get("https://rpz.twnic.tw/e.html").text, "html.parser")
datap = soup.find_all("tr")
del datap[0]
data = ""
for i in datap:
    data += i.find_all("td")[-2].text + "\n"
with open("blockedbytaiwan.txt","a") as f:
    f.write(data)
    f.close()
