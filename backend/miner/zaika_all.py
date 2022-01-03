import datetime
from time import sleep
import requests
from pprint import pprint
import json
import time

server = "http://127.0.0.1:8000/api/stats/"
argv_dict = dict()
ECHO = True
arg_list = ['token', 'bat', 'api_url', 'api_port', 'config', 'server', 'echo']
with open("miner_stat.cfg") as cfg:
    cfg_lines = cfg.readlines()
    for line in cfg_lines:
        key, value = line.strip().split("=")
        if key not in arg_list:
            print("Неизвестный аргумент")
            sleep(15)
            exit()
        argv_dict[key] = value
#
print(argv_dict)

try:
    URL = "http://" + f"{argv_dict.get('api_url')}:{argv_dict.get('api_port')}/stat"
    BAT_PATH = argv_dict.get('bat')
    if argv_dict.get('token'):
        TOKEN = argv_dict.get('token')
    else:
        print("Нет токена")
        sleep(15)
        exit()
    if argv_dict.get('server'):
        server = f"http://{argv_dict.get(f'server')}/api/stats/"

except Exception as e:
    print(f"Ошибка {e}")
    sleep(10)
    exit()

headers = {
    'Authorization': f'Bearer fd0ea523a00b7e4cad560938927b145077e4792c',
    'Content-Type': 'application/json',
}


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
             "rejected_shares":0, "stale_shares":0, 'fan': 0, 'temperature': 0, 'core_clock': 0, 'memory_clock': 0,
             'speed': 0, 'power_usage': 0}]}
    return normal_dict(error)


while True:
    for i in [{"url": "192.168.1.160:7890", "worker": '0x84fc5E96354844f5f27095d0A2B22377B6f54975.rtxz3060'},
              {"url": "192.168.1.157:7890", "worker": '0x84fc5E96354844f5f27095d0A2B22377B6f54975.rtxn3060'},]:
        URL = "http://" + f"{i.get('url')}/stat"
        try:
            response = requests.get(URL, verify=False, timeout=1)
            response = normal_dict(response.json())
        except Exception as e:
            print(e, i)
            response = error_response(i)
        sleep(1)
        try:
            response = requests.request("POST", server, headers=headers, data=json.dumps(response), verify=False, timeout=2)
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


