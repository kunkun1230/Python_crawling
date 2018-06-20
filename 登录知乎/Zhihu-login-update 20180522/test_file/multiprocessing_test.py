# -*- coding: utf-8 -*-
"""
Created on Sun May 13 14:49:04 2018

@author: lenovo
"""

import multiprocessing
import time

#def func(msg):
#    print('msg:',msg)
#    time.sleep(2)
#    print('********')
#    return ('func_return:%s'%msg)
#
#if __name__=='__main__':
## apply
#    print('\n--------apply------------')
#    pool = multiprocessing.Pool(processes=4)
#    results = []
#    start_time=time.time()
#    for i in range(10):
#        msg = 'hello world %d' % i
#        result = pool.apply(func, (msg,))
#        results.append(result)
#    print('apply: 堵塞')  # 执行完func才执行该句
#    pool.close()
#    pool.join()  # join语句要放在close之后
#    print(results)
#    print("运行时间",time.time()-start_time)
    
# apply_async
#    print('\n--------apply_async------------')
#    pool = multiprocessing.Pool(processes=4)
#    results = []
#    start_time=time.time()
#    for i in range(10):
#        msg = 'hello world %d' % i
#        result = pool.apply_async(func, (msg, ))
#        results.append(result)
#    print('apply_async: 不堵塞')
#
#    for i in results:
#        i.wait()  # 等待进程函数执行完毕
#
#    for i in results:
#        if i.ready():  # 进程函数是否已经启动了
#            if i.successful():  # 进程函数是否执行成功
#                print(i.get())  # 进程函数返回值
#    print("运行时间",time.time()-start_time)

def worker_1(interval):
    print("worker_1")
    time.sleep(interval)
    print ("end worker_1")

def worker_2(interval):
    print ("worker_2")
    time.sleep(interval)
    print ("end worker_2")

def worker_3(interval):
    print("worker_3")
    time.sleep(interval)
    print("end worker_3")

if __name__ == "__main__":
    start_time=time.time()
    pool = multiprocessing.Pool(processes=1)
    p1 = pool.apply(worker_1, args = (2,))
    p2 = pool.apply(worker_2, args = (3,))
    p3 = pool.apply(worker_3, args = (4,))

#    p1.start()
#    p2.start()
#    p3.start()

    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
    print("END!!!!!!!!!!!!!!!!!")
    print(time.time()-start_time)