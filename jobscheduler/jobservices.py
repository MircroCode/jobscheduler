#!/usr/local/bin/python
# -*-coding:utf8-*-
import logging
import os
from dbutil.mysqlutil import DBHandler

__author__ = 'youjiezeng'
__createDate__ = '2/6/15'

import conf
from module.jobs import Job

file_path = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(file_path + '/logging.conf')
logger = logging.getLogger("job")

def getJobById(jobid):
    db_handler = DBHandler(conf.DB_PARAMS)
    sql = "select jobid, module_name, job_name, env_script, job_script, pre_job_ids, pre_job_scripts, " \
          "schedule, is_avariable from etl_scheduler where jobid = '%s';" % jobid
    result = db_handler.queryWithOneResult(sql)
    if len(result) == 0:
        return
    job = Job()
    job.job_id = result[0]
    job.module_name = result[1]
    job.job_name = result[2]
    job.env_script = result[3]
    job.job_script = result[4]
    job.pre_job_ids = result[5]
    job.pre_job_scripts = result[6]
    job.schedule = result[7]
    job.is_avariable = result[8]
    return job


def getJobList():
    db_handler = DBHandler(conf.DB_PARAMS)
    sql = "select jobid, module_name, job_name, env_script, job_script, pre_job_ids, pre_job_scripts, " \
          "schedule, is_avariable from etl_scheduler;"
    result = db_handler.queryWithResult(sql)
    return result


def getJobHistory():
    db_handler = DBHandler(conf.DB_PARAMS)
    sql = "select * from etl_job_history order by keyid desc;"
    result = db_handler.queryWithResult(sql)
    return result


def saveJob2DB(job):
    db_handler = DBHandler(conf.DB_PARAMS)
    # sql = "insert into etl_job_history (jobid, module_name, job_name, env_script, job_script, pre_job_ids, pre_job_scripts, schedule, exec_status, exec_starttime, exec_endtime, exec_log) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
    # full_sql = sql % (
    # job.job_id, job.module_name, job.job_name, job.env_script, job.job_script, job.pre_job_ids, job.pre_job_scripts,
    # job.schedule, job.exec_status, job.exec_starttime, job.exec_endtime, job.exec_log)
    # print full_sql
    # result = db_handler.execSqlWithNoParams(full_sql)
    sql = "insert into etl_job_history (jobid, module_name, job_name, env_script, job_script, pre_job_ids, pre_job_scripts, schedule, exec_status, exec_starttime, exec_endtime, exec_log) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    result = db_handler.execSqlWithParams(sql, (
        job.job_id, job.module_name, job.job_name, job.env_script, job.job_script, job.pre_job_ids, job.pre_job_scripts,
        job.schedule, job.exec_status, job.exec_starttime, job.exec_endtime, job.exec_log))
    return result


def updateJob2DB(job):
    db_handler = DBHandler(conf.DB_PARAMS)
    # sql = "update etl_job_history set module_name='%s' , job_name='%s' , env_script='%s' , job_script='%s' , pre_job_ids='%s' " \
    # ", pre_job_scripts='%s' , schedule='%s' , exec_status='%s' , exec_starttime='%s' , exec_endtime='%s' where jobid = '%s' and exec_log='%s';"
    # full_sql = sql % (
    # job.module_name.replace('\'', '\\\''), job.job_name, job.env_script, job.job_script, job.pre_job_ids, job.pre_job_scripts,
    # job.schedule, job.exec_status, job.exec_starttime, job.exec_endtime, job.job_id, job.exec_log)
    # print full_sql
    # result = db_handler.execSqlWithNoParams(full_sql)
    sql = "update etl_job_history set module_name=%s , job_name=%s , env_script=%s , job_script=%s , pre_job_ids=%s " \
          ", pre_job_scripts=%s , schedule=%s , exec_status=%s , exec_starttime=%s , exec_endtime=%s where jobid = %s and exec_log=%s;"
    result = db_handler.execSqlWithParams(sql, (
        job.module_name, job.job_name, job.env_script, job.job_script, job.pre_job_ids, job.pre_job_scripts,
        job.schedule, job.exec_status, job.exec_starttime, job.exec_endtime, job.job_id, job.exec_log))
    return result


