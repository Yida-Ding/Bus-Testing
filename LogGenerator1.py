import logging
import json
from datetime import datetime
import time
import random

# prepare station location
with open("data/static_3.json", 'r', encoding='utf-8') as outfile:
    stat_dict = json.load(outfile)["stations"]
ids = [dic["station_id"] for dic in stat_dict]
locBD = [(dic["station_lon"], dic["station_lat"]) for dic in stat_dict]
id2loc = {ids[i]: locBD[i] for i in range(len(ids))}

# region1 (left, right) station IDs
# leftIDs = [26, 11, 13, 9, 19, 25, 1, 18, 28, 91, 27, 22, 129, 113, 2, 14, 16, 15, 21]
# rightIDs = [106, 114, 107, 100, 101, 98, 102, 127, 128, 126, 105, 125, 108, 99]
leftIDs = [2, 15, 22, 99, 100, 101, 102, 105, 108, 114, 126, 129, 145, 146]
rightIDs = [98, 147, 148, 149, 150, 151, 152]


class Logger:
    def __init__(self, filename:str):
        """
        initialize the logger file
        """
        # 创建Logger对象并设置输出格式
        self.logger = logging.getLogger(f'filename')
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


def create_instance(config):
    """
    create testing instance
    """
    test_id = config["TEST_ID"]
    prefix = f"TESTP-{test_id}"
    myLogger = Logger(f"logs/log_{test_id}")

    veh_id = 1
    for _ in range(config["NUM_LEFT_VEHS"]):
        stat = random.choice(leftIDs)
        data = {
            "region_id":1, 
            "vehicle_location":[
                {
                    "vehicle_id": veh_id,
                    "lat": id2loc[stat][1],
                    "lon": id2loc[stat][0],
                    "station": stat,
                    "status": 1,
                    "direction": 0
                }
            ]
        }
        veh_id += 1
        myLogger.add_info_to_logger(0, "vehicle_location", data)

    for _ in range(config["NUM_RIGHT_VEHS"]):
        stat = random.choice(rightIDs)
        data = {
            "region_id":1, 
            "vehicle_location":[
                {
                    "vehicle_id": veh_id,
                    "lat": id2loc[stat][1],
                    "lon": id2loc[stat][0],
                    "station": stat,
                    "status": 1,
                    "direction": 0
                }
            ]
        }
        veh_id += 1
        myLogger.add_info_to_logger(0, "vehicle_location", data)
    
    ptime = 0
    ord_id = 1    
    for _ in range(config["NUM_LEFT_ORDERS"]):
        pstat, dstat = random.sample(leftIDs, k=2)
        ptime += random.choice(range(0, 5))
        data = {
            "region_id":1,
            "order_id":f"{prefix}-{ord_id}", 
            "pax_num":1, 
            "order_time":f"2025-01-06 13:00:{ptime:02d}",
            "available_pickup_station_list":[pstat],  
            "available_pickup_walkingtime_list":[0], 
            "available_dropoff_station_list":[dstat],    
            "available_dropoff_walkingtime_list":[0]
        }
        ord_id += 1
        myLogger.add_info_to_logger(ptime, "order", data)

    for _ in range(config["NUM_RIGHT_ORDERS"]):
        pstat, dstat = random.sample(rightIDs, k=2)
        ptime += random.choice(range(0, 5))
        data = {
            "region_id":1,
            "order_id":f"{prefix}-{ord_id}", 
            "pax_num":1, 
            "order_time":f"2025-01-06 13:00:{ptime:02d}",
            "available_pickup_station_list":[pstat],  
            "available_pickup_walkingtime_list":[0], 
            "available_dropoff_station_list":[dstat],    
            "available_dropoff_walkingtime_list":[0]
        }
        ord_id += 1
        myLogger.add_info_to_logger(ptime, "order", data)

    del myLogger

    # # cancel order 1
    # data = {
    #     "region_id":1,
    #     "order_id":f"{prefix}-1"
    # }
    # ptime += random.choice(range(0, 5))
    # myLogger.add_info_to_logger(ptime, "order_cancel", data)

    # # cancel order NL+1
    # can_ord = config["NUM_LEFT_ORDERS"] + 1
    # data = {
    #     "region_id":1,
    #     "order_id":f"{prefix}-{can_ord}"
    # }
    # ptime += random.choice(range(0, 5))
    # myLogger.add_info_to_logger(ptime, "order_cancel", data)

if __name__ == '__main__':

    config = \
    {
        "TEST_ID": 65,
        "NUM_LEFT_VEHS": 2,
        "NUM_RIGHT_VEHS": 3,
        "NUM_LEFT_ORDERS": 5,
        "NUM_RIGHT_ORDERS": 5,
    }

    create_instance(config)
