data = {
    "region_id":1,
    "order_id":f"10001", 
    "pax_num":1, 
    "order_time":"2023-11-25 09:05:00",
    "available_pickup_station_list":[16],  
    "available_pickup_walkingtime_list":[110], 
    "available_dropoff_station_list":[1],    
    "available_dropoff_walkingtime_list":[120]
}
add_info_to_logger(0, "order", data, logger)


data = {
    "region_id":1,
    "order_id":f"10001",
}
add_info_to_logger(1, "order_cancel", data, logger)

data = {
    "region_id":1,
    "vehicle_id":1,
    "station_id":1,
}
add_info_to_logger(2, "vehicle_arrive", data, logger)

data = {
    "region_id":1, 
    "vehicle_location":[
        {
            "vehicle_id": 1,
            "lat": 28.13814561232112,
            "lon": 112.90367337946118,
            "status": 1,
            "direction": 150
        }
    ]
}
add_info_to_logger(3, "vehicle_location", data, logger)

