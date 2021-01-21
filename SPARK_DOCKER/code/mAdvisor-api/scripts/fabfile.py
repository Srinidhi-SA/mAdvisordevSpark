from __future__ import print_function
from builtins import input
from fabric.api import task, run, env
"""
Usage
        fab <function_name>:[arg,arg1=val1]
        e.g. fab deploy_api:branch=dev
        e.g. fab deploy_api:branch=leia
        e.g. fab deploy_api:branch=luke
        e.g. fab deploy_api:branch=dev_9015
        e.g. fab deploy_api:branch=cwpoc

        e.g. fab deploy_react:branch=dev
        e.g. fab deploy_react:branch=leia
        e.g. fab deploy_react:branch=luke
        e.g. fab deploy_react:branch=dev_9015
        e.g. fab deploy_react:branch=cwpoc

        e.g. fab deploy_api_and_migrate:branch=dev
        e.g. fab deploy_api_and_migrate:branch=leia
        e.g. fab deploy_api_and_migrate:branch=luke

List
        fab -list
"""
from __future__ import print_function

from builtins import str
from fabric.api import *
import os
from fabric.contrib import files
import fabric_gunicorn as gunicorn
from django.conf import settings
from fabric.context_managers import cd
import random


env.use_ssh_config = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env.hosts = ['dev_model_docker']



@task
def alt_deploy_api():
    down_all()
    print("DOWN ALL CONTAINERS")
    with cd("/home/ubuntu/env_deployment/mAdvisor-api"):
        run("git checkout env_vivek_fe ; sudo git pull")
        print("LATEST CODE PULLED FROM GITHUB")
        run("sudo cp -r /home/ubuntu/env_deployment/mAdvisor-api /tmp/")
        print("CODE COPIED TO TMP")
        run("sudo rm -f /tmp/mAdvisor-api/api/.gitignore && sudo rm -f -r /tmp/mAdvisor-api/api/.git")
        print("REMOVED .GIT FILES")
        run("sudo tar -zcvf /tmp/code.tgz /tmp/mAdvisor-api")
        print("MADE CODE TAR FILE")
        run("sudo cp /tmp/code.tgz /home/ubuntu/env_deployment/docker_kubernetes/mAdvisor-api/")
        print("COPIED TAR FILE TO API")
        run("sudo cp /tmp/code.tgz /home/ubuntu/env_deployment/docker_kubernetes/spark_docker/")
        print("COPIED TAR FILE TO SPARK")
        with cd("/home/ubuntu/env_deployment/docker_kubernetes/mAdvisor-api"):
            run("sudo docker build -t api:latest .")
            print("BUILT API IMAGE")

    with cd("/home/ubuntu/env_deployment/docker_kubernetes/spark_docker"):
        run("sudo docker build -t spark:latest .")
        print("BUILT SPARK IMAGE")
    up_all()
    print("UP ALL CONTAINERS")
    gunicorn.reload()
    print("** DEPLOYMENT COMPLETE **")



@task
def mysql_api_redis_nginx_down():
    run("cd /home/ubuntu/env_deployment/docker_kubernetes/mysql_api_redis_nginx_compose && sudo docker-compose down")



@task
def hadoop_spark_down():
    run("cd /home/ubuntu/env_deployment/docker_kubernetes/hadoop_spark_compose && sudo docker-compose -f hadoop_spark_compose.yml down")




@task
def mysql_api_redis_nginx_up():
    run("cd /home/ubuntu/env_deployment/docker_kubernetes/mysql_api_redis_nginx_compose && sudo docker-compose up -d")



@task
def hadoop_spark_up():
    run("cd /home/ubuntu/env_deployment/docker_kubernetes/hadoop_spark_compose && sudo docker-compose -f hadoop_spark_compose.yml up -d")



