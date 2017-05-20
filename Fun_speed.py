#coding=utf-8

import RPi.GPIO as GPIO
import time
import redis

import threading
#Timer（定时器）是Thread的派生类，
#用于在指定时间后调用一个方法

INTO = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(INTO, GPIO.IN)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)

N=1.021
global wheel #记录U型测速模块的次数
wheel = 0

def Count(self):
	global wheel
	wheel+=1

def flash(): 
	#轮子直径*3.14/20格码盘=6.5Cm*3.14/20约=1.021cm  即一个脉冲走约1CM距离
	#(count*1.021)/T cm/s= count*2.041 cm/s		取0.5S	
	global wheel
	vel=2.041*wheel
	r.set('speed',vel)
	#print sp
	print("速度为 {0},{1}".format(vel,"cm/s"))
	wheel = 0
	timer = threading.Timer(0.5, flash)
	timer.start()

try:

	wd=r.get('status')
	
	while wd<>'q':

		GPIO.add_event_detect(INTO, GPIO.RISING, callback=Count)
		#event_detected()函数被设计用来在循环中使用,
		#不同于polling轮询, 当CPU忙于其它事时, 不会错过引脚状态的改变
		'''		
		t=time.time()
		T=t-s

		if T==0.5:
			flash()
		'''		
		timer = threading.Timer(0.5, flash)
		timer.start()
except Exception, e:
	print "Sorry for the error, I may suspend this service for you"
	r.set('print','speed is wrong')
