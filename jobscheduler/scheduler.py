#!/usr/local/bin/python
# -*-coding:utf8-*-
import datetime
import logging
import threading
from time import sleep
from exectools import cmd
import jobservices

__author__ = 'youjiezeng'
__createDate__ = '2/10/15'

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("jobscheduler.SchedulerScan")


class SchedulerScan(threading.Thread):
    def __init__(self, thdname="SchedulerScan"):
        threading.Thread.__init__(self, name=thdname)

    def run(self):
        while True:
            try:
                jobs = jobservices.getJobListFromFileDB()
                job_schedulers = [(job.job_id, job.schedule) for job in jobs if job.schedule is not None]
                logger.debug('...scaning job schedulers' + str(job_schedulers))
                x = datetime.datetime.now()
                exec_jobs = [job for (job, sched) in job_schedulers if len(sched) > 0 and (
                sched.split()[0].encode('utf8').lstrip('0') == str(x.minute) or sched.split()[0].encode('utf8') == '*') \
                             and (sched.split()[1].encode('utf8').lstrip('0') == str(x.hour) or sched.split()[1] == '*') and (
                sched.split()[2].encode('utf8').lstrip('0') == str(x.day) or sched.split()[2] == '*') \
                             and (sched.split()[3].encode('utf8').lstrip('0') == str(x.month) or sched.split()[3] == '*') and (
                             sched.split()[4].encode('utf8') == str(x.year) or sched.split()[4] == '*')]
                for e_job_id in exec_jobs:
                    logger.debug('.... scan job start run job:'+str(e_job_id))
                    e_job = jobservices.getJobFromFileDB(e_job_id)
                    cmd.execJob(e_job)
            except Exception, e:
                logger.error("scheduler error:" + str(e))
                sleep(5)
                continue
            sleep(60)
