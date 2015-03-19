CREATE TABLE `etl_job_history` (
  `keyid` bigint(20) NOT NULL AUTO_INCREMENT,
  `jobid` bigint(20) NOT NULL,
  `module_name` varchar(50) NOT NULL COMMENT '模块名称',
  `job_name` varchar(100) NOT NULL COMMENT '任务名称',
  `env_script` varchar(1000) DEFAULT NULL COMMENT '环境脚本',
  `job_script` varchar(2000) NOT NULL COMMENT '任务脚本',
  `pre_job_ids` varchar(255) DEFAULT '' COMMENT '前置任务id',
  `pre_job_scripts` varchar(2000) DEFAULT NULL COMMENT '前置任务脚本',
  `schedule` varchar(100) DEFAULT NULL,
  `exec_status` varchar(100) DEFAULT NULL,
  `exec_starttime` varchar(30) DEFAULT NULL COMMENT '执行时间',
  `exec_endtime` varchar(30) DEFAULT NULL,
  `exec_log` varchar(255) DEFAULT NULL COMMENT '执行日志文件',
  PRIMARY KEY (`keyid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `etl_scheduler` (
  `jobid` bigint(20) NOT NULL AUTO_INCREMENT,
  `module_name` varchar(50) NOT NULL COMMENT '模块名称',
  `job_name` varchar(100) NOT NULL COMMENT '任务名称',
  `env_script` varchar(1000) DEFAULT NULL COMMENT '环境脚本',
  `job_script` varchar(2000) NOT NULL COMMENT '任务脚本',
  `pre_job_ids` varchar(255) DEFAULT '' COMMENT '前置任务id',
  `pre_job_scripts` varchar(2000) DEFAULT '' COMMENT '前置任务脚本',
  `schedule` varchar(100) DEFAULT '',
  `is_avariable` tinyint(20) DEFAULT '1' COMMENT '1:有效，0：无效',
  PRIMARY KEY (`jobid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8