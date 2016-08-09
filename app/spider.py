# encoding: utf-8
from bs4 import BeautifulSoup
import re
import requests
import urllib2
import codecs
import pymysql
import urllib

class CJScrap(object):
    def __init__(self, studentID, password):
        self.studentID = studentID
        self.password = password
        #进入MySQL，并选择数据库student
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='516211', db='mysql', charset='utf8mb4')
        self.cur = self.conn.cursor()
        self.cur.execute('USE student')

        #获得headers，Referer参数为上一页面的url
    def getHeaders(self, Referer):
        headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded',
                'Cookie':'_gscu_750909037=15074682dsiqpt59; iPlanetDirectoryPro=AQIC5wM2LY4Sfcy7allyeg8bTwGbxs56kCYwGNYhKYMOT3k%3D%40AAJTSQACMDE%3D%23',
                'Host':'jwxt2.gdufe.edu.cn:8080',
                'Origin':'jwxt2.gdufe.edu.cn:8080',
                'Referer':Referer,
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
            }
        return headers
    def getScore(self):
        #获取URL中的干扰myString,如:(S(tu2ev555t3hct445ra3v2p55))
        mainURL = 'http://jwxt2.gdufe.edu.cn:8080'
        pageURL = mainURL + '/default6.aspx'
        headers = self.getHeaders(pageURL)
        s = requests.Session()
        response = s.get(pageURL, headers=headers)
        #print response.url
        pattern = re.compile(r"/")
        myString = pattern.split(response.url)[3]
        #print myString
        #获得postdata中的__VIEWSTATE,__EVENTVALIDATION
        bsObj = BeautifulSoup(response.text, "lxml")
        __VIEWSTATE = bsObj.find(id="__VIEWSTATE")["value"]
        __EVENTVALIDATION = bsObj.find(id="__EVENTVALIDATION")["value"]
        #构造登录教务系统用的loginPostData字典
        loginPostData = {
                    '__VIEWSTATE':__VIEWSTATE,
                    '__EVENTVALIDATION':__EVENTVALIDATION,
                    'tname':'',
                    'tbtns':'',
                    'tnameXw':'yhdl',
                    'tbtnsXw':'yhdl|xwxsdl',
                    'txtYhm':self.studentID,
                    'txtXm':'111111',
                    'txtMm':self.password,
                    'rblJs':u'学生'.encode('gb2312'),
                    'btnDl':u'登 录'.encode('gb2312')
                }
        #登录进入主界面
        loginURL = mainURL + '/' + myString + '/default6.aspx'
        response = s.post(loginURL, data=loginPostData, headers=headers)
        #print response.url
        #获得学生名称studentName
        bsObj = BeautifulSoup(response.text, "lxml")
        studentInfo = bsObj.find(id="xhxm").string
        studentInfo = studentInfo.replace(' ','')
        studentInfo = studentInfo.replace(self.studentID,'')
        studentName = studentInfo.replace(u'同学','')
        #将utf-8编码的姓名转变为gb2312编码
        urlstudentName = studentName.encode('gb2312')         
        #进入查询成绩页面
        headers = self.getHeaders(response.url)
        params = {'xh':self.studentID, 'xm':urlstudentName, 'gnmkdm':'N121605'}
        cjURL = mainURL + '/' + myString + '/xscjcx_dq.aspx?'
        r = s.get(cjURL, params=params, headers=headers)
        #print r.url
        #获得查询成绩页面的__VIEWSTATE,__EVENTVALIDATION
        bsObj = BeautifulSoup(r.text, "lxml")
        __VIEWSTATE = bsObj.find(id="__VIEWSTATE")["value"]
        __EVENTVALIDATION = bsObj.find(id="__EVENTVALIDATION")["value"]
        #更新headers
        headers = self.getHeaders(cjURL)
        #构造查询所有成绩的post表单的字典
        cjPostData = {
                    '__EVENTTARGET':'',
                    '__EVENTARGUMENT':'',
                    '__LASTFOCUS':'',
                    '__VIEWSTATE':__VIEWSTATE,
                    '__EVENTVALIDATION':__EVENTVALIDATION,
                    'ddlxn':u'全部'.encode('gb2312'),     #全部
                    'ddlxq':u'全部'.encode('gb2312'),     #全部
                    'btnCx':u' 查  询 '.encode('gb2312')  #查询
                }
        #获得包含所有成绩的cjResponse
        cj_all_URL = mainURL + '/' + myString + '/xscjcx_dq.aspx'
        xm = ''
        for item in studentName:
            xm = xm + "%u" + "%x"%ord(item)
        #print 'xm:',xm
        payload = {'xh':self.studentID,'xm':xm,'gnmkdm':'N121605'}
        cjResponse = s.post(cj_all_URL, params=payload, data=cjPostData, headers=headers)
        bsObj = BeautifulSoup(cjResponse.text, "lxml")
        count = 0
        for tag in bsObj.form.table.next_sibling.next_sibling.find_all("td"):
            if count > 16:
                if count%17==0:
                    #学年
                    year = tag.string
                        
                elif count%17==1:
                    #学期
                    term = tag.string

                elif count%17==2:
                    #课程代码
                    code = tag.string

                elif count%17==3:
                    #课程名称
                    title = tag.string

                elif count%17==4:
                    #课程性质
                    cour_character = tag.string

                elif count%17==6:
                    #学分
                    credit = tag.string

                elif count%17==7:
                    #平时成绩
                    mid_score = tag.string
                    if mid_score.isspace():
                        mid_score = '0'

                elif count%17==9:
                    #期末成绩
                    end_score = tag.string

                elif count%17==11:
                    #总成绩
                    fin_score = tag.string

                elif count%17==14:
                    #开课学院
                    college = tag.string
                    self.cur.execute("INSERT INTO scorepages (studentid, year, term, code, title, cour_character, credit, mid_score, end_score, fin_score, college) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)",(self.studentID, year, term, code, title, cour_character, float(credit), float(mid_score), float(end_score), float(fin_score), college))
                    self.conn.commit()
                    pass
            count = count + 1
                
#绩点计算
        #self.cur.execute("SELECT ( ( SUM(credit * fin_score) / SUM(credit) ) / 10.0 ) - 5.0 FROM pages")
        #print "总绩点：" + str(self.cur.fetchone()[0])

        self.cur.close()
        self.conn.close()
        return True


if __name__ == '__main__':
    mycj = CJScrap('14151106132', 'password')
    gemycj = mycj.getScore()



