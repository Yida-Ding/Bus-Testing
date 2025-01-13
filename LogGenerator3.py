import logging
import json
from datetime import datetime
import time
import random

# prepare station location
with open("data/static_2.json", 'r', encoding='utf-8') as outfile:
    stat_dict = json.load(outfile)["stations"]
ids = [dic["station_id"] for dic in stat_dict]
locBD = [(dic["station_lon"], dic["station_lat"]) for dic in stat_dict]
id2loc = {ids[i]: locBD[i] for i in range(len(ids))}

# region1 (left, right) station IDs
leftIDs = [2, 15, 22, 99, 100, 101, 102, 105, 108, 114, 126, 129, 145, 146]
rightIDs = [98, 147, 148, 149, 150, 151, 152]

class Logger:
    def __init__(self, filename:str):
        """
        initialize the logger file
        """
        # 创建Logger对象并设置输出格式
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler(f'{filename}.json')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)
        self.logger.info(json.dumps({"sec":0, "action":"start", "data":{}}))

    def add_info_to_logger(self, sec:int, action:str, data:dict):
        """
        add logger info
        """
        self.logger.info(json.dumps({"sec":sec, "action":action, "data":data}))


if __name__ == '__main__':
    
    test_id = 54
    prefix = f"TEST-{test_id}"
    myLogger = Logger(f"logs/log_{test_id}")

    # vehicle 1 position
    stat = random.choice(leftIDs)
    data = {
        "region_id":1, 
        "vehicle_location":[
            {
                "vehicle_id": 1,
                "lat": id2loc[stat][1],
                "lon": id2loc[stat][0],
                "station": stat,
                "status": 1,
                "direction": 0
            }
        ]
    }
    myLogger.add_info_to_logger(0, "vehicle_location", data)

    # vehicle 2 position
    stat = random.choice(rightIDs)
    data = {
        "region_id":1, 
        "vehicle_location":[
            {
                "vehicle_id": 2,
                "lat": id2loc[stat][1],
                "lon": id2loc[stat][0],
                "station": stat,
                "status": 1,
                "direction": 0
            }
        ]
    }
    myLogger.add_info_to_logger(0, "vehicle_location", data)

    # order 1 info (left)
    pstat1, dstat1 = random.sample(leftIDs, k=2)
    ptime = random.choice(range(0, 5))
    data = {
        "region_id":1,
        "order_id":f"{prefix}-1", 
        "pax_num":1, 
        "order_time":f"2024-12-24 10:00:{ptime:02d}",
        "available_pickup_station_list":[pstat1],  
        "available_pickup_walkingtime_list":[0], 
        "available_dropoff_station_list":[dstat1],    
        "available_dropoff_walkingtime_list":[0]
    }
    myLogger.add_info_to_logger(ptime, "order", data)

    # order 2 info (left)
    pstat2, dstat2 = random.sample(leftIDs, k=2)
    ptime += random.choice(range(0, 5))
    data = {
        "region_id":1,
        "order_id":f"{prefix}-2", 
        "pax_num":1, 
        "order_time":f"2024-12-24 10:00:{ptime:02d}",
        "available_pickup_station_list":[pstat2],  
        "available_pickup_walkingtime_list":[0], 
        "available_dropoff_station_list":[dstat2],    
        "available_dropoff_walkingtime_list":[0]
    }
    myLogger.add_info_to_logger(ptime, "order", data)

    # order 3 info (right)
    pstat3, dstat3 = random.sample(rightIDs, k=2)
    ptime += random.choice(range(0, 5))
    data = {
        "region_id":1,
        "order_id":f"{prefix}-3", 
        "pax_num":1, 
        "order_time":f"2024-12-24 10:00:{ptime:02d}",
        "available_pickup_station_list":[pstat3],  
        "available_pickup_walkingtime_list":[0], 
        "available_dropoff_station_list":[dstat3],    
        "available_dropoff_walkingtime_list":[0]
    }
    myLogger.add_info_to_logger(ptime, "order", data)

    # order 4 info (right)
    pstat4, dstat4 = random.sample(rightIDs, k=2)
    ptime += random.choice(range(0, 5))
    data = {
        "region_id":1,
        "order_id":f"{prefix}-4", 
        "pax_num":1, 
        "order_time":f"2024-12-24 10:00:{ptime:02d}",
        "available_pickup_station_list":[pstat4],  
        "available_pickup_walkingtime_list":[0], 
        "available_dropoff_station_list":[dstat4],    
        "available_dropoff_walkingtime_list":[0]
    }
    myLogger.add_info_to_logger(ptime, "order", data)

    data = {
        "region_id":1,
        "vehicle_id":1,
        "station_id":pstat1,
        "pickup_order_id":[
            f'{prefix}-1',
        ],
        "dropoff_order_id":[]
    }
    myLogger.add_info_to_logger(60, "vehicle_arrive", data)

    data = {
        "region_id":1,
        "vehicle_id":2,
        "station_id":pstat3,
        "pickup_order_id":[
            f'{prefix}-3',
        ],
        "dropoff_order_id":[]
    }
    myLogger.add_info_to_logger(60, "vehicle_arrive", data)