import requests, json, logging, sys

logger = logging.getLogger(__name__)

def TWNIC_RPZ(source_url):
    raw = requests.get(source_url)
    if raw.status_code != 200:
        logger.critical("Fetch data error.")
        sys.exit(1)
    try:
        rpz_data = json.loads(raw.text.split('<script>')[1].split(';')[0].split('= ')[1])
        twnic_rpz_1_0_raw = ""
        twnic_rpz_1_0_AdGuardHome = ""
        for i in rpz_data:
            for datap in i["domains"]:
                twnic_rpz_1_0_raw += datap + "\n"
                twnic_rpz_1_0_AdGuardHome += "||" + datap + "^\n"
        with open("twnicRPZ1.0.txt","w") as f:
            f.write(twnic_rpz_1_0_raw)
        with open("./AdGuardHome/twnicRPZ1.0.txt","w") as f:
            f.write(twnic_rpz_1_0_AdGuardHome)
    except Exception as e:
        logger.critical(e)
        sys.exit(1)

def NPA_165(source_url):
    raw = requests.get("https://od.moi.gov.tw/api/v1/rest/datastore/A01010000C-002150-013")
    if raw.status_code != 200:
        logger.critical("Fetch data error.")
        sys.exit(1)
    try:
        raw_data = json.loads(raw.text)
        del raw_data["result"]["records"][0]
        npa_165_raw = ""
        npa_165_AdGuardHome = ""
        for i in raw_data["result"]["records"]:
            if "/" in i["WEBURL"]:
                npa_165_raw += i["WEBURL"].split("/")[0] + "\n"
                npa_165_AdGuardHome += "||" + i["WEBURL"].split("/")[0] + "^\n"
            else:
                npa_165_raw += i["WEBURL"] + "\n"
                npa_165_AdGuardHome += "||" + i["WEBURL"] + "^\n"
        with open("NPA165.txt","w") as f:
            f.write(npa_165_raw)
        with open("./AdGuardHome/NPA165.txt","w") as f:
            f.write(npa_165_AdGuardHome)
    except Exception as e:
        logger.critical(e)
        sys.exit(1)
    
def main():
    TWNIC_RPZ("https://rpz.twnic.tw/e.html")
    NPA_165("https://od.moi.gov.tw/api/v1/rest/datastore/A01010000C-002150-013")
    
if __name__ == '__main__':
    main()