# def check_miner(pid=None):
#     miner = False
#     for proc in psutil.process_iter():
#         if proc.name() == "miner.exe":
#             print("Процесс майнера работает")
#             miner = True
#             if pid:
#                 return proc.pid()
#     return miner
#
# class Miner:
#     def __init__(self):
#         self.speed = 0
#         self.power = 0
#         self.mclock = 0
#         self.status = True
#
#     def check_status(self):
#         if self.speed < speed_alarm:
#             print("Скорость ниже нормы")
#             self.status = False
#         if self.mclock < mclock_alarm:
#             print("Частота ниже нормы")
#             self.status = False
#         if self.power < power_alarm:
#             print("Потребление ниже нормы")
#             self.status = False
#         return self.status
#
#     def print_info(self):
#         print(f"{self.date}: Speed: {self.speed}, Memory: {self.mclock}, Power: {self.power}")
#
#     def get_info(self):
#         try:
#             response = requests.get(URL)
#             miner = response.json().get("devices")[0]
#         except Exception:
#             miner = {'power': 0, 'mclock': 0, 'speed': 0,}
#             print("offline")
#         # pprint(miner)
#         self.speed = round((miner.get('speed', 0)/1000000), 2)
#         self.power = miner.get('power_usage', 0)
#         self.mclock = miner.get('memory_clock', 0)
#         self.date = f"{datetime.now():%Y.%m.%d  %H:%M:%S}"
#         self.print_info()
#
#     def __str__(self):
#         return f"{self.date}: Speed: {self.speed}, Memory: {self.mclock}, Power: {self.power}"
#
# rig = Miner()
# while True:
#     rig.get_info()
#     if not rig.check_status():
#         if check_miner():
#             print("Попытаюсь включить разгон")
#             subprocess.Popen(afterburner)
#         else:
#             print("Попытаюсь включить майнер")
#             subprocess.Popen(BAT_PATH, creationflags=subprocess.CREATE_NEW_CONSOLE)
#         print("Нужно подождать 5 минут")
#         for i in tqdm(range(300)):
#             sleep(1)
#         if rig.check_status():
#             print("Вроде работает")
#         elif check_miner():
#             print("Пытаюсь перезапустить разгон и майнер")
#             subprocess.Popen(afterburner)
#             subprocess.Popen("taskkill /f /im miner.exe")
#             subprocess.Popen(BAT_PATH, creationflags=subprocess.CREATE_NEW_CONSOLE)
#             for i in tqdm(range(300)):
#                 sleep(1)
#     sleep(30)
import json
import os.path
# print(speed)
# with open(BAT_PATH) as f:
#     print(f.read())
# subprocess.Popen(BAT_PATH, creationflags=subprocess.CREATE_NEW_CONSOLE)
#
# json_test = {"miner":"GMiner 2.70","uptime":34505,"server":"eu1.ethermine.org:4444","user": "0x84fc5E96354844f5f27095d0A2B22377B6f54975.3080","extended_share_info":True,"shares_per_minute":0.92,"pool_speed":65847627,"algorithm":"Ethash","electricity":1.100,"total_accepted_shares":529,"total_rejected_shares":0,"total_stale_shares":0,"total_invalid_shares":0,"devices":[{"gpu_id":0,"bus_id":"0000:01:00.0","name":"3080","speed":72131151,"accepted_shares":529,"rejected_shares":0,"stale_shares":0,"invalid_shares":0,"fan":0,"temperature":57,"temperature_limit":90,"memory_temperature":0,"memory_temperature_limit":120,"core_clock":1080,"memory_clock":9355,"power_usage":115}],"speed_rate_precision":0,"speed_unit":"H/s","power_unit":"H/W"}
# test = {'miner': 'GMiner 2.73', 'uptime': 30389, 'server': 'eu1.ethermine.org:4444', 'user': '0x84fc5E96354844f5f27095d0A2B22377B6f54975.3060', 'extended_share_info': True, 'shares_per_minute': 0.57, 'pool_speed': 41129872, 'algorithm': 'Ethash', 'electricity': 0.817, 'total_accepted_shares': 291, 'total_rejected_shares': 0, 'total_stale_shares': 0, 'total_invalid_shares': 0, 'devices': [{'gpu_id': 0, 'bus_id': '0000:01:00.0', 'name': '3060', 'speed': 44646434, 'accepted_shares': 291, 'rejected_shares': 0, 'stale_shares': 0, 'invalid_shares': 0, 'fan': 0, 'temperature': 54, 'temperature_limit': 90, 'memory_temperature': 0, 'memory_temperature_limit': 120, 'core_clock': 990, 'memory_clock': 9000, 'power_usage': 97}], 'speed_rate_precision': 0, 'speed_unit': 'H/s', 'power_unit': 'H/W'}
# offline = {'miner': 'offline', 'uptime': 0, 'server': '-', 'user': '-', 'extended_share_info': True, 'shares_per_minute': 0, 'pool_speed': 0, 'algorithm': '-', 'electricity': 0, 'total_accepted_shares': 0, 'total_rejected_shares': 0, 'total_stale_shares': 0, 'total_invalid_shares': 0, 'devices': [{'gpu_id': 0, 'bus_id': '-', 'name': '-', 'speed': 0, 'accepted_shares': 0, 'rejected_shares': 0, 'stale_shares': 0, 'invalid_shares': 0, 'fan': 0, 'temperature': 0, 'temperature_limit': 0, 'memory_temperature': 0, 'memory_temperature_limit': 0, 'core_clock': 0, 'memory_clock': 0, 'power_usage': 0}], 'speed_rate_precision': 0, 'speed_unit': 'H/s', 'power_unit': 'H/W'}
