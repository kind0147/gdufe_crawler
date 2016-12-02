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
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='password', db='mysql', charset='utf8mb4')
        self.cur = self.conn.cursor()
        self.cur.execute('USE student')

        #获得headers，Referer参数为上一页面的url
    def getHeaders(self, Referer, JSESSIONID):
        headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded',
                'Cookie':'_gscu_750909037=15074682dsiqpt59; JSESSIONID='+JSESSIONID,
                'Host':'jwxt.gdufe.edu.cn',
                'Origin':'http://jwxt.gdufe.edu.cn',
                'Referer':Referer,
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
            }
        return headers
    def getScore(self):
        #获取URL中的干扰myString,如:(S(tu2ev555t3hct445ra3v2p55))
        mainURL = 'http://jwxt.gdufe.edu.cn'
        pageURL = mainURL + '/jsxsd'
        s = requests.Session()
        headers = self.getHeaders(pageURL) 
        #构造登录教务系统用的loginPostData字典
        loginPostData = {
                    'USERNAME':self.studentID,
                    'PASSWORD':self.password,
                }
        #登录进入主界面
        loginURL = mainURL + '/jsxsd/xk/LoginToXk'
        #获取cookie中的JSESSIONID
        response = s.get(pageURL)
        set_cookie = response.headers['set-cookie']
        jsessionid = set_cookie.split(';')[0]
        jsessionid = jsessionid.split('=')[-1]
        
        headers = self.getHeaders(pageURL, jsessionid) 
        
        response = s.post("http://jwxt.gdufe.edu.cn/jsxsd/xk/LoginToXkLdap", data=loginPostData, headers=headers)
        print response
        
        mainpageURL = pageURL + '/framework/xsMain.jsp'
        headers = self.getHeaders(mainpageURL, jsessionid)
        scorepageURL = pageURL + '/kscj/cjcx_query?Ves632DSdyV=NEW_XSD_XJCJ'
        mainPAGE = s.get(scorepageURL)
        print mainPAGE

        headers = self.getHeaders(scorepageURL, jsessionid)
        checkFORM = {
                'kksj':'',
                'kcxz':'',
                'kcmc':'',
                'fxkc':'0',
                'xsfs':'all'
                }
        checkscoreURL = pageURL + '/kscj/cjcx_list'
        cjResponse = s.post(checkscoreURL, data=checkFORM, headers=headers)
        bsObj = BeautifulSoup(cjResponse.text, "lxml")
        dataList = bsObj.find(id='dataList')
        #print dataList.text
        score_tank = []
        scoreInfo = {
                'studentID':'',
                'year':'',
                'term':'',
                'code':'',
                'title':'',
                'credit':'',
                'cour_character':'',
                'fin_score':'',
                'cour_attribute':''
                }
        for tag in dataList.find_all('tr'):
            if not tag.th:
                yearterm = tag.find_all('td')[1].string.split('-')
                year = yearterm[0] + '-' + yearterm[1]
                scoreInfo['studentID'] = self.studentID
                scoreInfo['year'] = year

                term = yearterm[2]
                scoreInfo['term'] = term

                code = tag.find_all('td')[2].string
                scoreInfo['code'] = code

                title = tag.find_all('td')[3].string
                scoreInfo['title'] = title

                fin_score = tag.find_all('td')[4].a.string
                scoreInfo['fin_score'] = fin_score

                credit = tag.find_all('td')[5].string
                scoreInfo['credit'] = credit

                cour_character = tag.find_all('td')[8].string
                scoreInfo['cour_character'] = cour_character

                cour_attribute = tag.find_all('td')[9].string
                scoreInfo['cour_attribute'] = cour_attribute

                score_tank.append(scoreInfo.copy())
                self.cur.execute("INSERT INTO scorepages (studentid, year, term, code, title, cour_character, credit, fin_score, cour_attribute) VALUES (%s, %s, %s, %s, %s, %s, %s, %s ,%s)",(self.studentID, year, term, code, title, cour_character, float(credit), float(fin_score), cour_attribute))
                self.conn.commit()
 

        self.cur.close()
        self.conn.close()
        return score_tank   

if __name__ == '__main__':
    mycj = CJScrap('username', 'password')
    gemycj = mycj.getScore()
    print gemycj[0]



