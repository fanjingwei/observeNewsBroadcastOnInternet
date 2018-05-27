import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import datetime
from datetime import timedelta

def observeBaidu(key, cycle):
	browser = webdriver.Chrome(os.getcwd()+"/3rdParty/chromedriver.exe")
	browser.get("http://www.baidu.com")
	inputElement = browser.find_element_by_id("kw")
	inputElement.send_keys(key)
	inputElement.send_keys(Keys.RETURN)
	time.sleep(10)

	count = 1
	start,end = getNextCycle(cycle, count)
	tryFunctionSomeTime(clickSearchTool, browser, 600)
	num = filterResult(browser,start,end)
	string = "Key word:"+ key + " search by baidu\n" + record(start,end,num) + "\n"
	while num > 0:
		start,end = getNextCycle(cycle, count)
		num = filterResult(browser, start,end)
		string+=record(start,end,num)+"\n"
		print(record(start,end,num)+"\n")
		time.sleep(1)
		count+=1
	browser.close()
	return string

def getNextCycle(cycle, count):
	endDay = datetime.now() - timedelta(days=cycle*(count-1))
	startDay = datetime.now() - timedelta(days=cycle*count)
	start = createDate(startDay)
	end = createDate(endDay)
	return start, end

def createDate(day):
	year = day.year
	month = day.month
	d = day.day
	if month < 10:
		month = "0" + str(month)
	else:
		month = str(month)
	if d < 10:
		d = "0" + str(d)
	else:
		d = str(d)
	return str(year)+"-"+month+"-"+d
	
def filterResult(browser, start, end):
	if not tryFunctionSomeTime(clickTimeFilter, browser, 240):
		return 0xffffffff
	if not tryFunctionSomeTimeTreeParameters(clickTimeFilterSubmit, browser, start, end, 240):
		return 0xffffffff
	r,v = tryFunctionSomeTimeWithReturn(getSearchResultNum, browser, 240)
	if r:
		return v
	else:
		return 0xffffffff

def tryFunctionSomeTime(function, parameter, maxTime):
	for i in range(maxTime):
		try:
			function(parameter)
		except:
			time.sleep(0.5)
		finally:
			return True
	return False

def tryFunctionSomeTimeWithReturn(function, parameter, maxTime):
	for i in range(maxTime):
		try:
			return True, function(parameter)
		except:
			time.sleep(0.5)
	return False, None

def tryFunctionSomeTimeTreeParameters(function, para1, para2, para3, maxTime):
	for i in range(maxTime):
		try:
			function(para1, para2, para3)
		except:
			time.sleep(0.5)
		finally:
			return True
	return False

def clickSearchTool(browser):
	searchTool = browser.find_element_by_class_name("search_tool")
	if not searchTool.is_displayed():
		searchTool = undefineWord#不可见时也能查到，因此此时要主动造成异常，等待其可见
	searchTool.click()
	return

def clickTimeFilter(browser):
	searchTool_Time = browser.find_element_by_class_name("search_tool_tf")
	if not searchTool_Time.is_displayed():
		searchTool_Time = undefineWord#不可见时也能查到，因此此时要主动造成异常，等待其可见
	searchTool_Time.click()
	return

def clickTimeFilterSubmit(browser, start, end):
	startTime = browser.find_element_by_name("st")
	startTime.clear()
	startTime.send_keys(start)
	endTime = browser.find_element_by_name("et")
	endTime.clear()
	endTime.send_keys(end)
	submit = browser.find_element_by_class_name("c-tip-custom-submit")
	submit.click()

def getSearchResultNum(browser):
	resultNum = browser.find_element_by_class_name("nums_text")
	result = resultNum.get_attribute("innerHTML")
	startPos = len('百度为您找到相关结果约')
	endPos = result.find('个')
	return int(result[startPos:endPos].replace(',',""))

def grabNumFromString(string, startStr, endStr):
	startPos = len(startStr)
	endPos = string.find(endStr)
	return int(string[startPos:endPos].replace(',',""))

def record(start, end, num):
	return start + "~" + end + ":" + str(num)

def observeSina(key, cycle):
	browser = webdriver.Chrome(os.getcwd()+"/3rdParty/chromedriver.exe")
	count = 1
	start,end = getNextCycle(cycle, count)
	num = oneSinaSearch(browser, key, start, end)
	count+=1
	string = "Key word:"+ key + " search by sina\n" + record(start,end,num) + "\n"
	while num > 0:
		start,end = getNextCycle(cycle, count)
		num = oneSinaSearch(browser, key, start, end)
		string+=record(start,end,num)+"\n"
		print(record(start,end,num))
		count+=1
		time.sleep(1)
	browser.close()
	return string

def oneSinaSearch(browser, key, start, end):
	browser.get("http://search.sina.com.cn/?c=adv")
	inputElement = browser.find_element_by_name("all")
	inputElement.send_keys(key)
	selectItem = browser.find_element_by_name("time")
	Select(selectItem).select_by_value("custom")
	startTime = browser.find_element_by_id("s_time")
	startTime.send_keys(start)
	endTime = browser.find_element_by_id("e_time")
	endTime.send_keys(end)
	time.sleep(1)
	submit = browser.find_element_by_id("submit_button")
	submit.click()
	result = browser.find_element_by_class_name("l_v2")
	num = int(grabNumFromString(result.text, "找到相关新闻", "篇"))
	mod_bar = browser.find_element_by_class_name("mod_bar")
	if 0 == len(mod_bar.find_elements_by_class_name("close")):
		return num
	else:
		return 0