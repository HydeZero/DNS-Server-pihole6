if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(
            prog='WiiLink PiHole6 Setup',
            description='Adds the current pihole list to your PiHole6 server\'s DNS config via the server API.')
    parser.add_argument("server", default="http://pi.hole:80")

    args = parser.parse_args()

    import getpass

    cur_pass = getpass.getpass('PiHole Password, used for API authentication: ')

    import requests
    import json
    
    url = args.server + "/api"
    payload = {'password': cur_pass}
    
    del cur_pass

    response = requests.request("POST", url + "/auth", json=payload, verify=False)

    auth_json = ""
    sid = ""
    csrf = ""

    try:
        auth_json = json.loads(response.text)
        sid = auth_json["session"]["sid"]
        csrf = auth_json["session"]["csrf"]
    except Exception as e:
        print("Error parsing json, exiting.")
        exit()

    print("Authentication complete.")

    with open("dns_zones-hosts.txt", "r") as hosts:
        host_list = hosts.read()

    hosts = host_list.split("\n")

    print("Adding...")
    
    while True:
        try:
            blank = hosts.index('')
            hosts.pop(blank)
        except Exception as e:
            print(e)
            break
            


    
    headers = {"X-FTL-SID": sid, "X-FTL-CSRF": csrf}
    from urllib.parse import quote
    import time
    for host in hosts:
        print(host)
        host = quote(host)
        response = requests.request("PUT", url + "/config/dns/hosts/" + host, headers=headers)
    print("done!")
