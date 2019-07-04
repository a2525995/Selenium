# -*- coding: utf-8 -*-
from splinter.browser import Browser
from time import sleep
import traceback
import time, sys

class huoche(object):
	"""docstring for huoche"""
	driver_name=''
	executable_path=''
	#用户名，密码
	username = u''
	passwd = u''
	# cookies值得自己去找, 下面两个分别是北京, 郑州
	starts = u'%u5317%u4EAC%u897F%2CBXP'
	ends = u'%u6708%u5C71%2CYBF'
	# 时间格式2018-01-19
	dtime = u'2018-02-09'
	#车次类型 G D Z T K QT
	train_type = ''
	# 车次，选择第几趟，0则从上之下依次点击
	order = 10
	###乘客名
	users = [u'', u'']
	##席位
	# 0 二等座  1 一等座  2 商务座
	# 0 硬卧  1 硬座  2 软卧
	xb = 0

	# 座位号 1A 1B 1C   1D 1F
	seat_num = '1F'

	pz=u'成人票'

	"""网址"""
	ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
	login_url = 'https://kyfw.12306.cn/otn/login/init'
	initmy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
	buy='https://kyfw.12306.cn/otn/confirmPassenger/initDc'
	login_url='https://kyfw.12306.cn/otn/login/init'
	
	def __init__(self):
		self.driver_name='chrome'
		self.executable_path='/usr/bin/chromedriver'

	def login(self):
		self.driver.visit(self.login_url)
		self.driver.fill('loginUserDTO.user_name', self.username)
		# sleep(1)
		self.driver.fill('userDTO.password', self.passwd)
		print(u'等待验证码，自行输入...')
		while True:
			if self.driver.url != self.initmy_url:
				sleep(1)
			else:
				break

	def start(self):
		self.driver=Browser(driver_name=self.driver_name,executable_path=self.executable_path)
		self.driver.driver.set_window_size(1400, 1000)
		self.login()
		# sleep(1)
		self.driver.visit(self.ticket_url)
		try:
			print(u'购票页面开始...')
			# sleep(1)
			# 加载查询信息
			self.driver.cookies.add({'_jc_save_fromStation': self.starts})
			self.driver.cookies.add({'_jc_save_toStation': self.ends})
			self.driver.cookies.add({'_jc_save_fromDate': self.dtime})

			self.driver.reload()

			#选择车次类型 高铁 动车
			if self.train_type != '':
				self.driver.find_by_xpath('//input[@value="'+self.train_type+'"]').click()

			count=0
			if self.order!=0:
				while self.driver.url==self.ticket_url:
					self.driver.find_by_text(u'查询').click()
					count += 1
					print(u'单次循环点击查询... 第 %s 次' % count)
					# sleep(1)
					try:
						self.driver.find_by_text(u'预订')[self.order - 1].click()
					except Exception as e:
						# print(e)
						print(u'抢票未开始')
						continue
			else:
				while self.driver.url == self.ticket_url:
					self.driver.find_by_text(u'查询').click()
					count += 1
					print(u'列表循环点击查询... 第 %s 次' % count)
					# sleep(0.8)
					try:
						for i in self.driver.find_by_text(u'预订'):
							i.click()
							sleep(1)
					except Exception as e:
						# print(e)
						print(u'抢票未开始 %s' %count)
						continue
			print(u'开始预订...')
			# sleep(3)
			# self.driver.reload()
			sleep(1)
			print(u'开始选择用户...')
			for user in self.users:
				self.driver.find_by_text(user).last.click()
			
			print(u'开始选择席位...')
			self.driver.find_by_id('seatType_1').find_by_tag('option')[self.xb].click()
			# self.driver.find_by_text(self.pz).click()
			# self.driver.find_by_id('').select(self.pz)
			# sleep(1)
			# self.driver.find_by_text(self.xb).click()
			# sleep(1)

			print(u'提交订单...')
			self.driver.find_by_id('submitOrder_id').click()

			if self.train_type == 'G':
				print(u'开始选择座位...')
				# sleep(5)
				# self.driver.find_by_id('1D').click()
				# self.driver.find_by_id('erdeng1').last.click()
				self.driver.find_by_xpath('//div[@id="erdeng1"]').find_by_id(self.seat_num).click()
				print(u'确认选择座位号为' + self.seat_num + '...')
				print(u'确认订单')
			else:
				print(u'确认订单')
			sleep(1.5)
			self.driver.find_by_id('qr_submit_id').click()
			print(u'购票成功...')

		except Exception as e:
			print(e)

if __name__ == '__main__':
	huoche=huoche()
	huoche.start()
