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
# leftIDs = [26, 11, 13, 9, 19, 25, 1, 18, 28, 91, 27, 22, 129, 113, 2, 14, 16, 15, 21]
# rightIDs = [106, 114, 107, 100, 101, 98, 102, 127, 128, 126, 105, 125, 108, 99]
leftIDs = [11, 13, 2, 129, 15, 22, 21, 105, 126]
rightIDs = [145, 114, 151, 100, 101, 152, 146, 98, 102, 147, 148, 150, 99, 108, 149]

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
    
    test_id = 39
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
    pstat = random.choice(leftIDs)
    dstat = random.choice(leftIDs)
    ptime = random.choice(range(0, 5))
    data = {
        "region_id":1,
        "order_id":f"{prefix}-1", 
        "pax_num":1, 
        "order_time":f"2024-01-01 09:00:{ptime:02d}",
        "available_pickup_station_list":[pstat],  
        "available_pickup_walkingtime_list":[0], 
        "available_dropoff_station_list":[dstat],    
        "available_dropoff_walkingtime_list":[0]
    }
    myLogger.add_info_to_logger(ptime, "order", data)

    # order 2 info (left)
    pstat = random.choice(leftIDs)
    dstat = random.choice(leftIDs)
    ptime += random.choice(range(0, 5))
    data = {
        "region_id":1,
        "order_id":f"{prefix}-2", 
        "pax_num":1, 
        "order_time":f"2024-01-01 09:00:{ptime:02d}",
        "available_pickup_station_list":[pstat],  
        "available_pickup_walkingtime_list":[0], 
        "available_dropoff_station_list":[dstat],    
        "available_dropoff_walkingtime_list":[0]
    }
    myLogger.add_info_to_logger(ptime, "order", data)
    

    # order 3 info (right)
    pstat = random.choice(rightIDs)
    dstat = random.choice(rightIDs)
    ptime += random.choice(range(0, 5))
    data = {
        "region_id":1,
        "order_id":f"{prefix}-3", 
        "pax_num":1, 
        "order_time":f"2024-01-01 09:00:{ptime:02d}",
        "available_pickup_station_list":[pstat],  
        "available_pickup_walkingtime_list":[0], 
        "available_dropoff_station_list":[dstat],    
        "available_dropoff_walkingtime_list":[0]
    }
    myLogger.add_info_to_logger(ptime, "order", data)

    # order 4 info (right)
    pstat = random.choice(rightIDs)
    dstat = random.choice(rightIDs)
    ptime += random.choice(range(0, 5))
    data = {
        "region_id":1,
        "order_id":f"{prefix}-4", 
        "pax_num":1, 
        "order_time":f"2024-01-01 09:00:{ptime:02d}",
        "available_pickup_station_list":[pstat],  
        "available_pickup_walkingtime_list":[0], 
        "available_dropoff_station_list":[dstat],    
        "available_dropoff_walkingtime_list":[0]
    }
    myLogger.add_info_to_logger(ptime, "order", data)

    # cancel order 1
    data = {
        "region_id":1,
        "order_id":f"{prefix}-1"
    }
    ptime += random.choice(range(0, 5))
    myLogger.add_info_to_logger(ptime, "order_cancel", data)

    # cancel order 3
    data = {
        "region_id":1,
        "order_id":f"{prefix}-3"
    }
    ptime += random.choice(range(0, 5))
    myLogger.add_info_to_logger(ptime, "order_cancel", data)


