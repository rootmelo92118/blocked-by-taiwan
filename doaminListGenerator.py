import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get("https://rpz.twnic.tw/e.html").text, "html.parser")
exec(str(soup.find("script")).split(";")[0].split("const ")[1])
data = ""
for i in rpzdata:
    for datap in i["domains"]:
        data += datap + "\n"
with open("blockedbytaiwan.txt","a") as f:
    f.write(data)
    f.close()
