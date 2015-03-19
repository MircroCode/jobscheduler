#!/usr/local/bin/python
# -*-coding:utf8-*-
import logging
import logging.config

__author__ = 'youjiezeng'
__createDate__ = '2/5/15'
import MySQLdb
import os

# cwd = os.getcwd()
file_path = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(file_path + '/../logging.conf')
logger = logging.getLogger("tool")


class DBHandler(object):
    def __init__(self, kwargs):
        self.connect = kwargs

    def query(self, query_str):
        """
            return affected rows number.
        """
        try:
            conn = MySQLdb.connect(**self.connect)
            cur = conn.cursor()
            result = cur.execute(query_str)
            conn.commit()
            conn.close()
            return result
        except Exception, e:
            logger.error("mysql util error:" + str(e))


    def queryWithResult(self, query_str):
        """
            return query result as list.
        :rtype : list
        :param query_str: 
        """
        try:
            conn = MySQLdb.connect(**self.connect)
            cursor = conn.cursor()
            cursor.execute(query_str)
            result = cursor.fetchall()
            conn.commit()
            conn.close()
            return result
        except Exception, e:
            logger.error("mysql util error:" + str(e))


    def queryWithResultSize(self, query_str, result_size):
        """
            return query result as list.
        :rtype : list
        :param query_str:
        """
        try:
            conn = MySQLdb.connect(**self.connect)
            cursor = conn.cursor()
            cursor.execute(query_str)
            result = cursor.fetchmany(result_size)
            conn.commit()
            conn.close()
            return result
        except Exception, e:
            logger.error("mysql util error:" + str(e))

    def queryWithOneResult(self, query_str):
        """
            return query result as list.
        :rtype : list
        :param query_str:
        """
        try:
            conn = MySQLdb.connect(**self.connect)
            cursor = conn.cursor()
            cursor.execute(query_str)
            result = cursor.fetchone()
            conn.commit()
            conn.close()
            return result
        except Exception, e:
            logger.error("mysql util error:" + str(e))

    def execSqlWithNoParams(self, sql_str):
        """
            execute sql with out parameters.
        """
        try:
            conn = MySQLdb.connect(**self.connect)
            cursor = conn.cursor()
            result = cursor.execute(sql_str)
            conn.commit()
            conn.close()
            return result
        except Exception, e:
            logger.error("mysql util error:" + str(e))

    def execSqlWithParams(self, sql_str, params_tuple):
        try:
            conn = MySQLdb.connect(**self.connect)
            cursor = conn.cursor()
            result = cursor.execute(sql_str, params_tuple)
            conn.commit()
            conn.close()
            return result
        except Exception, e:
            logger.error("mysql util error:" + str(e))

    def execSqlWithManyParams(self, sql_str, params_tuple_list):
        try:
            conn = MySQLdb.connect(**self.connect)
            cursor = conn.cursor()
            result = cursor.executemany(sql_str, params_tuple_list)
            conn.commit()
            conn.close()
            return result
        except Exception, e:
            logger.error("mysql util error:" + str(e))


if __name__ == '__main__':
    # p = {"host": "localhost", "user": "root", "passwd": "p@ssw0rd", "db": "mydata", "charset": "utf8"}
    # p = {"host": "10.13.83.170", "user": "game", "passwd": "mpc!*game", "db": "sohu_tv", "charset": "utf8",
    #      "secure_auth": "false"}
    # h = DBHandler(p)
    # x = h.queryWithResult("select * from etl_job_history;")
    # for k in x:
    #     print k
    logger.debug("myutil")