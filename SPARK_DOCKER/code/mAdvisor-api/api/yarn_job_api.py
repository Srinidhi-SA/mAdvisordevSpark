from __future__ import print_function
from knit import YARNAPI
from django.conf import settings
import subprocess
import re

yap = YARNAPI(
    rm = settings.YARN.get("host"),
    rm_port = settings.YARN.get("port")
)


def get_detailed_application_info(app_id=None):

    if None == app_id:
        return -1

    return yap.apps_info(app_id=app_id)


def get_brief_application_info(app_id=None):

    if None == app_id:
        return -1

    things_to_keep = [
        u'elapsedTime',
        u'finalStatus',
        u'finishedTime',
        u'memorySeconds',
        u'progress',
        u'queue',
        u'startedTime',
        u'state',
        u'trackingUI',
        u'trackingUrl'
    ]

    new_dict = {}
    old_info = yap.apps_info(app_id=app_id)

    for item in things_to_keep:
        new_dict[item] = old_info[item]

    return new_dict


def kill_application(app_id=None):
    print("################## Inside Kill Application ####################")
    if None == app_id:
        return -1

    kill_status = yap.kill(app_id=app_id)
    print(("Kill Status",kill_status))

    if kill_status is True:
        print("Killed Application.")
    else:
        print("Failed to kill.")


def kill_application_using_fabric(app_id=None):

    if None == app_id:
        return -1

    from fabric.api import env, run
    from django.conf import settings

    HDFS = settings.HDFS
    BASEDIR = settings.BASE_DIR
    emr_file = BASEDIR + "/keyfiles/TIAA.pem"

    env.key_filename = [emr_file]
    env.host_string = "{0}@{1}".format(HDFS["user.name"], HDFS["host"])

    capture = run("yarn application --kill {0}".format(app_id))

    if 'finished' in capture:
        return False
    else:
        return True


def start_yarn_application_again(command_array=None):

    if None == command_array:
        return -1

    try:
        cur_process = subprocess.Popen(command_array, stderr=subprocess.PIPE)
        # TODO: @Ankush need to write the error to error log and standard out to normal log
        for line in iter(lambda: cur_process.stderr.readline(), ''):
            print(line.strip())
            match = re.search('Submitted application (.*)$', line)
            if match:
                application_id = match.groups()[0]
                print("$$" * 100)
                print(application_id)
                print("$$" * 100)
                break
        print("proc", cur_process)
        return {
            "application_id": application_id
        }
    except Exception as e:
        from smtp_email import send_alert_through_email
        send_alert_through_email(e)
