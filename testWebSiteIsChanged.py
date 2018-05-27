import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import unittest

class WebSiteTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Chrome(os.getcwd()+"/3rdParty/chromedriver.exe")
		return

	def tearDown(self):
		self.browser.close()
		return

	def testBaiduSearch(self):
		self.browser.get("http://www.baidu.com")
		inputElement = self.browser.find_element_by_id("kw")
		self.assertNotEqual(None, inputElement)
		inputElement.send_keys("范璟玮")
		inputElement.send_keys(Keys.RETURN)
		time.sleep(1)

		num = self.browser.find_elements_by_class_name("nums_text")
		self.assertEqual(1,len(num))
		searchTool = self.browser.find_element_by_class_name("search_tool")
		self.assertNotEqual(None, searchTool)
		searchTool.click()
		time.sleep(1)

		searchTool_Time = self.browser.find_element_by_class_name("search_tool_tf")
		self.assertNotEqual(None, searchTool_Time)
		searchTool_Time.click()
		time.sleep(1)

		startTime = self.browser.find_elements_by_name("st")
		self.assertEqual(1,len(startTime))
		startTime[0].clear()
		startTime[0].send_keys("2015-08-15")
		endTime = self.browser.find_elements_by_name("et")
		self.assertEqual(1,len(endTime))
		endTime[0].clear()
		endTime[0].send_keys("2015-08-30")
		submit = self.browser.find_element_by_class_name("c-tip-custom-submit")
		self.assertNotEqual(None, submit)
		submit.click()
		time.sleep(1)

		results = self.browser.find_elements_by_class_name("result")
		self.assertEqual(2,len(results))
		resultNum = self.browser.find_element_by_class_name("nums_text")
		#该项此时被隐藏，需要使用get_attribute("innerHTML")方式获取
		self.assertEqual("百度为您找到相关结果约2个",resultNum.get_attribute("innerHTML"))

	def testSinaSearch(self):
		self.browser.get("http://search.sina.com.cn/?c=adv")
		inputElement = self.browser.find_element_by_name("all")
		self.assertNotEqual(None, inputElement)
		inputElement.send_keys("区块链")
		selectItem = self.browser.find_element_by_name("time")
		self.assertNotEqual(None, selectItem)
		Select(selectItem).select_by_value("custom")
		startTime = self.browser.find_element_by_id("s_time")
		self.assertNotEqual(None, startTime)
		startTime.send_keys("2018-05-23")
		endTime = self.browser.find_element_by_id("e_time")
		self.assertNotEqual(None, endTime)
		endTime.send_keys("2018-05-24")
		submit = self.browser.find_element_by_id("submit_button")
		self.assertNotEqual(None, submit)
		submit.click()
		r = self.browser.find_element_by_class_name("l_v2")
		self.assertNotEqual(None, r)


if __name__ == '__main__':
	unittest.main()