#!/usr/local/bin/python
# -*-coding:utf8-*-
__author__ = 'youjiezeng'
__createDate__ = '3/18/15'


import urllib2
import urllib
import hashlib
import datetime

content="python send sms:job error"
mobile="15201684563"
#网关接口字段
keyid='20140331151239106SMSPLATACCESS099280'
appid='100182'
priority=3
time = datetime.datetime.now().__format__("%Y%m%d%H%M%S")

enc_str = str(appid+mobile+content+time+keyid).encode("utf8")
md5 = hashlib.md5(enc_str).hexdigest()
print md5

params = {"appid":appid,
          "destnumber":mobile,
          "content":content,
          "tailsp":"01",
          "enc":md5,
          "linkid":"20121126101155432",
          "priority":3,
          "timestamp":time}
print params
print "http://i.sms.sohu.com/WLS/smsaccess/mt?"+urllib.urlencode(params)



# sms_url = "http://i.sms.sohu.com/WLS/smsaccess/mt?appid=%s\&destnumber=%s\&content=%s\&enc=%s\&linkid=20121126101155432&priority=%\&timestamp=%s"
#
#
#
# print (appid, mobile, urlContentCode, md5, priority, time)
# sms_url_full = sms_url % (appid, mobile, "sohu+box+dc+job+fail%2Cjob+id+%3A102", md5, priority, time)
#
# print sms_url_full

