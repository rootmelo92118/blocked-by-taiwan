import requests, json, logging, sys

logger = logging.getLogger(__name__)

def main():
    raw = requests.get("https://rpz.twnic.tw/e.html")
    if raw.status_code != 200:
        logger.critical("Fetch data error.")
        sys.exit(1)

    rpz_data = json.loads(raw.text.split('<script>')[1].split(';')[0].split('= ')[1])
    twnic_rpz_1_0_raw = ""
    twnic_rpz_1_0_AdGuardHome = ""
    for i in rpz_datatttt:
        for datap in i["domains"]:
            twnic_rpz_1_0_raw += datap + "\n"
            twnic_rpz_1_0_AdGuardHome += "||" + datap + "^\n"
    with open("twnicRPZ1.0.txt","w") as f:
        f.write(twnic_rpz_1_0_raw)
    with open("./AdGuardHome/twnicRPZ1.0.txt","w") as f:
        f.write(twnic_rpz_1_0_AdGuardHome)

if __name__ == '__main__':
    main()
