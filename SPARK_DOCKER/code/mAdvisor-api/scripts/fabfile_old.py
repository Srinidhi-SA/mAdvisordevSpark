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
# from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def set_fabric_env(configuration_detail=None):
    """Set dev environemnt"""

    if configuration_detail is None:
        return -1
    server_details = configuration_detail['server_details']
    path_details = configuration_detail['path_details']
    type = configuration_detail['type']
    gunicorn_details = configuration_detail['gunicorn_details']

    key_file = BASE_DIR + server_details['pem_detail']


    env.key_filename=[key_file]
    env.host_string="{0}@{1}".format(server_details.get('username'), server_details.get('host'))
    env.gunicorn_wsgi_app = gunicorn_details['gunicorn_wsgi_app']
    env.gunicorn_pidpath = path_details["base_remote_path"] + gunicorn_details['gunicorn_pidpath']
    env.gunicorn_bind = gunicorn_details['gunicorn_bind']
    env["server_details"] = server_details
    env["path_details"] = path_details

    return {'server_details': server_details, 'path_details': path_details, 'type': type}


def get_branch_details(branch=None):
    configuration_detail = configuration_details()
    # print(configuration_detail.keys())
    return configuration_detail[branch]


@task
def deploy_react(branch="dev"):
    """
    Default deploy to development. Other options are production
    """
    details = get_branch_details(branch)
    set_fabric_env(details)
    # print details
    path_details= details['path_details']
    server_details= details['server_details']
    k = details['type']
    npm_install_and_deploy(
        server_details=server_details,
        path_details=path_details,
        type=k
    )
    change_config_file(branch=branch)


@task
def deploy_api(branch="dev"):
    """
    Default deploy to development
    :param type:
    :return:
    """
    details = get_branch_details(branch)
    set_fabric_env(details)
    # print details
    path_details= details['path_details']
    server_details= details['server_details']
    # change_config_file(branch)
    only_for_api_push_and_pull(
        server_details=server_details,
        path_details=path_details
    )
    gunicorn.reload()

@task
def change_config_file(branch='dev'):
    import random
    details = get_branch_details(branch)
    set_fabric_env(details)
    # print details
    path_details= details['path_details']
    server_details= details['server_details']
    deployment_config= details['deployment_config']
    base_remote_path = path_details['base_remote_path']
    text_command = """CONFIG_FILE_NAME = '{0}'\nUI_VERSION = '{1}'
    """.format(deployment_config, random.randint(100000,10000000))
    config_file_path = BASE_DIR + '/config/settings/config_file_name_to_run.py'
    react_env = BASE_DIR + '/static/react/src/app/helpers/env.js'
    react_npm_log = BASE_DIR + '/static/react/npm-debug.log'
    local('rm {0}'.format(config_file_path))
    local('echo "{0}" > {1}'.format(text_command, config_file_path))

    with cd(BASE_DIR):

        # unecessary lock file
        if os.path.exists(BASE_DIR + '/static/react/package-lock.json'):
            local('git checkout {0}'.format(BASE_DIR + '/static/react/package-lock.json'))

        if os.path.exists(config_file_path) is True:
            local('git add {0}'.format(config_file_path))

        if os.path.exists(react_env) is True:
            local('git checkout {0}'.format(react_env))

        if os.path.exists(react_npm_log) is True:
            ls_react_npm_log = local('ls {0}'.format(react_npm_log), capture=True)
            if 'cannot access' in ls_react_npm_log:
                pass
            else:
                #local('git checkout {0}'.format(react_npm_log),capture=False)
                pass
        local('git commit -m "version changed. Automated Deployment."')

    only_for_api_push_and_pull(
        server_details=server_details,
        path_details=path_details
    )
    gunicorn.reload()


@task
def deploy_api_and_migrate(branch="dev"):
    """
    Default deploy to development
    :param type:
    :return:
    """

    details = get_branch_details(branch)
    set_fabric_env(details)
    # print details
    path_details= details['path_details']
    server_details= details['server_details']

    only_for_api_push_and_pull(
        server_details=server_details,
        path_details=path_details
    )
    pip_install_and_deploy_remote(
        base_remote_path=path_details['base_remote_path']
    )
    gunicorn.reload()


def do_npm_install(react_path):
    with lcd(BASE_DIR + react_path):
        local("rm -rf dist")
        local("npm install")


def do_npm_run(branch, react_path):
    with lcd(BASE_DIR + react_path):
        if "development" == branch:
            local("npm run buildDev")
        elif "production" == branch:
            local("npm run buildProd")
        elif "local" == branch:
            local("npm run buildLinux")
        elif "luke" == branch:
            local("npm run buildLuke")
        elif "leia" == branch:
            local("npm run buildLeia")
        elif "cwpoc" == branch:
            local("npm run buildCwpoc")

