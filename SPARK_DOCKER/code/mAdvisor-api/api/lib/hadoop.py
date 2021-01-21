from __future__ import print_function
import subprocess
# import hadoopy
import json
import os
import os.path
from pywebhdfs.webhdfs import PyWebHdfsClient
from pywebhdfs.errors import FileNotFound
from django.conf import settings


def hadoop_put(from_path, to_dir):
    hdfs_file_path = to_dir + '/' + os.path.basename(from_path)
    print("Uploading to hdfs {} : {}".format(from_path, to_dir))
    # subprocess.call(["/usr/local/hadoop/bin/hadoop", "fs", "-put", from_path, to])

    hdfs_client = hadoop_hdfs()
    with open(from_path, newline='') as file:
        hdfs_client.create_file(hdfs_file_path, file)

def hadoop_mkdir(path):
    print("Creating directory {}".format(path))
    # subprocess.call(["/home/hadoop/hadoop-2.8.5/bin/hadoop", "fs", "-mkdir", "-p", path])
    hadoop_hdfs().make_dir(path)

def hadoop_exists(path):
    try:
        hadoop_hdfs().get_file_dir_status(path)
        return True
    except FileNotFound as e:
        return False

def hadoop_ls(path='/'):
    print("Looking for {}".format(path))
    result = hadoop_hdfs().list_dir(path)
    return result['FileStatuses']['FileStatus']

def hadoop_r():
	subprocess.call(["/usr/local/hadoop/bin/hadoop"])

def hadoop_hdfs_url(path=''):
    return "hdfs://localhost:9000"

def hadoop_read_file(path='', parse_json = True):
    print("Reading file: " + path)
    data = hadoop_hdfs().read_file(path)
    if parse_json :
        return json.loads(data.replace('\n', ''))
    return data

def hadoop_del_file(path):
    hadoop_hdfs().delete_file_dir(path)

def hadoop_read_output_file(path):
    list = hadoop_ls(path)
    for item in list:
        if item['length'] > 0:
            filled_part = path + "/" + item['pathSuffix']
            print("Found at: " + filled_part)
            return hadoop_read_file(filled_part)
    return {}

def hadoop_get_full_url(path):
    return "hdfs://" + settings.HDFS['host'] + ":8020" + path

def hadoop_hdfs():
    conf = settings.HDFS
    print("conf:", conf)
    return PyWebHdfsClient(host= conf['host'],port= conf['port'], user_name=conf['user.name'])
