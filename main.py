from LogGenerator1 import create_instance
from LogExecutor import execute_log_file
from collections import defaultdict
from pandas import DataFrame
import requests
import json


server = "http://121.199.173.212:8031"
# server = "https://dispatch.zex-t.cn:8031"


def clear_orders():
    headers = {'Content-Type': 'application/json', 'token':'222'}

    response = requests.get(f'{server}/order-list/1', headers=headers)
    res = json.loads(response.text)
    ord_ids = [row['order_id'] for row in res["data"]]

    data = {
        "region_id":1, 
        "ids": ord_ids,
    }
    response = requests.post(f"{server}/order/batch-cancel", headers=headers, json=data)
    print(f"{response.text}")

def analyze_results(config, test_range, sum_name):
    instances = [f"res_{i}" for i in range(*test_range)]
    Nveh = config["NUM_LEFT_VEHS"] + config["NUM_RIGHT_VEHS"]
    Nord = config["NUM_LEFT_ORDERS"] + config["NUM_RIGHT_ORDERS"]
    resd = defaultdict(list)
    for instance in instances:
        resd["instance"].append(instance)
        resd["vehicles"].append(Nveh)
        resd["input_orders"].append(Nord)

        with open(f"results/{instance}.txt", "r") as file:
            lines = file.readlines()  # Read all lines into a list
            last_line = lines[-1] if lines else ""  # Get the last line, or empty string if file is empty
            res = float(last_line)
            resd["success_orders"].append(res)
            resd["success_rate"].append(res/Nord)
    
    df = DataFrame(resd)
    df.to_csv(f"results/{sum_name}.csv", index=None)


if __name__ == '__main__':

    test_range = (21, 31)

    config = \
        {
            "TEST_ID": None,
            "NUM_LEFT_VEHS": 2,
            "NUM_RIGHT_VEHS": 2,
            "NUM_LEFT_ORDERS": 7,
            "NUM_RIGHT_ORDERS": 7,
        }

    for test_id in range(*test_range):
        config_c = config.copy()
        config_c["TEST_ID"] = test_id
        clear_orders()
        create_instance(config_c)
        execute_log_file(test_id)

    analyze_results(config, test_range, "summary_3")
