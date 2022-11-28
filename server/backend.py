import requests
import json

username_password = "awqety:qaerft"
url = "http://esw-onem2m.iiit.ac.in:443/" + "~/in-cse/in-name/"

nodes = {
    "Machine-1": "Team-15/Node-1/Data",
    "Machine-2": "Team-15/Node-2/Data",
    "Machine-3": "Team-15/Node-3/Data",
    "Machine-4": "Team-15/Node-4/Data"
}


def get_sensor_data(saved):
    return get_sensor_data_thingspeak(saved)


def get_sensor_data_thingspeak(saved):
    data = {**{node: "" for node in nodes}, "_error": ""}
    chart = {node: [[], []] for node in nodes}
    for node in nodes:
        if saved == False:
            get = requests.get(
                f"https://api.thingspeak.com/channels/1944689/fields/{node[-1]}.json?results=10&timezone=Asia%2FKolkata",
                timeout=3)
            get_json = get.json()
            # print(get_json)
            with open(f"data/{node}.json", "w") as f:
                json.dump(get_json, f)
        else:
            with open(f"data/{node}.json", "r") as f:
                get_json = json.load(f)
        for item in get_json["feeds"][-10:]:
            chart[node][0].append(item[f"field{node[-1]}"])
            # "2022-11-19T13:32:43Z"
            chart[node][1].append(item["created_at"][11:16])
        data[node] = get_json["feeds"][-1][f"field{node[-1]}"]
        if data[node]:
            if float(data[node]) > 0.6:
                data[node] = "On"
            else:
                data[node] = "Off"
    return data, chart


def get_sensor_data_om2m(saved=False):
    headers = {
        'X-M2M-Origin': username_password,
        'Content-type': 'application/json'
    }
    data = {**{node: "" for node in nodes}, "_error": ""}
    chart = {node: [[], []] for node in nodes}
    get_json = {"m2m:cnt": {"m2m:cin": []}}
    # try:
    if 1:
        for node in nodes:
            if saved == False:
                get = requests.get(f"{url}{nodes[node]}?rcn=4",
                                   headers=headers,
                                   timeout=3)
                get_json = get.json()
                with open(f"data/{node}.json", "w") as f:
                    json.dump(get_json, f)
            else:
                with open(f"data/{node}.json", "r") as f:
                    get_json = json.load(f)
            for item in get_json["m2m:cnt"]["m2m:cin"][-10:]:
                chart[node][0].append(float(item["con"]))
                chart[node][1].append(
                    f'{item["lt"][9:11]}:{item["lt"][11:13]}')
            data[node] = get_json["m2m:cnt"]["m2m:cin"][-1]["con"]
            # chart[node] = list(zip(
            #     *((float(item["con"]), f'{item["lt"][9:11]}:{item["lt"][12:14]}') for item in get_json["m2m:cnt"]["m2m:cin"][:5])))
    # except:
    #     data[
    #         "_error"] = "Unable to receive data from server (OM2M Not Responding)"
    return data, chart


# def send_data(protector):
#     try:
#         create_ae(url, "protector")
#         # delete(url+"protector/command")
#         create_cnt(url + "protector", "command")
#         if protector["automatic"]:
#             command = 0
#         elif protector["status"]:
#             command = 1
#         else:
#             command = -1
#         create_data_cin(url + "protector/command", command)
#         print("sent", command, protector)
#     except:
#         protector[
# "_error"] = "Unable to send commands to server (OM2M Not Responding)"

# onem2m functions

# def create_ae(uri_cse, ae_name, ae_labels=""):
#     headers = {
#         'X-M2M-Origin': username_password,
#         'Content-type': 'application/json;ty=2'
#     }
#     body = {
#         "m2m:ae": {
#             "rn": str(ae_name),
#             "api": "acp_admin",
#             "rr": "true",  # resource reachable from CSE
#             "lbl": ae_labels
#         }
#     }
#     requests.post(uri_cse, data=json.dumps(body), headers=headers, timeout=3)

# def create_cnt(uri_ae, cnt_name, cnt_labels=""):
#     headers = {
#         'X-M2M-Origin': username_password,
#         'Content-type': 'application/json;ty=3'
#     }
#     body = {"m2m:cnt": {"rn": str(cnt_name), "mni": 120, "lbl": cnt_labels}}
#     requests.post(uri_ae, data=json.dumps(body), headers=headers, timeout=3)

# def create_data_cin(uri_cnt, value, cin_labels=""):
#     headers = {
#         'X-M2M-Origin': username_password,
#         'Content-type': 'application/json;ty=4'
#     }
#     body = {"m2m:cin": {"con": str(value), "lbl": cin_labels, "cnf": "text"}}
#     requests.post(uri_cnt, data=json.dumps(body), headers=headers, timeout=3)

# def delete(uri):
#     headers = {
#         'X-M2M-Origin': username_password,
#         'Content-type': 'application/json'
#     }
#     requests.delete(uri, headers=headers, timeout=3)
