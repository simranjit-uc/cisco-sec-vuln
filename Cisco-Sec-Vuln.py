import json
import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import datetime, openpyxl
import os


API_TOKEN_CLIENT_ID = "<Client ID from the API Console Page>"
API_TOKEN_CLIENT_PASS = "<Client Password from the API Console Page>"
TOKEN_URL = "https://cloudsso.cisco.com/as/token.oauth2"
CUCM_ADV_URL = "https://api.cisco.com/security/advisories/product?product=Cisco%20Unified%20Communications%20Manager"


current_Month_str = datetime.datetime.today().strftime("%B") + " " + str(datetime.datetime.today().year)

disable_warnings(InsecureRequestWarning)

def get_Token():
    response = requests.post(TOKEN_URL, verify=False, data={"grant_type": "client_credentials"},
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             params={"client_id": API_TOKEN_CLIENT_ID, "client_secret": API_TOKEN_CLIENT_PASS})

    json_form = json.loads(response.text)
    access_token = json_form["access_token"]
    return access_token


def get_Data():
    AUTH = "Bearer " + get_Token()
    HEADERS = {"Authorization": AUTH}
    CUCM_REQUEST = requests.get(CUCM_ADV_URL, verify = False, headers = HEADERS)
    cucm_Resp_JSON = json.loads(CUCM_REQUEST.text)
    cucm_Advisories = cucm_Resp_JSON["advisories"]
    curr_Year_Str = str(datetime.datetime.now().year)

    count = 1
    wb = openpyxl.Workbook()
    cucm_ws = wb.create_sheet(title = "CUCM", index = 1)


    for a_det in cucm_Advisories:
        if curr_Year_Str in a_det["lastUpdated"]:
            adv_ID = a_det["advisoryId"]
            last_Update = a_det["lastUpdated"]
            adv_Title = a_det["advisoryTitle"]
            cvs_Score = a_det["cvssBaseScore"]
            cve_id = a_det["cves"]
            pub_url = a_det["publicationUrl"]
            sev_State = a_det["sir"]
            length = len(adv_ID)
            count += 1

            cucm_ws.cell(row = 1, column = 1, value="Advisory ID" )
            cucm_ws.cell(row = 1, column = 2, value = "Advisory Title")
            cucm_ws.cell(row = 1, column = 3, value = "Last Updated")
            cucm_ws.cell(row = 1, column = 4, value="CVE ID")
            cucm_ws.cell(row = 1, column = 5, value = "CVS Score")
            cucm_ws.cell(row = 1, column = 6, value="URL")
            cucm_ws.cell(row = 1, column = 7, value = "Severity")

            advid_Cell_Loc = cucm_ws.cell(row = count, column = 1)
            advtitle_Cell_Loc = cucm_ws.cell(row = count, column = 2)
            lu_Cell_Loc = cucm_ws.cell(row = count, column = 3)
            cve_Cell_Loc = cucm_ws.cell(row=count, column=4)
            cvs_Cell_loc = cucm_ws.cell(row = count, column = 5)
            url_Cell_loc = cucm_ws.cell(row=count, column=6)
            sev_Cell_Loc = cucm_ws.cell(row = count, column = 7)

            advid_Cell_Loc.value = adv_ID
            advtitle_Cell_Loc.value = adv_Title
            lu_Cell_Loc.value = last_Update
            cve_Cell_Loc.value = str(cve_id)
            cvs_Cell_loc.value = cvs_Score
            url_Cell_loc.value = pub_url
            sev_Cell_Loc.value = sev_State

    count = 1



    global file_Loc, today
    today = str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.
                                                                                                    now().year)
    file_Loc = "D:/" + today + ".xlsx"
    wb.save(file_Loc)


def create_Inc():
    uname = os.environ.get('uname')
    pwd = os.environ.get('pwd')
    url = "https://<Your Service Now Instance URL>/api/now/table/incident"
    headers = {'Content-Type': 'application/json', "Accept": "application/json"}
    data = {"short_description": "Cisco UC Vulnerabilities " + current_Month_str, "description" : "List of Cisco CUCM Vulnerabilities"}
    resp_INC = requests.post(url, json=data, auth=(uname, pwd), verify=False, headers=headers)
    output = resp_INC.json()
    print(output)
    sysid = output["result"]["sys_id"]
    return sysid


def add_Attach():
    uname = os.environ.get('uname')
    pwd = os.environ.get('pwd')

    url_Attach = "https://<Your Service Now Instance URL>/api/now/attachment/file?table_name=incident&table_sys_id=" + \
                 create_Inc() + "&file_name=Advisory " + current_Month_str + ".xlsx"
    post_headers = {'Content-Type': 'application/vnd.ms-excel'}
    file = open(file_Loc, 'rb').read()
    resp_Attach = requests.post(url_Attach, headers=post_headers, data=file, auth=(uname, pwd))



get_Data()
add_Attach()




