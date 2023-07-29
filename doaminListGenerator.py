import requests, json
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

plain_text = requests.get("https://od.moi.gov.tw/api/v1/rest/datastore/A01010000C-002150-013").text
row_data = json.loads(plain_text)
del row_data["result"]["records"][0]
npa_rpz_row = ""
npa_rpz_AdGuardHome = ""
for i in row_data["result"]["records"]:
    if "/" in i["WEBURL"]:
        npa_rpz_row += i["WEBURL"].split("/")[0] + "\n"
        npa_rpz_AdGuardHome += "||" + i["WEBURL"].split("/")[0] + "^\n"
    else:
        npa_rpz_row += i["WEBURL"] + "\n"
        npa_rpz_AdGuardHome += "||" + i["WEBURL"] + "^\n"
with open("165RPZ1.0.txt","a") as f:
    f.write(npa_rpz_row)
    f.close()
with open("./AdGuardHome/twnicRPZ1.0.txt","a") as f:
    f.write(npa_rpz_AdGuardHome)
    f.close()
