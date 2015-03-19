#!/usr/local/bin/python
# -*-coding:utf8-*-
__author__ = 'youjiezeng'
__createDate__ = '2/6/15'


class Job(object):
    def __init__(self):
        self._job_id = ''
        self._module_name = ''
        self._job_name = ''
        self._job_script = ''
        self._job_params = ''
        self._env_script = ''
        self._pre_job_ids = ''
        self._pre_job_scripts = ''
        self._schedule = ''
        self._is_avariable = ''
        self._exec_status = ''
        self._exec_starttime = ''
        self._exec_endtime = ''
        self._exec_log = ''

    def Job(self, job_id, module_name, job_name, job_script, job_params=None, env_script=None, pre_job_ids=None,
            pre_job_scripts=None, schedule=None, is_avariable=None, exec_status=None, exec_starttime=None,
            exec_endtime=None,
            exec_log=None):
        self._job_id = job_id
        self._module_name = module_name
        self._job_name = job_name
        self._job_script = job_script
        self._job_params = job_params
        self._env_script = env_script
        self._pre_job_ids = pre_job_ids
        self._pre_job_scripts = pre_job_scripts
        self._schedule = schedule
        self._is_avariable = is_avariable
        self._exec_status = exec_status
        self._exec_starttime = exec_starttime
        self._exec_endtime = exec_endtime
        self._exec_log = exec_log

    @property
    def job_id(self):
        return self._job_id

    @job_id.setter
    def job_id(self, jobid):
        self._job_id = jobid

    @property
    def module_name(self):
        return self._module_name

    @module_name.setter
    def module_name(self, modname):
        self._module_name = modname

    @property
    def job_name(self):
        return self._job_name

    @job_name.setter
    def job_name(self, jobname):
        self._job_name = jobname

    @property
    def env_script(self):
        return self._env_script

    @env_script.setter
    def env_script(self, envscript):
        self._env_script = envscript

    @property
    def job_script(self):
        return self._job_script

    @job_script.setter
    def job_script(self, jobscript):
        self._job_script = jobscript

    @property
    def job_params(self):
        return self._job_params

    @job_params.setter
    def job_params(self, jobparams):
        self._job_params = jobparams


    @property
    def pre_job_ids(self):
        return self._pre_job_ids

    @pre_job_ids.setter
    def pre_job_ids(self, prejobids):
        self._pre_job_ids = prejobids

    @property
    def pre_job_scripts(self):
        return self._pre_job_scripts

    @pre_job_scripts.setter
    def pre_job_scripts(self, prejobscripts):
        self._pre_job_scripts = prejobscripts

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, sche):
        self._schedule = sche

    @property
    def exec_status(self):
        return self._exec_status

    @exec_status.setter
    def exec_status(self, execstatus):
        self._exec_status = execstatus

    @property
    def exec_starttime(self):
        return self._exec_starttime

    @exec_starttime.setter
    def exec_starttime(self, execstarttime):
        self._exec_starttime = execstarttime

    @property
    def exec_endtime(self):
        return self._exec_endtime

    @exec_endtime.setter
    def exec_endtime(self, execendtime):
        self._exec_endtime = execendtime

    @property
    def exec_log(self):
        return self._exec_log

    @exec_log.setter
    def exec_log(self, execlog):
        self._exec_log = execlog

    @property
    def is_avariable(self):
        return self._is_avariable

    @is_avariable.setter
    def is_avariable(self, isavariable):
        self._is_avariable = isavariable

    def to_job_json(self):
        job_dic = {}
        job_dic['job_id'] = self._job_id
        job_dic['module_name'] = self._module_name
        job_dic['job_name'] = self._job_name
        job_dic['job_script'] = self._job_script
        job_dic['env_script'] = self._env_script
        job_dic['pre_job_ids'] = self._pre_job_ids
        job_dic['pre_job_scripts'] = self._pre_job_scripts
        job_dic['schedule'] = self._schedule
        job_dic['is_avariable'] = self._is_avariable

        job_str = '{'
        for key, value in job_dic.items():
            job_str += '"%s":"%s"' % (key,value)
            job_str +=','
        job_str = job_str[:-1]+"}"
        return job_str


    def to_job_history_json(self):
        job_dic = {}
        job_dic['job_id'] = self._job_id
        job_dic['module_name'] = self._module_name
        job_dic['job_name'] = self._job_name
        job_dic['job_script'] = self._job_script
        job_dic['env_script'] = self._env_script
        job_dic['pre_job_ids'] = self._pre_job_ids
        job_dic['pre_job_scripts'] = self._pre_job_scripts
        job_dic['schedule'] = self._schedule
        job_dic['exec_status'] = self._exec_status
        job_dic['exec_starttime'] = self._exec_starttime
        job_dic['exec_endtime'] = self._exec_endtime
        job_dic['exec_log'] = self._exec_log
        job_str = '{'
        for key, value in job_dic.items():
            job_str += '"%s":"%s"' % (key,value)
            job_str +=','
        job_str = job_str[:-1]+"}"
        return job_str


class JobStatus(object):
    JOB_SUCCESS = 'JOB SUCCESS'
    JOB_NOT_EXISTS = 'JOB NOT EXISTS'
    JOB_IS_RUNNING = 'JOB IS RUNNING'
    JOB_FAILED = 'JOB FAILED'
    PRE_JOB_FAILED = 'PRE JOB FAILED'
    PRE_JOB_SCRIPT_FAILED = 'PRE JOB SCRIPT FAILED'
    ENV_SCRIPT_FAILED = 'ENV SCRIPT FAILED'
    # @property
    # def JOB_SUCCESS(self):
    # return 'JOB SUCCESS'
    #
    # @property
    # def JOB_NOT_EXISTS(self):
    # return 'JOB NOT EXISTS'
    #
    # @property
    # def JOB_IS_RUNNING(self):
    #     return 'JOB IS RUNNING'
    #
    # @property
    # def JOB_FAILED(self):
    #     return 'JOB FAILED'
    #
    # @property
    # def PRE_JOB_FAILED(self):
    #     return 'PRE JOB FAILED'
    #
    # @property
    # def PRE_JOB_SCRIPT_FAILED(self):
    #     return 'PRE JOB SCRIPT FAILED'
    #
    # @property
    # def ENV_SCRIPT_FAILED(self):
    #     return 'ENV SCRIPT FAILED'


if __name__ == '__main__':
    js = JobStatus()
    print type(js.JOB_SUCCESS)
    print type(JobStatus.JOB_SUCCESS_1)
    print type(JobStatus.PRE_JOB_SCRIPT_FAILED)