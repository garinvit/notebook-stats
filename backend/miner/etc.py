from pprint import pprint

stat = {"miner":"GMiner 2.73","uptime":704042,"server":"eu1.ethermine.org:4444","user": "0x84fc5E96354844f5f27095d0A2B22377B6f54975.3060","extended_share_info": True,"shares_per_minute":0.58,"pool_speed":40365355,"algorithm":"Ethash","electricity":18.286,"total_accepted_shares":6799,"total_rejected_shares":0,"total_stale_shares":0,"total_invalid_shares":0,"devices":[{"gpu_id":0,"bus_id":"0000:01:00.0","name":"3060","speed":43429602,"accepted_shares":6799,"rejected_shares":0,"stale_shares":0,"invalid_shares":0,"fan":0,"temperature":55,"temperature_limit":90,"memory_temperature":0,"memory_temperature_limit":120,"core_clock":1095,"memory_clock":8797,"power_usage":93}],"speed_rate_precision":0,"speed_unit":"H/s","power_unit":"H/W"}

pprint(stat)