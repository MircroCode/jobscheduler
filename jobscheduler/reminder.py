#!/usr/local/bin/python
# -*-coding:utf8-*-
import conf
import urllib
import urllib2
import datetime
import hashlib
import logging
import logging.config
import os

__author__ = 'youjiezeng'
__createDate__ = '2/10/15'

file_path = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(file_path + '/logging.conf')
logger = logging.getLogger("job.reminder")

#网关接口字段
keyid='20140331151239106SMSPLATACCESS099280'
appid='100182'
priority=3


class ReminderTools(object):
    def emailReminder(self):
        pass
    def smsReminder(self, content):
        sms_url = conf.SMS_URL
        mobile = conf.REMIND_MOBILE
        time = datetime.datetime.now().__format__("%Y%m%d%H%M%S")

        enc_str = str(appid+mobile+content+time+keyid).encode("utf8")
        md5 = hashlib.md5(enc_str).hexdigest()

        params = {"appid":appid,
          "destnumber":mobile,
          "content":content,
          "tailsp":"1",
          "enc":md5,
          "linkid":"20121126101155432",
          "priority":3,
          "timestamp":time}

        try:
            request_url = sms_url+"?"+str(urllib.urlencode(params))
            print request_url
            response = urllib2.urlopen(request_url)
            #send sms sucess
            if response.getcode() == 0:
                logger.info("send sms sucess!content:"+content)
        except Exception,e:
            logger.error("send sms error:"+str(e))



if __name__ == '__main__':
    t = ReminderTools()
    t.smsReminder("python send sms:main job")
