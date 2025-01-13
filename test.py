import requests
import json
from datetime import datetime


headers = {'Content-Type': 'application/json', 'token':'222'}
now = datetime.now()

# 第一辆车位置
data = {
    "region_id":1, 
    "vehicle_location":[
        {
            "vehicle_id": 1,
            "lat": 28.126267365816954,
            "lon": 112.89570937100143, 
            "status": 1,
            "direction": 315
        }
    ]
}
response = requests.post("https://dispatch.zex-t.cn:8031/vehicle/location", headers=headers, json=data)
print(f"1. {response.text}")

# 第二辆车位置
data = {
    "region_id":1, 
    "vehicle_location":[
        {
            "vehicle_id": 2,
            "lat": 28.13814561232112,
            "lon": 112.90367337946118,
            "status": 1,
            "direction": 150
        }
    ]
}
response = requests.post("https://dispatch.zex-t.cn:8031/vehicle/location", headers=headers, json=data)
print(f"2. {response.text}")


# 第一个订单
data = {
    "region_id":1,
    "order_id":f"1-{now}", 
    "pax_num":1, 
    "order_time":"2023-11-25 09:05:05",
    "available_pickup_station_list":[16],  
    "available_pickup_walkingtime_list":[110], 
    "available_dropoff_station_list":[1],    
    "available_dropoff_walkingtime_list":[120]
}
response = requests.post("https://dispatch.zex-t.cn:8031/order", headers=headers, json=data)
print(f"3. {response.text}")

# 第二个订单
data = {
    "region_id":1,
    "order_id":f"2-{now}", 
    "pax_num":1, 
    "order_time":"2023-11-25 09:05:05",
    "available_pickup_station_list":[14],  
    "available_pickup_walkingtime_list":[110], 
    "available_dropoff_station_list":[19],    
    "available_dropoff_walkingtime_list":[108]
}
response = requests.post("https://dispatch.zex-t.cn:8031/order", headers=headers, json=data)
print(f"4. {response.text}")


# 获取调度信息
response = requests.get('https://dispatch.zex-t.cn:8031/all-dispatch/1', headers=headers)
print(f"5. {response.text}")



# # 批量结束
# data = {
#     "region_id":1, 
#     "ids":[f"1-{now}",f"2-{now}"],
# }
# response = requests.post("https://dispatch.zex-t.cn:8031/order/batch-cancel", headers=headers, json=data)
# print(f"6. {response.text}")



# with open("data/static.json", 'r', encoding='utf-8') as outfile:
#     res_dict = json.load(outfile)

# response = requests.put("https://dispatch.zex-t.cn:8031/region", headers=headers, json=res_dict)
# print(response.text)




# print(response.text)
