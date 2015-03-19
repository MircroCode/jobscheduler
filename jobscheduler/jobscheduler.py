#!/usr/local/bin/python
# -*-coding:utf8-*-
import logging
import logging.config
import tornado
from tornado.ioloop import IOLoop
from tornado.web import Application, url, RequestHandler
import conf
from exectools import cmd

import jobservices
import os
import scheduler
from module import jobs

__author__ = 'youjiezeng'

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("jobscheduler.JobScheduler")

def make_app():
    settings = {"static_path": os.path.join(os.path.dirname(__file__), "logs")}
    return Application([url('/', ConsoleHandler),
                        url('/console', ConsoleHandler),
                        url('/start_job', StartJobHandler),
                        url('/stop_job', StopJobHandler),
                        url('/edit_job', EditJobHandler),
                        url('/add_job', AddJobHandler),
                        url('/filter_job_history', FilterJobHistoryHandler),
                        url('/read_log', ReadLogHandler),
                        url('/logs/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path']))],
                       **settings
    )

class ReadLogHandler(RequestHandler):
    def get(self):
        log_name = self.get_argument("log")
        file_handler = open(log_name, 'rb')
        while True:
            line = file_handler.readline()
            if not line: break
            self.write(line)
            self.write("<br/>")
            self.flush()

class FilterJobHistoryHandler(RequestHandler):
    def get(self):
        jobs = jobservices.getJobListFromFileDB()
        jobhistory = jobservices.getEtlJobHistoryListFromFileDB()
        jobhistory.sort(key=lambda job: job.exec_starttime, reverse=True)
        self.render('template/console.html', title='console', jobs=jobs, jobhistory=jobhistory)

    def post(self):
        filter_start_time = self.get_argument("starttime")
        filter_end_time = self.get_argument("endtime")
        filter_module_name = self.get_argument("modulename")
        filter_job_name = self.get_argument("jobname")
        filter_exec_status = self.get_argument("execstatus")

        try:
            jobs = jobservices.getJobListFromFileDB()
            jobhistory = jobservices.getEtlJobHistoryListFromFileDB()
            job_history_filter = [j for j in jobhistory if (
            filter_start_time.strip() == '' or j.exec_starttime.find(str(filter_start_time)) >= 0)
                                  and (filter_end_time.strip() == '' or j.exec_endtime.find(str(filter_end_time)) >= 0)
                                  and (filter_job_name.strip() == '' or j.job_name.find(str(filter_job_name)) >= 0)
                                  and (filter_module_name.strip() == '' or j.module_name.find(str(filter_module_name)) >= 0)
                                  and (filter_exec_status.strip() == '' or j.exec_status.find(str(filter_exec_status)) >=0)
            ]

            job_history_filter.sort(key=lambda job: job.exec_starttime, reverse=True)
            self.render('template/console.html', title='console', jobs=jobs, jobhistory=job_history_filter)
        except Exception, e:
            logger.error("FilterJobHistoryHandler error" + str(e))


class EditJobHandler(RequestHandler):
    def get(self):
        try:
            job_id = self.get_argument("jobid")
            job = jobservices.getJobFromFileDB(job_id)
            self.render('template/editjob.html', title='edit job', job=job, vflag="")
        except Exception, e:
            logger.error("EditJobHandler error:" + str(e))

    def post(self):
        try:
            job_id = self.get_argument("jobid")
            module_name = self.get_argument("modulename")
            job_name = self.get_argument("jobname")
            env_script = self.get_argument("envscript")
            job_script = self.get_argument("jobscript")
            pre_job_ids = self.get_argument("prejobids")
            pre_job_scripts = self.get_argument("prejobscripts")
            schedule = self.get_argument("schedule")
            is_avariable = self.get_argument("isavariable")

            job = jobs.Job()
            job.job_id = job_id
            job.module_name = module_name
            job.job_name = job_name
            job.env_script = env_script
            job.job_script = job_script
            job.pre_job_ids = pre_job_ids
            job.pre_job_scripts = pre_job_scripts
            job.schedule = schedule
            job.is_avariable = is_avariable

            if job_id == '' or job_id is None:
                self.render('template/editjob.html', title='edit job', job=job, vflag='JOB ID CAN NOT BE NULL')
            if job_name == '' or job_name is None:
                self.render('template/editjob.html', title='edit job', job=job, vflag='JOB NAME CAN NOT BE NULL')
            if module_name == '' or module_name is None:
                self.render('template/editjob.html', title='edit job', job=job, vflag='MODULE NAME CAN NOT BE NULL')
            if job_script == '' or job_script is None:
                self.render('template/editjob.html', title='edit job', job=job, vflag='JOB SCRIPT CAN NOT BE NULL')
            if is_avariable == '' or is_avariable is None:
                self.render('template/editjob.html', title='edit job', job=job, vflag='ISAVARIABLE CAN NOT BE NULL')

            jobservices.updateJob2FileDB(job)
            self.render('template/editjob.html', title='edit job', job=job, vflag='EDIT JOB SUCESS')
        except Exception, e:
            logger.error("UpdateJob error:" + str(e))


