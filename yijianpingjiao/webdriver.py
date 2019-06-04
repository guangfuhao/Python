from selenium import webdriver
import time

'''
**********************************
*************By:BITHGF************
*************2019-6-4*************
***************V0.0***************
'''


class Login(object):
	def __init__(self):
		self.headers={
			'Host': 'login.bit.edu.cn',
			'Origin': 'https://login.bit.edu.cn',
			'Referer': 'https://login.bit.edu.cn/cas/login?service=http%3A%2F%2Fjwms.bit.edu.cn%2F',
			'User-Agent': 'Mozilla/6.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
		}
		self.post_url='https://login.bit.edu.cn/cas/login?service=http%3A%2F%2Fjwms.bit.edu.cn%2F'
		self.ticket_url='http://jwms.bit.edu.cn/?ticket=ST-817724-UHtxCsFcjeOzOpeK9RqW-44lL-cas-1559639201964'
		self.logined_url='http://jwms.bit.edu.cn/jsxsd/framework/main.jsp'

if __name__ == '__main__':
	print('*********************************')
	username=str(input("请输入用户名："))
	print('*********************************')
	password=str(input("请输入密码："))
	print('*********************************')
	rank=int(input("请输入评教等级：（1，2，3，4，5分别对应从好到差）"))
	while (rank<1 or rank>5):
		print("评教等级输入错误，请重新输入")
		rank=input("请输入评教等级：（1，2，3，4，5分别对应从好到差）")
	print('*********************************')
	print('正在自动评教中....................')
	i=0
	driver=webdriver.Chrome()
	login=Login()
	driver.get(login.post_url)
	input1=driver.find_element_by_id('username')
	input1.send_keys(username)
	input1=driver.find_element_by_id('password')
	input1.send_keys(password)
	driver.find_element_by_xpath(".//form//li[@class='btn_image']/input").click()
	driver.find_element_by_xpath(".//div[@class='Nsb_menu menu_cn']//li[@title='教学评价']/a").click()
	driver.find_element_by_xpath(".//div[@class='Nsb_layout_r']/input").click()
	time.sleep(4)
	n = driver.window_handles
	driver.switch_to.window (n[1])
	driver.get('http://pj.bit.edu.cn:8080/pjxt2.0/stpj/queryListStpj')
	time.sleep(2)
	ranks=[1,2,3,4,5]
	rank=rank-1
	'''
	获取当前的句柄并打印窗口值
	current_window = driver.current_window_handle
	print(current_window, driver.title)
	'''
	#driver.find_element_by_xpath(".//a[@class='J_menuItem']").click()
	nextpages=driver.find_element_by_xpath(".//font[@color='red']").text
	page_number=int(nextpages)//10+1
	#print(page_number)
	num=0
	page_num=len(driver.find_elements_by_xpath(".//a[@class='btn btn-mini btn-purple']/i"))
	while(page_num!=0):
		button=driver.find_elements_by_xpath(".//a[@class='btn btn-mini btn-purple']/i")
		if button[0].text=='查看':
			num=num+1
			#print(i.text)
		else:
			driver.find_elements_by_xpath(".//a[@class='btn btn-mini btn-purple']")[num].click()
			for row in range(1,9):
				driver.find_element_by_id("pjnr_{:.0f}_{:.0f}".format(row,ranks[rank])).click()
				#time.sleep(1)
			driver.find_elements_by_xpath(".//a[@class='btn btn-warning']")[0].click()
			#time.sleep(1)
			driver.find_element_by_xpath(".//a[@class='btn btn-primary']").click()
			#time.sleep(1)
		num=0
		driver.find_element_by_xpath(".//a[@class='chzn-single chzn-default']").click()
		driver.find_element_by_id("ztTab_chzn_o_3").click()
		driver.find_element_by_xpath(".//button[@class='btn btn-mini btn-info editm_search']").click()
		page_num=len(driver.find_elements_by_xpath(".//a[@class='btn btn-mini btn-purple']/i"))
	print("全部评教成功！！！")
