from time import sleep

from scheduler import Scheduler
from db import MongoClient, MysqlClient,RedisClient
import multiprocessing
import threading

def main():
    s = Scheduler()
    print('程序开始运行。。')
    s.run()

if __name__ == '__main__':
    # for i in range(15):
    #     p = multiprocessing.Process(target=main)
    #     p.start()
    main()