def deploy_dist_to_destination(base_remote_path, react_path):
    import random
    with cd(base_remote_path + react_path):
        run("cp -r dist dist_{0}".format(random.randint(10,100)))

    put(
        local_path = BASE_DIR + react_path + "/dist",
        remote_path = base_remote_path + react_path,
        use_sudo=True
    )


def npm_install_and_deploy(server_details, path_details, type="development"):
    do_npm_install(path_details['react_path'])
    do_npm_run(
        branch=type,
        react_path=path_details['react_path']
    )

    # print path_details['base_remote_path'], path_details['react_path']
    deploy_dist_to_destination(
        base_remote_path=path_details['base_remote_path'],
        react_path=path_details['react_path']
    )


def pip_install_and_deploy_remote(base_remote_path):
    with cd(base_remote_path):
        # sudo('pip install -r requirements.txt')
        run('python manage.py migrate')
        sudo('apt-get install python-matplotlib')


def pull_ui_and_merge_to_api():
    is_done = False

    try:
        with lcd(BASE_DIR):
            capture = local("git status", capture=True)
            # print capture
            if "Changes not staged for commit" in capture:
                abort("Unstaged changes. Please commit or stash.")
                # local("git stash")

            local("git checkout {0}".format(api_branch))
            capture = local("git merge --ff origin/{0} -m 'Merging {1} into {2}'".format(
                ui_branch,
                ui_branch,
                api_branch
            ), capture=True)

            if 'conflict' in capture:
                abort('Resolve Conflicts')

            push_api_to_remote()
            is_done = True
    except Exception as err:
        print(err)

    if is_done:
        pull_api_at_remote()
    else:
        print("Keep Calm. Wait. Take a Breath. Remember Absurdism.")


def push_api_to_remote(api_branch):

    try:
        with lcd(BASE_DIR):

            capture = local("git status", capture=True)
            # print capture
            if "Changes not staged for commit" in capture:
                abort("Unstaged changes. Please commit or stash.")
                local("git stash")

            local("git checkout {0}".format(api_branch))

            capture = local("git push origin {0}".format(api_branch))
            # print capture
    except Exception as err:
        print(err)

    finally:
        print("finally loop.")


def pull_api_at_remote(base_remote_path, api_branch):
    try:
        with cd(base_remote_path):
            capture = run("git status")
            print(capture)
            if "Changes not staged for commit" in capture:
                # abort("Unstaged changes. Please commit or stash.")
                run("git stash")

            run("git checkout {0}".format(api_branch))
            run("git pull origin {0}".format(api_branch))
            # run("git stash apply")

            sudo("pip install -r requirements.txt")
            #run('python manage.py makemigrations')
            run('python manage.py migrate')

    except Exception as err:
        print(err)

    finally:
        print("finally loop.")


def only_for_api_push_and_pull(server_details, path_details):
    push_api_to_remote(path_details['api_branch'])
    pull_api_at_remote(
        path_details['base_remote_path'],
        path_details['api_branch']
    )


def apt_get(*packages):
    sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)


