import dns.resolver, sys

def DNSQuery(my_resolver,domain_name,source_port=0):
    try:
        result = my_resolver.query(domain_name,source_port=source_port)   
        if len(result.response.answer) == 1:
            print(result.response.answer[0].to_text())
            return result.response.answer[0].to_text().split(" ")
        else:
            for i in result.response.answer:
                print(i.to_text())
                return None
    except Exception as e:
        print(domain_name + " Error: unable to start thread")
        return None
  
def removeDomainWhichAreNoLongerBlocked(domain_list,specified_ip_list,source_port=0):
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = ["168.95.1.1"]
    raw_list = ""
    adguard_format = ""
    adguard_format_include_rewrote_ip = ""
    for i in domain_list:
        dnsres = DNSQuery(my_resolver,i,source_port=source_port)
        if dnsres != None and dnsres[4] in specified_ip_list:
            raw_list += i+"\n"
            adguard_format += "||"+i+"^\n"
            adguard_format_include_rewrote_ip += "||"+i+"^$dnsrewrite=NOERROR;A;"+dnsres[4]+"\n"
    return [raw_list,adguard_format,adguard_format_include_rewrote_ip]

def main(specified_ip_list,raw_filepath="./raw.txt",adguard_filepath="./adguard.txt",adguard_rewrote_filename="./adguard_rewrote.txt"):
    domain_list = []
    for line in sys.stdin:
        domain_list.append(line.strip("\n"))
    specified_ip_list = specified_ip_list.split(",") if "," in specified_ip_list else specified_ip_list
    data = removeDomainWhichAreNoLongerBlocked(domain_list=domain_list,specified_ip_list=specified_ip_list)
    with open(raw_filepath,"w") as f:
        f.write(data[0])
        f.close()
    with open(adguard_filepath,"w") as f:
        f.write(data[1])
        f.close()
    with open(adguard_rewrote_filename,"w") as f:
        f.write(data[2])
        f.close()


if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
