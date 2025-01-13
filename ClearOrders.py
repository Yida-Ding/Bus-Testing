import requests
import json
from datetime import datetime


headers = {'Content-Type': 'application/json', 'token':'222'}

# 获取上线订单

server = "http://121.199.173.212:8031"
# server = "https://dispatch.zex-t.cn:8031"

for reg_id in range(1, 4):
    response = requests.get(f'{server}/order-list/{reg_id}', headers=headers)
    res = json.loads(response.text)
    ord_ids = [row['order_id'] for row in res["data"]]
    print(ord_ids)

    # 批量结束
    data = {
        "region_id":reg_id, 
        "ids": ord_ids,
    }
    response = requests.post(f"{server}/order/batch-cancel", headers=headers, json=data)
    print(f"{response.text}")



# # 获取调度信息
# response = requests.get('https://dispatch.zex-t.cn:8031/all-dispatch/1', headers=headers)
# res = json.loads(response.text)
# print(res)
# # print(res['data'])
# # v1 = res['data']['vehicle_dispatch'][0]
# # v2 = res['data']['vehicle_dispatch'][1]
# # set1 = set([row[0]['order_id'] for row in v1['station_related_orders_list']])
# # set2 = set([row[0]['order_id'] for row in v2['station_related_orders_list']])
# # print(set1, set2)

