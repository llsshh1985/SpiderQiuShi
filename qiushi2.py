__author__ = 'lsh'
#-*- encoding:utf8 -*-

import urllib
import urllib2
import re
import thread
import time

#糗事百科爬虫
class QSBK:

    # 初始化方法，定义变量
    def __init__(self):
        self.pageIndex=1
        self.user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers={ 'User-Agent' : self.user_agent}
        #存放段子的变量，一页一个元素
        self.stories=[]
        #存放程序是否继续运行的变量
        self.enable=False
        #传入某一页的索引获得页面代码

    def getPage(self,pageIndex):
        try:
            url='http://www.qiushibaike.com/8hr/page/' + str(pageIndex)
            #构建请求的request
            request=urllib2.Request(url,headers = self.headers)
            response=urllib2.urlopen(request)
            pagecode=response.read().decode('utf-8')
            return pagecode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print  u"连接糗事百科失败,错误原因 ",e.reason
                return None

    #传入某一页代码 返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode=self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败..."
            return None
        pattern=re.compile('<div.*?class="content">(.*?)</div>(.*?)</i>',re.S)
        items=re.findall(pattern,pageCode)
        #用来存储段子
        pageStories=[]
        for item in items:
            singleS=re.sub('<[^>]+>','',item[0].strip())+'\n'
            pageStories.append(singleS)
            #print singleS
        return pageStories


    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        if self.enable==True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories=self.getPageItems(self.pageIndex)
                #将该页的段子存放在全局List中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    #调用该方法，每次前回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            input=raw_input()
            self.loadPage()
            #输入q终止
            if input=="q":
                self.enable=False
                return
            print story

    #开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，q退出"
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()