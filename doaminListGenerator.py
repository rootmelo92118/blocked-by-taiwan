import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get("https://rpz.twnic.tw/e.html").text, "html.parser")
exec(str(soup.find("script")).split(";")[0].split("const ")[1])
rpz_1_0_row = ""
rpz_1_0_AdGuardHome = ""
for i in rpzdata:
    for datap in i["domains"]:
        rpz_1_0_row += datap + "\n"
        rpz_1_0_AdGuardHome += "||" + datap + "^\n"
with open("rpz1.0row.txt","a") as f:
    f.write(rpz_1_0_row)
    f.close()
with open("rpz1.0AdGuardHome.txt","a") as f:
    f.write(rpz_1_0_AdGuardHome)
    f.close()
