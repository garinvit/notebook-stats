from time import sleep
import requests
import json

server = "127.0.0.1:8000"
argv_dict = dict()
ECHO = True
arg_list = ['token', 'bat', 'miner_list', 'config', 'server', 'echo']
with open("miner_stat.cfg") as cfg:
    cfg_lines = cfg.readlines()
    for line in cfg_lines:
        key, value = line.strip().split("=")
        if key not in arg_list:
            print("Неизвестный аргумент")
            sleep(15)
            exit()
        argv_dict[key] = value
miner_list = []
with open("miner_list.cfg") as rigs:
    rigs_list = rigs.readlines()
    for line in rigs_list:
        rig_dict = dict()
        args = line.strip().split(",")
        for arg in args:
            key, value = arg.strip().split("=")
            rig_dict[key] = value
        miner_list.append(rig_dict)

print(argv_dict, miner_list)

if argv_dict.get('server'):
    server = f"http://{argv_dict.get(f'server')}/api/stats/"


def normal_dict(response):
    response.update(response.pop("devices")[0])
    response['accepted_shares'] = response.pop('total_accepted_shares')
    response['invalid_shares'] = response.pop('invalid_shares')
    response['rejected_shares'] = response.pop('rejected_shares')
    response['stale_shares'] = response.pop('stale_shares')
    response['miner_worker'] = response.pop('user')
    response['power'] = response.pop('power_usage')
    response['speed'] = round(response.pop('speed') / 1000000, 2)
    response['pool_speed'] = round(response.pop('pool_speed') / 1000000, 2)
    response['version'] = response.pop('miner')
    return response


def error_response(item):
    error = {'miner': 'offline', 'uptime': 0, 'server': '', 'user': item.get('worker'),
             'shares_per_minute': 0, 'pool_speed': 0, 'electricity': 0, 'total_accepted_shares': 0,
             'total_rejected_shares': 0, 'total_stale_shares': 0, 'total_invalid_shares': 0, 'devices': [
            {'gpu_id': 0, 'bus_id': '', 'name': item.get("worker").split(".")[1], 'invalid_shares': 0,
             "rejected_shares": 0, "stale_shares": 0, 'fan': 0, 'temperature': 0, 'core_clock': 0, 'memory_clock': 0,
             'speed': 0, 'power_usage': 0}]}
    return normal_dict(error)


while True:
    for i in miner_list:
        URL = "http://" + f"{i.get('url')}/stat"
        try:
            response = requests.get(URL, verify=False, timeout=1)
            response = normal_dict(response.json())
        except Exception as e:
            print(e, i)
            response = error_response(i)
        sleep(1)
        try:
            headers = {
                'Authorization': f'Bearer {i.get("token")}',
                'Content-Type': 'application/json',
            }
            response = requests.request("POST", server, headers=headers, data=json.dumps(response), verify=False,
                                        timeout=2)
            if ECHO:
                data = response.json()
                speed = data.get("speed")
                name = data.get("miner_worker").split(".")[1]
                time = data.get("datetime")
                power = data.get("power")
                if power == 0 and speed == 0:
                    print(f"{time} Miner offline")
                else:
                    print(f"OK:{time}: {name} Speed: {speed}, Power: {power}")
        except Exception as e:
            print("Server offline", e)

    sleep(300)
