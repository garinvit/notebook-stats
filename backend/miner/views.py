import json
from datetime import datetime
from pprint import pprint

import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .miner_utils import json_test, test, offline
from .models import Miner


# Create your views here.
def index(request):
    miners = Miner.objects.all()
    miner_list = []
    for rig in miners:
        rig_dict = rig.get_dict()
        URL = "http://" + f"{rig.url}/stat"
        try:
            response = requests.get(URL, verify=False, timeout=0.2)
            # pprint(response.json())
            miner = response.json().get("devices")[0]
        except Exception:
            miner = {'power': 0, 'mclock': 0, 'speed': 0, 'temperature': 0}
        rig_dict['speed'] = round((miner.get('speed', 0)/1000000), 2)
        rig_dict['power'] = int(miner.get('power_usage', 0))
        rig_dict['temperature'] = int(miner.get('temperature', 0))
        rig_dict['invalid_shares'] = int(miner.get('invalid_shares', 0))
        rig_dict['mclock'] = int(miner.get('memory_clock', 0))
        rig_dict.update(rig.check_status(rig_dict['speed'], rig_dict['power'], rig_dict['mclock']))
        miner_list.append(rig_dict)
    # print(miner_list)
    date = f"{datetime.now():%Y.%m.%d  %H:%M:%S}"
    return render(request, 'index.html', context={"miners": miner_list, "date": date})

# data = {}
def rig_view(request, id):
    try:
        rig = get_object_or_404(Miner, id=id)
        # print(rig)
        URL = "http://" + f"{rig.url}/stat"
        response = requests.get(URL, verify=False, timeout=0.1)
        data = response.json()
    except Exception:
        # data = offline
        data = {}
    return render(request, 'rig.html', context={"data": data, "URL": URL,})


# def stat(request):
#     global data
#     return HttpResponse(json.dumps(data))
