from threading import Thread
import time
from time import sleep
 
import gc
for i in range(10):
    gc.collect()  # 强制垃圾回收
    print(i)
