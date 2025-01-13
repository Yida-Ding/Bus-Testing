import requests
import json
from datetime import datetime
import networkx as nx
import itertools

headers = {'Content-Type': 'application/json', 'token':'222'}

server = "http://121.199.173.212:8031"
# server = "https://dispatch.zex-t.cn:8031"

# 获取上线订单
response = requests.get(f"{server}/region/1", headers=headers)
print(response)
res = json.loads(response.text)
print(res)

# config = {
#     "region_id": 1,
#     "max_wait_time": 10,
#     "max_delay_time": 10,
#     "sharing_ratio": 2,
#     "overtime_sharing_ratio": 1.3,
#     "turning_angle": 180,
#     "within_tenmin_delay_time": 5,
#     "beyond_tenmin_delay_time": 8,
#     "next_station_lock_dist": 200,
#     "assign_concentration": 10
# }


# requests.post(f"{server}/config", headers=headers, json=config)


# jsondata = eval(response.text)["data"]
# with open("data/static_2.json", 'w', encoding="utf-8") as outfile:
#     json.dump(jsondata, outfile, ensure_ascii=False, indent = 4)


# # 下线多余车辆
# data = {
#     "region_id":1, 
#     "vehicle_location":[
#         {
#             "vehicle_id": 1,
#             "lat": 28.126267365816954,
#             "lon": 112.89570937100143, 
#             "status": 0,
#             "direction": 0
#         }
#     ]
# }
# response = requests.post("https://dispatch.zex-t.cn:8031/vehicle/location", headers=headers, json=data)
# print(f"{response.text}")

# # 获取调度信息
# response = requests.get('https://dispatch.zex-t.cn:8031/all-dispatch/1', headers=headers)
# res = json.loads(response.text)
# print(res)

# # 获取有向边数据
# response = requests.get('https://dispatch.zex-t.cn:8031/region/1/segments', headers=headers)
# seg_data = eval(response.text)["data"]
# G = nx.DiGraph()
# for row in seg_data:
#     from_n, to_n = row["seg_stations"]
#     G.add_edge(from_n, to_n, weight=row["seg_dist"])


# def sum_path(stat_lst):
#     sum_dist = 0
#     for i in range(len(stat_lst)-1):
#         dist = nx.dijkstra_path_length(G, source=stat_lst[i], target=stat_lst[i+1], weight='weight')
#         sum_dist += dist
    
#     return sum_dist

# originL = [129,2,126,105,11]
# pairs = [[2, 126],[105, 11]]

# perm2res = {}
# for perm in list(itertools.permutations(originL[1:])):
#     perm = list(perm)
#     # check pair feasibility
#     check = True
#     for pair in pairs:
#         a, b = pair
#         ia = perm.index(a)
#         ib = perm.index(b)
#         if ia > ib:
#             check = False
    
#     if check:
#         perm = tuple([129]+perm)
#         perm2res[perm] = sum_path(perm)

# print(perm2res)

# min_key = min(perm2res, key=perm2res.get)
# print(min_key, perm2res[min_key])

