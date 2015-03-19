#!/usr/local/bin/python
# -*-coding:utf8-*-
import subprocess
import threading
import datetime
import sys
import reminder
sys.path.append("..")
from module.jobs import Job, JobStatus
import jobservices
import logging
import logging.config

__author__ = 'youjiezeng'
__createDate__ = '2/5/15'

import commands
import os

# cwd = os.getcwd()
file_path = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(file_path + '/../logging.conf')
logger = logging.getLogger("tool")

class ExecShell(object):
    def execShellWithResult(self, shell_cmd):
        result = commands.getoutput(shell_cmd)
        return result

    def execShellWithStatusOutput(self, shell_cmd):
        result = commands.getstatusoutput(shell_cmd)
        return result

    def execShellWithStatus(self, shell_cmd):
        result = commands.getstatusoutput(shell_cmd)
        return result[0]

    def setEnvParameter(self, env_dict):
        if not isinstance(env_dict, type({})):
            env_dict = dict(env_dict)
        for k, v in env_dict.items():
            os.environ[k] = v  # set environment value

    def execShellGetOutputRealTime(self, log_name, shell_cmd, is_shell, call_back=None):
        popen = subprocess.Popen(shell_cmd, stdout=subprocess.PIPE, shell=bool(is_shell))
        while True:
            line = popen.stdout.readline()
            # if not line: break  #这种方式不可行，在结束stdout的时候，进程实际还没有结束，容易返回None
            if call_back is not None:
                call_back(log_name, line)
            code = popen.poll()
            if code is not None:
                break
        returnCode = popen.returncode
        return returnCode

    def execShellGetOutputAsyn(self, job):
        jt = JobExecThread("ExecJobThread" + str(job.job_id), job)
        if not isinstance(job, Job):
            return
        if job.exec_log == '':
            job.exec_log = 'logs/job_' + str(job.job_id) + '_' + datetime.datetime.now().__format__(
                "%Y%m%d%H%M%S") + ".txt"
        job.exec_status = JobStatus.JOB_IS_RUNNING
        job.exec_starttime = datetime.datetime.now().__format__("%Y-%m-%d %H:%M:%S")
        # jobservices.saveJob2DB(job)
        jobservices.saveJobHistory2FileDB(job)
        jt.start()
        return JobStatus.JOB_IS_RUNNING


class JobExecThread(threading.Thread):
    def __init__(self, thdname, job):
        threading.Thread.__init__(self, name=thdname)
        self.job = job

    def saveLog2File(self, log_name, line):
        file_handler = open(file_path+"/../"+log_name, 'a')
        file_handler.write(line)
        file_handler.flush()
        file_handler.close()

    def run(self):
        scirpt = self.job.job_script
        params = self.job.job_params
        popen = subprocess.Popen(str(scirpt)+" "+str(params), stdout=subprocess.PIPE, shell=True)
        while True:
            line = popen.stdout.readline()
            logger.debug("job runing log:" + str(line))
            self.saveLog2File(self.job.exec_log, line)
            code = popen.poll()
            if code is not None:
                break
        self.saveLog2File(self.job.exec_log, '------------------------------- END -------------------------------')
        returnCode = popen.returncode
        if returnCode != 0:
            self.job.exec_status = JobStatus.JOB_FAILED
            #send sms
            t = reminder.ReminderTools()
            t.smsReminder("Job run error, job name:"+str(self.job.job_name))
        else:
            self.job.exec_status = JobStatus.JOB_SUCCESS
        self.job.exec_endtime = datetime.datetime.now().__format__("%Y-%m-%d %H:%M:%S")
        # jobservices.updateJob2DB(self.job)
        jobservices.updateJobStatus2FileDB(self.job)


class ExecShellUnderSystem(ExecShell):
    def execShellWithStatus(self, shell_cmd):
        status = os.system(shell_cmd)
        return status


class ExecShellUnderPopen(ExecShell):
    def execShellWithFileObject(self, shell_cmd):
        file_object = os.popen(shell_cmd)
        return file_object


def printline(log_name, line):
    print 'printline: ', log_name, line


def execJob(job):
    if job is None:  # job not exists
        return JobStatus.JOB_NOT_EXISTS

    #####    pre job   #####
    pre_job_id = job.pre_job_ids
    pre_job_exec_status = 0
    for sub_job_id in pre_job_id.split(','):  # pre jobs defined format like '1,2,3'
        if sub_job_id == '' or int(sub_job_id) == 0:  # pre job id null
            continue
        sub_job = jobservices.getJobFromFileDB(sub_job_id)
        sub_job_status = execJob(sub_job)
        if sub_job_status != 0:
            pre_job_exec_status = sub_job_status
    if pre_job_exec_status != 0:  # pre job failed
        return JobStatus.PRE_JOB_FAILED

    #####    pre job scripts  #####
    pre_job_scripts = job.pre_job_scripts
    cmdtool = ExecShellUnderSystem()
    if pre_job_scripts.encode('utf8') != '':
        cmd_status = cmdtool.execShellWithStatus(pre_job_scripts)
        if cmd_status != 0:
            return JobStatus.PRE_JOB_SCRIPT_FAILED

    #####   env script   #####
    env_script = job.env_script
    env_utf8 = env_script.encode('utf8')
    if env_utf8 != '':
        env_params = env_utf8.split(';')
        params = {}
        for p in env_params:
            ps = p.replace('set', '').strip().split('=')
            if not len(ps) == 2: continue
            params[ps[0]] = ps[1]
        try:
            cmdtool.setEnvParameter(params)
        except Exception as e:
            logger.error("env script error:" + str(e))
            return JobStatus.ENV_SCRIPT_FAILED

    cmd_status = cmdtool.execShellGetOutputAsyn(job)
    return cmd_status


if __name__ == "__main__":
    t = ExecShell()
    # x = t.execShellGetOutputRealTime('log_name', '/Users/youjiezeng/Desktop/test2.sh', 'True', printline)
    # x = t.execShellGetOutputRealTime(['ping', '-c', '10', 'www.baidu.com'], False, printline)
    # job = Job()
    # job.job_id = 88
    # job.module_name = 'test'
    # job.job_name = 'test2'
    # job.job_script = '/Users/youjiezeng/Desktop/test2.sh'
    # t.execShellGetOutputAsyn(job)