# <<<<<<< HEAD
# @task
# def up_all():
#     mysql_api_redis_nginx_up()
#     hadoop_spark_up()
#
# =======
#             push_api_to_remote()
#             is_done = True
#     except Exception as err:
#         print(err)
#
#     if is_done:
#         pull_api_at_remote()
#     else:
#         print("Keep Calm. Wait. Take a Breath. Remember Absurdism.")
# >>>>>>> 97d1573cd86b06f237d3caecca2551a886da58b9
#
#
# @task
# def down_all():
#     hadoop_spark_down()
#     mysql_api_redis_nginx_down()
#
#
# @task
# def deploy_api():
#     with cd("/home/ubuntu/env_deployment/mAdvisor-api"):
#         '''
#         print "CHECKING BRANCH STATUS..."
#         capture = run("git status")
#         print capture
#         if "Changes not staged for commit" in capture:
#             run("git stash")
#             print "UNCOMMITTED CHANGES STASHED"
#         else:
#             print "NO UNSTASHED CHANGES. PROCEEDING..."
#         '''
#         run("sudo git checkout env_vivek_fe ; sudo git pull")
#         print("LATEST API CODE PULLED FROM GITHUB")
#         run("sudo cp -r /home/ubuntu/env_deployment/mAdvisor-api /tmp/")
#         print("CODE COPIED TO TMP")
#         run("sudo rm -f /tmp/mAdvisor-api/api/.gitignore && sudo rm -f -r /tmp/mAdvisor-api/api/.git")
#         print("REMOVED .GIT FILES")
#
#         container_name = run("sudo docker ps -aqf \"name=api\" | head -n 1")
#         print(container_name)
#         print("FETCHED API CONTAINER ID")
#         run("sudo docker cp /tmp/mAdvisor-api "+container_name+":/home/mAdvisor/")
#         print("LATEST API CODE PUT INSIDE API CONTAINER")
#
#         ifReqInstAPI = input("API Requirements installation required?(y/n)")
#         ifMigrateAPI = input("Database migrations required?(y/n)")
#         if (ifReqInstAPI.strip().lower() == 'y'  and  ifMigrateAPI.strip().lower() == 'y'):
#             run ("docker exec "+container_name+" bash -c  \"cd ..  &&  . myenv/bin/activate  &&  pip install -r requirements.txt  &&  cd mAdvisor-api/  &&  python manage.py makemigrations  &&  python manage.py migrate\"")
#             print("API REQUIREMENTS INSTALLED AND DATABASES MIGRATED")
#         elif (ifReqInstAPI.strip().lower() == 'y'):
#             run ("docker exec "+container_name+" bash -c  \"cd ..  &&  . myenv/bin/activate  &&  pip install -r requirements.txt\"")
#             print("API REQUIREMENTS INSTALLED")
#         else:
#              print("API REQUIREMENTS INSTALL AND DATABASE MIGRATE AVOIDED")
#
#         container_name = run("sudo docker ps -aqf \"name=spark\" | head -n 1")
#         print(container_name)
#         print("FETCHED SPARK CONTAINER ID")
#         run("sudo docker cp /tmp/mAdvisor-api "+container_name+":/home/mAdvisor/")
#         print("LATEST API CODE PUT INSIDE SPARK CONTAINER")
#
#         ifReqInstSPARK = input("SPARK Requirements installation required?(y/n)")
#         if (ifReqInstSPARK.strip().lower() == 'y'):
#             run ("docker exec "+container_name+" bash -c  \"pip install -r requirements.txt\"")
#             print("SPARK REQUIREMENTS INSTALLED")
#         else:
#             print("SPARK REQUIREMENTS INSTALL AVOIDED")
#
#         reloadCelery = input("Celery reload required?(y/n)")
#         if (reloadCelery.strip().lower() == 'y'):
#             run ('''docker exec '''+container_name+''' bash -c  \"ps auxww | grep celery | grep -v 'grep' | awk '{print $2}' | xargs kill -HUP\"''')
#             print("CELERY GRACEFULLY RELOADED")
#         else:
#             print("CELERY RELOAD AVOIDED")
#
# <<<<<<< HEAD
#
#         #gunicorn.reload()
#         #print "GUNICORN RELOADED"
#     print("** DEPLOYMENT COMPLETE **")
# =======
#             capture = local("git push origin {0}".format(api_branch))
#             # print capture
#     except Exception as err:
#         print(err)
#
#     finally:
#         print("finally loop.")
# >>>>>>> 97d1573cd86b06f237d3caecca2551a886da58b9
#
#
# @task
# def deploy_ml():
#     with cd("/home/ubuntu/env_deployment/mAdvisor-MLScripts"):
#         '''
#         print "CHECKING BRANCH STATUS..."
#             capture = run("git status")
#             print(capture)
#             if "Changes not staged for commit" in capture:
#                 run("git stash")
# <<<<<<< HEAD
#                 print "UNCOMMITTED CHANGES STASHED"
#             else:
#                 print "NO UNSTASHED CHANGES. PROCEEDING..."
#         '''
#         run("sudo git checkout staging ; sudo git pull")
#         print("LATEST ML CODE PULLED FROM GITHUB")
# =======
#
#             run("git checkout {0}".format(api_branch))
#             run("git pull origin {0}".format(api_branch))
#             # run("git stash apply")
#
#             sudo("pip install -r requirements.txt")
#             #run('python manage.py makemigrations')
#             run('python manage.py migrate')
#
#     except Exception as err:
#         print(err)
#
#     finally:
#         print("finally loop.")
#
#
# def only_for_api_push_and_pull(server_details, path_details):
#     push_api_to_remote(path_details['api_branch'])
#     pull_api_at_remote(
#         path_details['base_remote_path'],
#         path_details['api_branch']
#     )
#
#
# def apt_get(*packages):
#     sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)
# >>>>>>> 97d1573cd86b06f237d3caecca2551a886da58b9
#
#
#         run("sudo su -c  \"cd /home/ubuntu/env_deployment  &&  . venv/bin/activate  &&  cd mAdvisor-MLScripts  &&  python setup.py bdist_egg\"")
#
#         container_name = run("sudo docker ps -aqf \"name=spark\" | head -n 1")
#         print(container_name)
#         print("FETCHED SPARK CONTAINER ID")
#         run("sudo docker cp /home/ubuntu/env_deployment/mAdvisor-MLScripts/dist/marlabs_bi_jobs-0.0.0-py2.7.egg "+container_name+":/home/mAdvisor/mAdvisor-api/scripts/")
#         print("LATEST ML CODE PUT INSIDE SPARK CONTAINER")
#     print("** DEPLOYMENT COMPLETE **")
#
#
# <<<<<<< HEAD
#
#
#
# @task
# def deploy_ui():
#
#     with cd("/home/ubuntu/env_deployment/mAdvisor-api"):
#         '''
#         print "CHECKING BRANCH STATUS..."
#         capture = run("git status")
#         print capture
#         if "Changes not staged for commit" in capture:
#             run("git stash")
#             print "UNCOMMITTED CHANGES STASHED"
#         else:
#             print "NO UNSTASHED CHANGES. PROCEEDING..."
#         '''
#         run("git checkout env_vivek_fe ; sudo git pull")
#         print("LATEST UI CODE PULLED FROM GITHUB")
#
#     run("sudo cp -r /home/ubuntu/env_deployment/mAdvisor-api /home/ubuntu/env_deployment/UI_deployment/")
#     with cd("/home/ubuntu/env_deployment/UI_deployment/mAdvisor-api/static/react/"):
#         run("sudo su -c \"curl -sL https://deb.nodesource.com/setup_8.x | bash -  &&  sudo apt-get install nodejs -y  &&  sudo node -v  &&  sudo npm install  &&  sudo npm -v  &&  npm audit fix  &&  sudo npm run buildDev\"")
# =======
#     details = get_branch_details(branch)
#     set_fabric_env(details)
#     print(details)
#     path_details= details['path_details']
#     server_details= details['server_details']
#     run('ls')
#
#
# @task
# def remember_git_cache_local_and_remote(branch="dev"):
#     """
#     remember git password.
#     """
#     details = get_branch_details(branch)
#     set_fabric_env(details)
#     print(details)
#     path_details= details['path_details']
#     server_details= details['server_details']
#
#     local("git config --global credential.helper cache")
#     local("git config --global credential.helper 'cache --timeout=360000'")
#     run("git config --global credential.helper cache")
#     run("git config --global credential.helper 'cache --timeout=360000'")
#
# @task
# def cleanup_static_react_old_dist(branch="dev"):
#     """
#     cleaup dist_files from static_react
#     """
#     details = get_branch_details(branch)
#     set_fabric_env(details)
#     print(details)
#     path_details= details['path_details']
#     server_details= details['server_details']
#
#     base_remote_path = path_details.get('base_remote_path')
#     react_path = path_details.get('react_path')
#
#     with cd(base_remote_path + react_path):
#         run('mv dist_* ~/old_dist')
#
#
# def create_database(branch="development"):
#     details = get_branch_details(branch)
#     set_fabric_env(details)
#     print(details)
#     path_details = details['path_details']
#     server_details = details['server_details']
#
#     db_name = "madvisor"
#     user_name = "marlabs"
#     host= "localhost"
#     passowrd = "Password@123"
#
#     # CREATE DATABASE myproject CHARACTER SET UTF8;
#     run("CREATE DATABASE {0} CHARACTER SET UTF8;".format(db_name))
#
#     # CREATE USER marlabs@localhost IDENTIFIED BY 'Password@123';
#     run("CREATE USER {0}@{1} IDENTIFIED BY '{2}';".format(user_name, host, passowrd))
#
#     # GRANT ALL PRIVILEGES ON madvisor.* TO marlabs@localhost;
#     run("GRANT ALL PRIVILEGES ON {0}.* TO {1}@{2};".format(db_name, user_name, host))
#
#
# @task
# def download_sql_and_dump(branch='dev'):
#     import time
#     details = get_branch_details(branch)
#     set_fabric_env(details)
#     print(details)
#     path_details= details['path_details']
#     server_details= details['server_details']
#     current_time = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
#     base_remote_path = path_details.get('base_remote_path')
#     dump_file_name = "datadump{0}.json".format(current_time)
#     tar_dump_file_name = dump_file_name + ".tar.gz"
#     base_remote_path_json = base_remote_path + "/" + tar_dump_file_name
#     local_dumping_path = '/tmp'
#     local_tar_dumping_file_path = local_dumping_path + '/' + tar_dump_file_name
#     local_dumping_file_path = local_dumping_path + '/' + dump_file_name
#
#     with cd(base_remote_path):
#         run("python manage.py dumpdata -e contenttypes -e auth.Permission > {0}".format(dump_file_name))
#         run("tar -zcvf {0} {1}".format(tar_dump_file_name, dump_file_name))
#         get(base_remote_path_json, local_dumping_path)
#         run('rm {0}'.format(dump_file_name))
#         run('rm {0}'.format(tar_dump_file_name))
#
#     with lcd(local_dumping_path):
#         local('tar -xzvf {0}'.format(local_tar_dumping_file_path))
#
#     with lcd(BASE_DIR):
#         local('python manage.py loaddata {0}'.format(local_dumping_file_path))
# >>>>>>> 97d1573cd86b06f237d3caecca2551a886da58b9
#
#         print("BUNDLE.JS FILE OF LATEST CODE CREATED")
#
#
#     container_name = run("sudo docker ps -aqf \"name=nginx\" | head -n 2 | tail -n 1")
#     print(container_name)
#     print("FETCHED NGINX CONTAINER ID")
#     run("sudo docker cp /home/ubuntu/env_deployment/UI_deployment/mAdvisor-api/static/react/dist/app/bundle.js "+container_name+":/home/static/react/dist/app/")
#     print("LATEST UI CODE PUT INSIDE NGINX CONTAINER")
#
# <<<<<<< HEAD
#     #Task: Avoid updating UI Version In script.
#     #with cd("/home/ubuntu/env_deployment/UI_deployment/mAdvisor-api/config/settings"):
#     #    text_command = 'CONFIG_FILE_NAME = \'luke\'\nUI_VERSION = \'{0}\''.format(random.randint(100000,10000000))
#     #    print text_command
#     #    run("sudo su -c \"echo '{0}' > config_file_name_to_run.py\"".format(text_command))
#     #    run('''sudo sed -i "s/luke/'luke'/"  config_file_name_to_run.py''')
#         #run('''sudo sed -i "s/4309824/'4309824'/"  config_file_name_to_run.py''')
#     #    print "CONFIG FILENAME TO RUN UPDATED"
# =======
# @task
# def restart_jobserver(branch="development"):
#
#     key_file = BASE_DIR + "/config/keyfiles/TIAA.pem"
#
#     if "development" == branch:
#         username = 'hadoop'
#         host = '34.205.203.38'
#         port = '8090'
#     else:
#         username = 'hadoop'
#         host = '174.129.163.0'
#         port = '8090'
#     env.key_filename=[key_file]
#     env.host_string="{0}@{1}".format(username, host)
#
#     server_start_process_id = sudo("netstat -nlp |grep 8090| awk  '{print $7}' |cut -f1 -d'/'")
#     print(server_start_process_id, type(server_start_process_id), str(server_start_process_id), end=' ')
#
#     capture = run('/tmp/job-server/server_stop.sh')
#
#     if files.exists('/tmp/job-server/spark-jobserver.pid'):
#         run("rm /tmp/job-server/spark-jobserver.pid")
#     import time
#     time.sleep(10)
#     if "Job server not running" in capture:
#         if str(server_start_process_id) == "" :
#             pass
#         else:
#             print("killing server_start_process_id")
#             print("command to kill")
#             print("-------")
#             print("kill -9 {0}".format(server_start_process_id))
#             print("-------")
#             kill_capture = sudo("kill -9 {0}".format(server_start_process_id))
#
#
#     output=sudo('cd /tmp/job-server && /bin/bash server_start.sh', pty=False)
#
#     time.sleep(5)
#
#     run('''curl -X POST "{0}:{1}/contexts/{2}?context-factory=spark.jobserver.python.PythonSQLContextFactory"
#             '''.format(
#         host,
#         port
#         , 'pysql-context'
#     )
#     )
#
#
# def configuration_details():
#
#
#     configuration_detail = {
#         'luke': {
#             'server_details': {
#                 "known name": "luke.marlabsai.com",
#                 "username": "ubuntu",
#                 "host": "34.196.22.246",
#                 "port": "9012",
#                 "initail_domain": "/api",
#                 'pem_detail': "/config/keyfiles/TIAA.pem"
#             },
#             'path_details': {
#                 "react_path": "/static/react",
#                 "asset_path": "/static/asset",
#                 "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api",
#                 #"ui_branch": "api_ui_dev_staging",
#                 #"api_branch": "api_ui_dev_staging"
#                 "ui_branch": "env_vivek_fe",
#                 "api_branch": "env_vivek_fe"
#             },
#             'type': 'luke',
#             'gunicorn_details': {
#                 'gunicorn_wsgi_app': 'config.wsgi:application',
#                 'gunicorn_pidpath': "/gunicorn.pid",
#                 'gunicorn_bind': "0.0.0.0:9012"
#             },
#             'deployment_config': 'luke'
#         },
#         'madvisor': {
#             'server_details': {
#                 "known name": "madvisor.marlabsai.com",
#                 "username": "ubuntu",
#                 "host": "34.196.22.246",
#                 "port": "9012",
#                 "initail_domain": "/api",
#                 'pem_detail': "/config/keyfiles/TIAA.pem"
#             },
#             'path_details': {
#                 "react_path": "/static/react",
#                 "asset_path": "/static/asset",
#                 "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api",
#                 "ui_branch": "env_vivek_fe",
#                 "api_branch": "env_vivek_fe"
#             },
#             'type': 'luke',
#             'gunicorn_details': {
#                 'gunicorn_wsgi_app': 'config.wsgi:application',
#                 'gunicorn_pidpath': "/gunicorn.pid",
#                 'gunicorn_bind': "0.0.0.0:9012"
#             },
#             'deployment_config': 'luke'
#         },
#
#         'dev': {
#             'server_details': {
#                 "known name": "madvisordev.marlabsai.com",
#                 "username": "ubuntu",
#                 "host": "35.172.209.49",
#                 "port": "9012",
#                 "initail_domain": "/api",
#                 'pem_detail': "/config/keyfiles/TIAA.pem"
#             },
#             'path_details': {
#                 "react_path": "/static/react",
#                 "asset_path": "/static/asset",
#                 "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api",
#                 "ui_branch": "model_management",
#                 "api_branch": "model_management"
#             },
#             'type':'development',
#             'gunicorn_details': {
#                 'gunicorn_wsgi_app': 'config.wsgi:application',
#                 'gunicorn_pidpath': "/gunicorn.pid",
#                 'gunicorn_bind': "0.0.0.0:9012"
#             },
#             'deployment_config': 'development'
#         },
#         'dev_9015': {
#             'server_details': {
#                 "known name": "madvisordev.marlabsai.com",
#                 "username": "ubuntu",
#                 "host": "34.196.204.54",
#                 "port": "9015",
#                 "initail_domain": "/api",
#                 'pem_detail': "/config/keyfiles/TIAA.pem"
#             },
#             'path_details': {
#                 "react_path": "/static/react",
#                 "asset_path": "/static/asset",
#                 "base_remote_path": "/home/ubuntu/codebase/dummy_servers/mAdvisor-api",
#                 "ui_branch": "api_ui_dev_metadata",
#                 "api_branch": "api_ui_dev_metadata"
#             },
#             'type': 'development',
#             'gunicorn_details': {
#                 'gunicorn_wsgi_app': 'config.wsgi:application',
#                 'gunicorn_pidpath': "/gunicorn.pid",
#                 'gunicorn_bind': "0.0.0.0:9015"
#             },
#             'deployment_config': 'development'
#         },
#         'leia': {
#             'server_details': {
#                 "known name": "leia.marlabsai.com",
#                 "username": "ubuntu",
#                 "host": "34.196.22.246",
#                 "port": "9015",
#                 "initail_domain": "/api",
#                 'pem_detail': "/config/keyfiles/TIAA.pem"
#             },
#             'path_details': {
#                 "react_path": "/static/react",
#                 "asset_path": "/static/asset",
#                 "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api_2",
#                 "ui_branch": "vivek_fe",
#                 "api_branch": "vivek_fe"
#             },
#             'type':'leia',
#             'gunicorn_details': {
#                 'gunicorn_wsgi_app': 'config.wsgi:application',
#                 'gunicorn_pidpath': "/gunicorn.pid",
#                 'gunicorn_bind': "0.0.0.0:9015"
#             },
#             'deployment_config': 'leia'
#         },
#         'cwpoc': {
#             'server_details': {
#                 "known name": "cwpoc.marlabsai.com",
#                 "username": "ubuntu",
#                 "host": "34.196.22.246",
#                 "port": "9016",
#                 "initail_domain": "/api",
#                 'pem_detail': "/config/keyfiles/TIAA.pem"
#             },
#             'path_details': {
#                 "react_path": "/static/react",
#                 "asset_path": "/static/asset",
#                 "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api_cwpoc",
#                 "ui_branch": "api_ui_dev_staging",
#                 "api_branch": "api_ui_dev_staging"
#             },
#             'type': 'cwpoc',
#             'gunicorn_details': {
#                 'gunicorn_wsgi_app': 'config.wsgi:application',
#                 'gunicorn_pidpath': "/gunicorn.pid",
#                 'gunicorn_bind': "0.0.0.0:9016"
#             },
#             'deployment_config': 'cwpoc'
#         },
#     }
#
#     return configuration_detail
# >>>>>>> 97d1573cd86b06f237d3caecca2551a886da58b9
#
#     container_name = run("sudo docker ps -aqf \"name=api\" | head -n 1")
#     print(container_name)
#     print("FETCHED API CONTAINER ID")
#     run("sudo docker cp /home/ubuntu/env_deployment/UI_deployment/mAdvisor-api/config/settings/config_file_name_to_run.py "+container_name+":/home/mAdvisor/mAdvisor-api/config/settings/")
#     print("CONFIG FILE UPDATED INSIDE API CONTAINER")
#
#     container_name = run("sudo docker ps -aqf \"name=nginx\" | head -n 2 | tail -n 1")
#     print(container_name)
#     print("FETCHED NGINX CONTAINER ID")
#     run("docker exec -it "+container_name+" bash -c \"service nginx reload\"")
#     print("NGINX RELOADED")
#
#     print("** DEPLOYMENT COMPLETE **")



'''
api restarting problem
sudo docker cp /home/ubuntu/env_deployment/UI_deployment/mAdvisor-api/config/settings/config_file_name_to_run.py <api-container-id>:/home/mAdvisor/mAdvisor-api/config/settings/
'''
