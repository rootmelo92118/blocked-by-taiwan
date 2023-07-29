import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get("https://rpz.twnic.tw/e.html").text, "html.parser")
exec(str(soup.find("script")).split(";")[0].split("const ")[1])
twnic_rpz_1_0_row = ""
twnic_rpz_1_0_AdGuardHome = ""
for i in rpzdata:
    for datap in i["domains"]:
        twnic_rpz_1_0_row += datap + "\n"
        twnic_rpz_1_0_AdGuardHome += "||" + datap + "^\n"
with open("twnicRPZ1.0.txt","a") as f:
    f.write(twnic_rpz_1_0_row)
    f.close()
with open("./AdGuardHome/twnicRPZ1.0.txt","a") as f:
    f.write(twnic_rpz_1_0_AdGuardHome)
    f.close()