def install_mysql():
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')
    if result.failed is False:
        warn('MySQL is already installed')
        return
    mysql_password = prompt('Please enter MySQL root password:')
    sudo('echo "mysql-server-5.0 mysql-server/root_password password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    sudo('echo "mysql-server-5.0 mysql-server/root_password_again password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    apt_get('mysql-server')


@task
def uptime(branch="dev"):

    details = get_branch_details(branch)
    set_fabric_env(details)
    print(details)
    path_details= details['path_details']
    server_details= details['server_details']
    run('ls')


@task
def remember_git_cache_local_and_remote(branch="dev"):
    """
    remember git password.
    """
    details = get_branch_details(branch)
    set_fabric_env(details)
    print(details)
    path_details= details['path_details']
    server_details= details['server_details']

    local("git config --global credential.helper cache")
    local("git config --global credential.helper 'cache --timeout=360000'")
    run("git config --global credential.helper cache")
    run("git config --global credential.helper 'cache --timeout=360000'")

@task
def cleanup_static_react_old_dist(branch="dev"):
    """
    cleaup dist_files from static_react
    """
    details = get_branch_details(branch)
    set_fabric_env(details)
    print(details)
    path_details= details['path_details']
    server_details= details['server_details']

    base_remote_path = path_details.get('base_remote_path')
    react_path = path_details.get('react_path')

    with cd(base_remote_path + react_path):
        run('mv dist_* ~/old_dist')


def create_database(branch="development"):
    details = get_branch_details(branch)
    set_fabric_env(details)
    print(details)
    path_details = details['path_details']
    server_details = details['server_details']

    db_name = "madvisor"
    user_name = "marlabs"
    host= "localhost"
    passowrd = "Password@123"

    # CREATE DATABASE myproject CHARACTER SET UTF8;
    run("CREATE DATABASE {0} CHARACTER SET UTF8;".format(db_name))

    # CREATE USER marlabs@localhost IDENTIFIED BY 'Password@123';
    run("CREATE USER {0}@{1} IDENTIFIED BY '{2}';".format(user_name, host, passowrd))

    # GRANT ALL PRIVILEGES ON madvisor.* TO marlabs@localhost;
    run("GRANT ALL PRIVILEGES ON {0}.* TO {1}@{2};".format(db_name, user_name, host))


@task
def download_sql_and_dump(branch='dev'):
    import time
    details = get_branch_details(branch)
    set_fabric_env(details)
    print(details)
    path_details= details['path_details']
    server_details= details['server_details']
    current_time = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
    base_remote_path = path_details.get('base_remote_path')
    dump_file_name = "datadump{0}.json".format(current_time)
    tar_dump_file_name = dump_file_name + ".tar.gz"
    base_remote_path_json = base_remote_path + "/" + tar_dump_file_name
    local_dumping_path = '/tmp'
    local_tar_dumping_file_path = local_dumping_path + '/' + tar_dump_file_name
    local_dumping_file_path = local_dumping_path + '/' + dump_file_name

    with cd(base_remote_path):
        run("python manage.py dumpdata -e contenttypes -e auth.Permission > {0}".format(dump_file_name))
        run("tar -zcvf {0} {1}".format(tar_dump_file_name, dump_file_name))
        get(base_remote_path_json, local_dumping_path)
        run('rm {0}'.format(dump_file_name))
        run('rm {0}'.format(tar_dump_file_name))

    with lcd(local_dumping_path):
        local('tar -xzvf {0}'.format(local_tar_dumping_file_path))

    with lcd(BASE_DIR):
        local('python manage.py loaddata {0}'.format(local_dumping_file_path))


@task
def load_local_sql_dump_data(filepath=None):
    with lcd(BASE_DIR):
        local('python manage.py loaddata {0}'.format(filepath))
    local("cat 'Done.'")


@task
def restart_jobserver(branch="development"):

    key_file = BASE_DIR + "/config/keyfiles/TIAA.pem"

    if "development" == branch:
        username = 'hadoop'
        host = '34.205.203.38'
        port = '8090'
    else:
        username = 'hadoop'
        host = '174.129.163.0'
        port = '8090'
    env.key_filename=[key_file]
    env.host_string="{0}@{1}".format(username, host)

    server_start_process_id = sudo("netstat -nlp |grep 8090| awk  '{print $7}' |cut -f1 -d'/'")
    print(server_start_process_id, type(server_start_process_id), str(server_start_process_id), end=' ')

    capture = run('/tmp/job-server/server_stop.sh')

    if files.exists('/tmp/job-server/spark-jobserver.pid'):
        run("rm /tmp/job-server/spark-jobserver.pid")
    import time
    time.sleep(10)
    if "Job server not running" in capture:
        if str(server_start_process_id) == "" :
            pass
        else:
            print("killing server_start_process_id")
            print("command to kill")
            print("-------")
            print("kill -9 {0}".format(server_start_process_id))
            print("-------")
            kill_capture = sudo("kill -9 {0}".format(server_start_process_id))


    output=sudo('cd /tmp/job-server && /bin/bash server_start.sh', pty=False)

    time.sleep(5)

    run('''curl -X POST "{0}:{1}/contexts/{2}?context-factory=spark.jobserver.python.PythonSQLContextFactory"
            '''.format(
        host,
        port
        , 'pysql-context'
    )
    )


def configuration_details():


    configuration_detail = {
        'luke': {
            'server_details': {
                "known name": "luke.marlabsai.com",
                "username": "ubuntu",
                "host": "34.196.22.246",
                "port": "9012",
                "initail_domain": "/api",
                'pem_detail': "/config/keyfiles/TIAA.pem"
            },
            'path_details': {
                "react_path": "/static/react",
                "asset_path": "/static/asset",
                "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api",
                "ui_branch": "api_ui_dev_staging",
                "api_branch": "api_ui_dev_staging"
            },
            'type': 'luke',
            'gunicorn_details': {
                'gunicorn_wsgi_app': 'config.wsgi:application',
                'gunicorn_pidpath': "/gunicorn.pid",
                'gunicorn_bind': "0.0.0.0:9012"
            },
            'deployment_config': 'luke'
        },
        'madvisor': {
            'server_details': {
                "known name": "madvisor.marlabsai.com",
                "username": "ubuntu",
                "host": "34.196.22.246",
                "port": "9012",
                "initail_domain": "/api",
                'pem_detail': "/config/keyfiles/TIAA.pem"
            },
            'path_details': {
                "react_path": "/static/react",
                "asset_path": "/static/asset",
                "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api",
                "ui_branch": "env_vivek_fe",
                "api_branch": "env_vivek_fe"
            },
            'type': 'luke',
            'gunicorn_details': {
                'gunicorn_wsgi_app': 'config.wsgi:application',
                'gunicorn_pidpath': "/gunicorn.pid",
                'gunicorn_bind': "0.0.0.0:9012"
            },
            'deployment_config': 'luke'
        },

        'dev': {
            'server_details': {
                "known name": "madvisordev.marlabsai.com",
                "username": "ubuntu",
                "host": "35.172.209.49",
                "port": "9012",
                "initail_domain": "/api",
                'pem_detail': "/config/keyfiles/TIAA.pem"
            },
            'path_details': {
                "react_path": "/static/react",
                "asset_path": "/static/asset",
                "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api",
                "ui_branch": "model_management",
                "api_branch": "model_management"
            },
            'type':'development',
            'gunicorn_details': {
                'gunicorn_wsgi_app': 'config.wsgi:application',
                'gunicorn_pidpath': "/gunicorn.pid",
                'gunicorn_bind': "0.0.0.0:9012"
            },
            'deployment_config': 'development'
        },
        'dev_9015': {
            'server_details': {
                "known name": "madvisordev.marlabsai.com",
                "username": "ubuntu",
                "host": "34.196.204.54",
                "port": "9015",
                "initail_domain": "/api",
                'pem_detail': "/config/keyfiles/TIAA.pem"
            },
            'path_details': {
                "react_path": "/static/react",
                "asset_path": "/static/asset",
                "base_remote_path": "/home/ubuntu/codebase/dummy_servers/mAdvisor-api",
                "ui_branch": "api_ui_dev_metadata",
                "api_branch": "api_ui_dev_metadata"
            },
            'type': 'development',
            'gunicorn_details': {
                'gunicorn_wsgi_app': 'config.wsgi:application',
                'gunicorn_pidpath': "/gunicorn.pid",
                'gunicorn_bind': "0.0.0.0:9015"
            },
            'deployment_config': 'development'
        },
        'leia': {
            'server_details': {
                "known name": "leia.marlabsai.com",
                "username": "ubuntu",
                "host": "34.196.22.246",
                "port": "9015",
                "initail_domain": "/api",
                'pem_detail': "/config/keyfiles/TIAA.pem"
            },
            'path_details': {
                "react_path": "/static/react",
                "asset_path": "/static/asset",
                "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api_2",
                "ui_branch": "vivek_fe",
                "api_branch": "vivek_fe"
            },
            'type':'leia',
            'gunicorn_details': {
                'gunicorn_wsgi_app': 'config.wsgi:application',
                'gunicorn_pidpath': "/gunicorn.pid",
                'gunicorn_bind': "0.0.0.0:9015"
            },
            'deployment_config': 'leia'
        },
        'cwpoc': {
            'server_details': {
                "known name": "cwpoc.marlabsai.com",
                "username": "ubuntu",
                "host": "34.196.22.246",
                "port": "9016",
                "initail_domain": "/api",
                'pem_detail': "/config/keyfiles/TIAA.pem"
            },
            'path_details': {
                "react_path": "/static/react",
                "asset_path": "/static/asset",
                "base_remote_path": "/home/ubuntu/codebase/mAdvisor-api_cwpoc",
                "ui_branch": "api_ui_dev_staging",
                "api_branch": "api_ui_dev_staging"
            },
            'type': 'cwpoc',
            'gunicorn_details': {
                'gunicorn_wsgi_app': 'config.wsgi:application',
                'gunicorn_pidpath': "/gunicorn.pid",
                'gunicorn_bind': "0.0.0.0:9016"
            },
            'deployment_config': 'cwpoc'
        },
    }

    return configuration_detail


@task
def testpad():
    import os
    local('pwd')
    get_local_home()


def get_local_home():
    localhome = local('echo $HOME', capture=True)
    return localhome


def get_local_user_name():
    localusername = local('whoami', capture=True)
    return localusername