class AddJobHandler(RequestHandler):
    def get(self):
        self.render('template/addjob.html', title='add job', job=None, vflag='')

    def post(self):
        try:
            job_id = self.get_argument("jobid")
            module_name = self.get_argument("modulename")
            job_name = self.get_argument("jobname")
            env_script = self.get_argument("envscript")
            job_script = self.get_argument("jobscript")
            pre_job_ids = self.get_argument("prejobids")
            pre_job_scripts = self.get_argument("prejobscripts")
            schedule = self.get_argument("schedule")
            is_avariable = self.get_argument("isavariable")

            job = jobs.Job()
            job.job_id = job_id
            job.module_name = module_name
            job.job_name = job_name
            job.env_script = env_script
            job.job_script = job_script
            job.pre_job_ids = pre_job_ids
            job.pre_job_scripts = pre_job_scripts
            job.schedule = schedule
            job.is_avariable = is_avariable

            job_list = jobservices.getJobListFromFileDB()
            job_exists_list = [j for j in job_list if j.job_id == job_id]
            if job_id == '' or job_id is None:
                self.render('template/addjob.html', title='add job', job=job, vflag='JOB ID CAN NOT BE NULL')
            if job_exists_list.__len__() > 0:
                self.render('template/addjob.html', title='add job', job=job, vflag='JOB ID EXISTS ALREADY')
            if job_name == '' or job_name is None:
                self.render('template/addjob.html', title='add job', job=job, vflag='JOB NAME CAN NOT BE NULL')
            if module_name == '' or module_name is None:
                self.render('template/addjob.html', title='add job', job=job, vflag='MODULE NAME CAN NOT BE NULL')
            if job_script == '' or job_script is None:
                self.render('template/addjob.html', title='add job', job=job, vflag='JOB SCRIPT CAN NOT BE NULL')
            if is_avariable == '' or is_avariable is None:
                self.render('template/addjob.html', title='add job', job=job, vflag='ISAVARIABLE CAN NOT BE NULL')

            jobservices.saveJob2FileDB(job)
            self.render('template/addjob.html', title='add job', job=job, vflag='ADD JOB SUCESS')
        except Exception, e:
            logger.error("AddJob error:" + str(e))


class StopJobHandler(RequestHandler):
    def get(self):
        job_id = self.get_argument("jobid")
        self.killJobProcessById(job_id)

    def killJobProcessById(self, job_id):
        pass


class StartJobHandler(RequestHandler):
    def get(self):
        try:
            job_id = self.get_argument("jobid")
            # job = jobservices.getJobById(job_id)
            job = jobservices.getJobFromFileDB(job_id)
            if job is None:
                logger.error("job is None when start the job!")
                return
            self.render('template/execjob.html', title='exec job', job=job, vflag='')
        except Exception, e:
            logger.error("StartHandler error:" + str(e))

    def post(self):
        job_id = self.get_argument("jobid")
        module_name = self.get_argument("modulename")
        job_name = self.get_argument("jobname")
        env_script = self.get_argument("envscript")
        job_script = self.get_argument("jobscript")
        pre_job_ids = self.get_argument("prejobids")
        pre_job_scripts = self.get_argument("prejobscripts")
        params = self.get_argument("params")

        job = jobs.Job()
        job.job_id = job_id
        job.module_name = module_name
        job.job_name = job_name
        job.env_script = env_script
        job.job_script = job_script
        job.pre_job_ids = pre_job_ids
        job.pre_job_scripts = pre_job_scripts
        job.job_params = params

        status = cmd.execJob(job)
        self.redirect('/')


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello world")


class ConsoleHandler(RequestHandler):
    def get(self):
        """
            get jobs from db
        """
        try:
            jobs = jobservices.getJobListFromFileDB()
            jobhistory = jobservices.getEtlJobHistoryListFromFileDB()
            jobhistory.sort(key=lambda job: job.exec_starttime, reverse=True)
            self.render('template/console.html', title='console', jobs=jobs, jobhistory=jobhistory)
        except Exception, e:
            logger.error("ConsoleHandler error" + str(e))


if __name__ == '__main__':
    logger.info("----start jobscheduler-----")
    if not os.path.exists(conf.LOGS_DIR):
        os.makedirs(conf.LOGS_DIR)  # create log dir if no exists
    app = make_app()
    port = conf.WEBSITE_PORT
    app.listen(port)
    scan = scheduler.SchedulerScan()
    scan.start()
    print 'tornado server started!'
    IOLoop.current().start()