def getJobListFromFileDB():
    fileDB = open(file_path + '/db/jobs.data', 'rb')
    job_list = []
    try:
        while True:
            line = fileDB.readline()
            if not line:
                break
            d = eval(line)
            if d is None: return
            job = Job()
            job.job_id = d.get('job_id')
            job.module_name = d.get('module_name')
            job.job_name = d.get('job_name')
            job.env_script = d.get('env_script')
            job.job_script = d.get('job_script')
            job.pre_job_ids = d.get('pre_job_ids')
            job.pre_job_scripts = d.get('pre_job_scripts')
            job.schedule = d.get('schedule')
            job.is_avariable = d.get('is_avariable')
            if job.is_avariable == "1": job_list.append(job)
    except Exception, e:
        logger.error("getJobListFromFileDB error:" + str(e))
    return job_list


def getEtlJobHistoryListFromFileDB():
    fileDB = open(file_path + '/db/etl_job_history.data', 'rb')
    job_list = []
    try:
        while True:
            line = fileDB.readline()
            if not line:
                break
            d = eval(line)
            job = Job()
            job.job_id = d.get('job_id')
            job.module_name = d.get('module_name')
            job.job_name = d.get('job_name')
            job.env_script = d.get('env_script')
            job.job_script = d.get('job_script')
            job.pre_job_ids = d.get('pre_job_ids')
            job.pre_job_scripts = d.get('pre_job_scripts')
            job.schedule = d.get('schedule')
            job.exec_status = d.get('exec_status')
            job.exec_starttime = d.get('exec_starttime')
            job.exec_endtime = d.get('exec_endtime')
            job.exec_log = d.get('exec_log')
            job_list.append(job)
    except Exception, e:
        logger.error("getEtlJobHistoryListFromFileDB error:" + str(e))
    return job_list


def getJobFromFileDB(job_id):
    try:
        job_list = getJobListFromFileDB()
        if job_list is None: return
        job = [job for job in job_list if job.job_id == job_id]
        if len(job) != 1:
            logger.error("getJobFromFileDB error: did not find job or find multi jobs by job_id:" + str(job_id))
        else:
            return job[0]
    except Exception, e:
        logger.error("getJobFromFileDB error:" + str(e))

def saveJob2FileDB(job):
    file_db = open(file_path + '/db/jobs.data', 'a')
    job_json = job.to_job_json()
    file_db.write(job_json)
    file_db.write("\n")
    file_db.flush()
    file_db.close()

def saveJobHistory2FileDB(job):
    file_db = open(file_path + '/db/etl_job_history.data', 'a')
    job_json = job.to_job_history_json()
    file_db.write(job_json)
    file_db.write("\n")
    file_db.flush()
    file_db.close()

def updateJob2FileDB(job):
    fileDB = open(file_path + '/db/jobs.data', 'a')
    jobs = getJobListFromFileDB()
    new_jobs = []
    for j in jobs:
        if j.job_id == job.job_id:
            new_jobs.append(job)
        else:
            new_jobs.append(j)
    clear_file_handler = open(file_path + '/db/jobs.data', 'w')
    clear_file_handler.truncate()

    for nj in new_jobs:
        fileDB.write(nj.to_job_json())
        fileDB.write("\n")
    fileDB.flush()
    fileDB.close()


def updateJobStatus2FileDB(job):
    fileDB = open(file_path + '/db/etl_job_history.data', 'a')
    jobs = getEtlJobHistoryListFromFileDB()
    new_jobs = []
    for j in jobs:
        if j.job_id == job.job_id and j.exec_endtime == '':
            new_jobs.append(job)
        else:
            new_jobs.append(j)
    clear_file_handler = open(file_path + '/db/etl_job_history.data', 'w')
    clear_file_handler.truncate()

    for nj in new_jobs:
        fileDB.write(nj.to_job_history_json())
        fileDB.write("\n")
    fileDB.flush()
    fileDB.close()


if __name__ == '__main__':
    logger.error("job services,,,,,")


