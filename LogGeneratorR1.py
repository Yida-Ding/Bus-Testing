import logging
import json
from datetime import datetime
import time
import random
import gc

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


def create_instance(config, reg_id):
    """
    create testing instance
    """
    # prepare station location
    with open(f"data/static_R{reg_id}.json", 'r', encoding='utf-8') as outfile:
        stat_dict = json.load(outfile)["stations"]
    ids = [dic["station_id"] for dic in stat_dict]
    locBD = [(dic["station_lon"], dic["station_lat"]) for dic in stat_dict]
    id2loc = {ids[i]: locBD[i] for i in range(len(ids))}

    test_id = config["TEST_ID"]
    prefix = f"TEST-{test_id}"
    myLogger = Logger(f"logs/log_{test_id}")

    veh_id = 1
    for _ in range(config["NUM_VEHS"]):
        stat = random.choice(ids)
        data = {
            "region_id":reg_id, 
            "vehicle_location":[
                {
                    "vehicle_id": veh_id,
                    "lat": id2loc[stat][1],
                    "lon": id2loc[stat][0],
                    "station": stat,
                    "status": 1,
                    "direction": -1
                }
            ]
        }
        veh_id += 1
        myLogger.add_info_to_logger(0, "vehicle_location", data)
    
    ptime = 0
    ord_id = 1    
    for _ in range(config["NUM_ORDERS"]):
        pstat, dstat = random.sample(ids, k=2)
        data = {
            "region_id":reg_id,
            "order_id":f"{prefix}-{ord_id}", 
            "pax_num":1, 
            "order_time":f"2025-01-07 12:00:{ptime:02d}",
            "available_pickup_station_list":[pstat],  
            "available_pickup_walkingtime_list":[0], 
            "available_dropoff_station_list":[dstat],    
            "available_dropoff_walkingtime_list":[0]
        }
        ord_id += 1
        myLogger.add_info_to_logger(ptime, "order", data)

    del myLogger

if __name__ == '__main__':

    for n_ord in range(10, 20, 10):
        for rg in range(1, 2):

            config = \
            {
                "TEST_ID": f"R{rg}-{n_ord}",
                "NUM_VEHS": 5,
                "NUM_ORDERS": n_ord,
            }

            create_instance(config, rg)
