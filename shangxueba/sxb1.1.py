# 绕过验证码无限次获取上学吧题目答案
# 上学吧网址：https://www.shangxueba.com/ask

import tkinter as tk
import random
import time
import os
import requests
import urllib3
urllib3.disable_warnings() # 这句和上面一句是为了忽略 https 安全验证警告，参考：https://www.cnblogs.com/ljfight/p/9577783.html
from bs4 import BeautifulSoup
import webbrowser
from tkinter import scrolledtext        # 导入滚动文本框的模块
from tkinter import filedialog

def saveClick(filename,txt):
	with open (filename,'w') as f:
		f.write(txt)
		f.close()

def get_question(session, dataid):
	link = "https://m.shangxueba.com/ask/" + dataid + ".html"
	r = session.get(link)
	soup = BeautifulSoup(r.content, "html.parser")
	try:
		description = soup.find(attrs={"name":"description"})['content'] # 抓取题干内容
		if(description and description[0:5] != '上学吧提供'): # 页面错误的话，显示的内容是：上学吧提供考研、公务员、司法、会计、金融等各种资格考试认证学习资料,视频课程,真题,模拟试题分享下载服务和培训服务
			return description
		else:
			return "无法获取题目内容！"
	except: # 有的时候网址出错会弹JavaScript弹框：该问题不存在或未审核
		return "该问题不存在或未审核！"

def get_answer(session, dataid):
	millis = int(round(time.time() * 1000))
	data = {
		"id": dataid,
		"action": "showZuiJia",
		"t": millis
	}
	r = session.post("https://m.shangxueba.com/ask/ask_getzuijia.aspx", data=data) # 核查验证码正确性
	soup = BeautifulSoup(r.content, "html.parser")
	ans = soup.select('.replyCon')
	if(ans):
		images = ans[0].select('img') # 有的题目答案中有图片，例如：https://www.shangxueba.com/ask/9710781.html
		if(images): # 有的答案中图片出错，链接为：http://www.shangxueba.com/exam/images/onErrorImg.jpg
			with open('shangxueba_answer.html','w') as f:
				f.write(str(ans[0]))
				f.close()
				webbrowser.open('shangxueba_answer.html')
				return "答案中有图片，已自动打开答案网页文件。如没有自动打开网页，可以手动打开 shangxueba_answer.html"
		return ans[0].text.strip()
	else:
		return "答案获取失败！请检查链接是否正确。"	
if __name__ == '__main__':
	i=1
	j=1
	root = tk.Tk()
	root.title("上学吧答案神器")
	s = requests.session()
	theLabel = tk.Label(root,text="*"*45 + "\n上学吧答案神器（绕过验证码 + 破解IP限制）\n" + "*"*45).pack(fill=tk.X)
	label1=tk.Label(root,text='请输入链接：\n例如：https://www.shangxueba.com/ask/8952241.html').pack(fill=tk.X)
	e=tk.Entry(root,borderwidth = 3,foreground = 'red',width = 50)
	e.pack(fill=tk.X)
	# 滚动文本框
	scr = scrolledtext.ScrolledText(root)
	scr.pack()
	def put_text_into_file():
		global scr
		a=tk.filedialog.asksaveasfilename(defaultextension=".txt")
		if(a!=''):
			fetched_content = scr.get('1.0', 'end-1c')
			saveClick(a,fetched_content)
	def show(event=None):
		global i
		global j
		global s
		link = e.get().strip() # 过滤首尾的空格
		dataid = link.split("/")[-1].replace(r".html","") # 提取网址最后的数字部分
		ipaddress="%d.%d.%d.%d"%(random.randint(120,125),random.randint(1,200),random.randint(1,200),random.randint(1,200))
		s.headers.update({
			"X-Forwarded-For":ipaddress, # 这一句是整个程序的关键，通过修改 X-Forwarded-For 信息来欺骗 ASP 站点对于 IP 的验证。
                        "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36"
			#"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1", # 这一句非常重要，不然获取不了答案，2019.05.09 更新
		})
		#print(ipaddress)
		if(dataid.isdigit()): # 根据格式，dataid 应该全部为数字，判断字符串是否全部为数字，返回 True 或者 False
			i=j
			answer='\n' + '-'*45 + '\n%d题目：' + get_question(s, dataid) + '\n\n' + get_answer(s, dataid) + '\n' + '-'*45 + '\n'
			answer=answer%i
			e.delete(0, tk.END)
			#label2=tk.Message(root,text=answer).pack(fill=tk.X)
			scr.insert(tk.END,answer)
			scr.see(tk.END)
			i=i+1
			j=j+1
		else:
			answer="\r网址输入有误！请重新输入！"
			i=i+1
			e.insert(0,answer)
			#label2=tk.Message(root,text=answer,fg='red').pack(fill=tk.Y)
	e.bind("<Return>",show)
	tk.Button(root,text = "获取答案",width=10,command=show).pack(side=tk.LEFT,fill=tk.X,padx=20)
	tk.Button(root,text = "查询结果\n保存为文件",width=10,command=put_text_into_file).pack(side=tk.RIGHT,fill=tk.X,padx=20)
	
	root.mainloop()
