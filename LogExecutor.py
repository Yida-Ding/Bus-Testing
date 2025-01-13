import logging
import requests
import time
from threading import Thread

headers = {'Content-Type': 'application/json', 'token':'222'}

def execute_log_file(testID, reg_id=1):
    """
    read the log file by line
    """

    server = "http://121.199.173.212:8031"
    # server = "https://dispatch.zex-t.cn:8031"

    f = open(f"results/res_{testID}.txt", 'a')
    start = time.time()

    with open(f"logs/log_{testID}.json", 'r') as file:
        lastsec = 0
        for row in file.readlines():
            row = eval(row)
            cursec = row["sec"]
            action = row["action"]
            data = row["data"]
            time.sleep(cursec - lastsec)
            print(f"Time={time.time()-start: .1f}", file=f)

            if action == "vehicle_location":
                response = requests.post(f"{server}/vehicle/location", headers=headers, json=data)
                print(action, response.text, file=f)

            elif action == "order":
                response = requests.post(f"{server}/order", headers=headers, json=data)
                print(action, response.text, file=f)

            elif action == "order_cancel":
                response = requests.post(f"{server}/order/cancel", headers=headers, json=data)
                print(action, response.text, file=f)

            elif action == "vehicle_arrive":
                response = requests.post(f"{server}/vehicle/arrive", headers=headers, json=data)
                print(action, response.text, file=f)
        
            lastsec = cursec

            response = requests.get(f'{server}/all-dispatch/{reg_id}', headers=headers)
            print("feedback", response.text, file=f)
            print(file=f)
        
        time.sleep(5)
        response = requests.get(f'{server}/all-dispatch/{reg_id}', headers=headers)
        print("feedback", response.text, file=f)
        print(response.text)

        time.sleep(10)
        response = requests.get(f'{server}/all-dispatch/{reg_id}', headers=headers)
        print("feedback", response.text, file=f)
        print(response.text)

        # Initialize an empty set to store the order_ids
        order_ids = set()

        # Loop through each vehicle and its related orders

        for vehicle in eval(response.text)["data"]["vehicle_dispatch"]:
            for station_related_orders in vehicle["station_related_orders_list"]:
                for order in station_related_orders:
                    order_id = order.get("order_id")
                    if order_id and order_id.startswith("TEST"):
                        order_ids.add(order_id)

        # Print the set of order_ids
        print(file=f)
        print(len(order_ids), file=f)

if __name__ == '__main__':

    execute_log_file("1")
    

    # thread1 = Thread(target=execute_log_file, args=("R1-30", 1))  
    # thread2 = Thread(target=execute_log_file, args=("R2-30", 2)) 
    # thread3 = Thread(target=execute_log_file, args=("R3-30", 3))  

    # thread1.start()  # 线程1开始
    # thread2.start()  # 线程2开始
    # thread3.start()  # 线程3开始
    
    # thread1.join()  # 等待线程1结束
    # thread2.join()  # 等待线程2结束
    # thread3.join()  # 等待线程3结束