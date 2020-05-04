#! /usr/bin/env python3
#
# 2020-05-03 
# Colton Grainger 
# CC-0 Public Domain

"""
Configuration structure
"""

import configparser

config_file_abs_path = '/home/colton/images/config.ini'

# that config.ini file contains two sections, DEFAULT and database
# looks like ...

# [DEFAULT]
# ingest_dir=/home/colton/images/ingest
# output_dir=/home/colton/images/output
# data_dir=/home/colton/images/data
# 
# [database]
# 
# sqlite=no
# # If sqlite=yes, then the imagearchive's SQLAlchemy database URL will be
# #
# # 	sqlite:///:memory:
# #
# # if sqlite=no, then the SQLAlchemy database URL will be of the form
# #
# # 	dialect+driver://username:password@host:port/database
# 
# dialect=mysql
# driver=pymysql
# # pymysql is the recommended driver for SQLAlchemy
# #
# # mysqlconnector, although available at NCAR, is not recommended, c.f. 
# # docs.sqlalchemy.org/en/13/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqlconnector
# 
# user=colton
# pass=
# host=localhost
# database=images

config = configparser.ConfigParser()
config.read(config_file_abs_path)
