from __future__ import absolute_import, unicode_literals
from __future__ import print_function

from builtins import str
from builtins import map
import random
import time
import base64
import mimetypes
import signal

import os
import time
from celery.decorators import task
from config.settings.config_file_name_to_run import CONFIG_FILE_NAME
from django.conf import settings
import datetime
import simplejson as json
import copy
from api.helper import get_random_model_id, get_mails_from_outlook
from django.contrib.auth.models import User


@task(name="sum_two_numbers")
def add(x, y):
    print("crazy bird {0}{1}".format(x, y))
    return x + y


@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total


@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)


import subprocess
import re
import requests
from api.models import Job, Dataset, Score, Insight, Trainer, StockDataset, Robo, DatasetScoreDeployment, CustomApps, \
    OutlookToken


@task(name='hum_se_hai_zamana_sara', queue=CONFIG_FILE_NAME)
def submit_job_separate_task(command_array, slug):
    import subprocess, os
    my_env = os.environ.copy()
    if settings.HADOOP_CONF_DIR:
        my_env["HADOOP_CONF_DIR"] = settings.HADOOP_CONF_DIR
        my_env["HADOOP_USER_NAME"] = settings.HADOOP_USER_NAME

    try:
        cur_process = subprocess.Popen(command_array, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1,
                                       universal_newlines=True, env=my_env)
        print(cur_process)
    except Exception as e:
        from api.helper import get_db_object
        model_instance = get_db_object(model_name=Job.__name__,
                                       model_slug=slug
                                       )
        model_instance.status = "KILLED"
        model_instance.message = json.dumps({'message': 'Killed while submitting job',
                                             'error': e})
        model_instance.save()
        return "Failed"

    for line in iter(lambda: cur_process.stdout.readline(), ''):
        print(line.strip())
        line = line.strip()
        match = re.search('Submitted application (.*)$', line)
        if match:
            application_id = match.groups()[0]
            print(("<------------------------ YARN APPLICATION ID ---------------------->", application_id))
            from api.helper import get_db_object

            model_instance = get_db_object(model_name=Job.__name__,
                                           model_slug=slug
                                           )
            model_instance.url = application_id
            model_instance.save()
            # Break statement is commented in order to get the complete log of the subprocess
            # break


'''
    time.sleep(10)
    exists = os.path.isfile('/tmp/SparkDriver.log')
    while( exists != True):
      exists = os.path.isfile('/tmp/SparkDriver.log')
      time.sleep(1)
    with open("/tmp/SparkDriver.log") as file:
        data = file.readlines()
        for line in data:
            match = re.search('Submitted application (.*)$', line)
            if match:
                application_id = match.groups()[0]
                print ("############################## Application ID ################################# ", application_id)
                from api.helper import get_db_object
                model_instance = get_db_object(model_name=Job.__name__,
                                           model_slug=slug
                                           )
                model_instance.url = application_id
                model_instance.save()
                dist_file_name = "/tmp/" + str(application_id) + ".driver.log"
                os.rename("/tmp/SparkDriver.log",dist_file_name)
                break
'''


def submit_job_separate_task1(command_array, slug):
    import subprocess, os
    my_env = os.environ.copy()
    if settings.HADOOP_CONF_DIR:
        my_env["HADOOP_CONF_DIR"] = settings.HADOOP_CONF_DIR
        my_env["HADOOP_USER_NAME"] = settings.HADOOP_USER_NAME
    cur_process = subprocess.Popen(command_array, stderr=subprocess.PIPE, env=my_env)
    print(cur_process)
    # TODO: @Ankush need to write the error to error log and standard out to normal log
    for line in iter(lambda: cur_process.stderr.readline(), ''):
        # print(line.strip())
        match = re.search('Submitted application (.*)$', line.decode("utf-8"))
        if match:
            application_id = match.groups()[0]
            from api.helper import get_db_object

            model_instance = get_db_object(model_name=Job.__name__,
                                           model_slug=slug
                                           )
            model_instance.url = application_id
            model_instance.save()
            break


@task(name='write_into_databases', queue=CONFIG_FILE_NAME)
def write_into_databases(job_type, object_slug, results):
    from api import helper
    # import json
    from api.helper import get_db_object
    from api.views import chart_changes_in_metadata_chart, add_slugs

    if job_type in ["metadata", "subSetting"]:
        dataset_object = get_db_object(model_name=Dataset.__name__,
                                       model_slug=object_slug
                                       )

        if "error_message" in results:
            dataset_object.status = "FAILED"
            dataset_object.save()
            return results
        columnData = results['columnData']
        for data in columnData:
            # data["chartData"] = helper.find_chart_data_and_replace_with_chart_data(data["chartData"])
            card_data = data["chartData"]
            if 'dataType' in card_data and card_data['dataType'] == 'c3Chart':
                chart_data = card_data['data']
                final_chart_data = helper.decode_and_convert_chart_raw_data(chart_data, object_slug=object_slug)
                data["chartData"] = chart_changes_in_metadata_chart(final_chart_data)
                data["chartData"]["table_c3"] = []

        results['columnData'] = columnData
        # results['possibleAnalysis'] = settings.ANALYSIS_FOR_TARGET_VARIABLE
        da = []
        for d in results.get('sampleData'):
            da.append(list(map(str, d)))
        results['sampleData'] = da
        # results["modified"] = False

        dataset_object.meta_data = json.dumps(results)
        dataset_object.analysis_done = True
        dataset_object.status = 'SUCCESS'
        dataset_object.save()
        print("Every thing went well. Lets see if more can be done")
        check_if_dataset_is_part_of_datascore_table_and_do_we_need_to_trigger_score(dataset_object.id)
        ####   Check if model job needs to be triggered for email AutoML   ###
        check_if_autoML_model_job_needs_to_be_triggered(dataset_object.id)
        return "Done Succesfully."
    elif job_type == "master":
        insight_object = get_db_object(model_name=Insight.__name__,
                                       model_slug=object_slug
                                       )

        if "error_message" in results:
            insight_object.status = "FAILED"
            insight_object.save()
            return results

        results = add_slugs(results, object_slug=object_slug)
        insight_object.data = json.dumps(results)
        insight_object.analysis_done = True
        insight_object.status = 'SUCCESS'
        insight_object.save()
        return "Done Succesfully."
    elif job_type == "model":
        trainer_object = get_db_object(model_name=Trainer.__name__,
                                       model_slug=object_slug
                                       )

        if "error_message" in results or "model_summary" not in results:
            trainer_object.status = "FAILED"
            trainer_object.save()
            #------------------------------------------------------------------#
            #Sending failure mail on autoML model failure
            if trainer_object.mode == 'autoML':
                outlook_autoML_failure_mail(
                    trainer_object_id=trainer_object.id,
                    error='ML-failure',
                    mail_id=trainer_object.email
                )
            #------------------------------------------------------------------#
            return results

        results['model_summary'] = add_slugs(results['model_summary'], object_slug=object_slug)
        trainer_object.data = json.dumps(results)
        trainer_object.analysis_done = True
        trainer_object.status = 'SUCCESS'
        trainer_object.save()

        if 'model_management_summary' in results:
            train_algo_details = results['model_management_summary']
            for algo_detail in train_algo_details:
                if len(algo_detail['listOfNodes']) > 1:
                    from api.utils import TrainAlgorithmMappingSerializer
                    temp_data = dict()
                    temp_data['name'] = get_random_model_id(algo_detail['name'])
                    temp_data['data'] = json.dumps(add_slugs(algo_detail, object_slug=object_slug))
                    temp_data['trainer'] = trainer_object.id
                    temp_data['app_id'] = trainer_object.app_id
                    temp_data['created_by'] = trainer_object.created_by.id
                    temp_config = {}
                    for i in results['model_dropdown']:
                        if algo_detail['name'] == i['name']:
                            temp_config['selectedModel'] = i
                    temp_config['variablesSelection'] = {}
                    temp_config['app_id'] = trainer_object.app_id
                    temp_data['config'] = json.dumps(temp_config)

                    serializer = TrainAlgorithmMappingSerializer(data=temp_data)
                    if serializer.is_valid():
                        train_algo_object = serializer.save()
                    else:
                        print(serializer.errors)
        if "one_click" in results:
            trainer_object.fe_config = json.dumps(results["one_click"])
            results["one_click"]={}
            trainer_object.data=json.dumps(results)
            trainer_object.save()

        outlook_autoML_success_mail(trainer_object.id)
        return "Done Succesfully."
    elif job_type == 'score':
        score_object = get_db_object(model_name=Score.__name__,
                                     model_slug=object_slug
                                     )

        if "error_message" in results:
            score_object.status = "FAILED"
            score_object.save()
            return results

        results = add_slugs(results, object_slug=object_slug)
        score_object.data = json.dumps(results)
        score_object.analysis_done = True
        score_object.status = 'SUCCESS'
        score_object.save()
        return "Done Succesfully."
    elif job_type == 'robo':
        robo_object = get_db_object(model_name=Robo.__name__,
                                    model_slug=object_slug
                                    )

        if "error_message" in results:
            robo_object.status = "FAILED"
            robo_object.save()
            return results

        results = add_slugs(results, object_slug=object_slug)
        robo_object.data = json.dumps(results)
        robo_object.robo_analysis_done = True
        robo_object.status = 'SUCCESS'
        robo_object.save()
        return results
    elif job_type == 'stockAdvisor':
        stock_objects = get_db_object(model_name=StockDataset.__name__,
                                      model_slug=object_slug
                                      )
        results['name'] = stock_objects.name
        results = add_slugs(results, object_slug=object_slug)
        stock_objects.data = json.dumps(results)
        stock_objects.analysis_done = True
        stock_objects.status = 'SUCCESS'
        stock_objects.save()
        return results
    else:
        print("No where to write")


def write_into_databases1(job_type, object_slug, results):
    from api import helper
    # import json
    from api.helper import get_db_object
    from api.views import chart_changes_in_metadata_chart, add_slugs

    if job_type in ["metadata", "subSetting"]:
        dataset_object = get_db_object(model_name=Dataset.__name__,
                                       model_slug=object_slug
                                       )

        if "error_message" in results:
            dataset_object.status = "FAILED"
            dataset_object.save()
            return results
        columnData = results['columnData']
        for data in columnData:
            # data["chartData"] = helper.find_chart_data_and_replace_with_chart_data(data["chartData"])
            card_data = data["chartData"]
            if 'dataType' in card_data and card_data['dataType'] == 'c3Chart':
                chart_data = card_data['data']
                final_chart_data = helper.decode_and_convert_chart_raw_data(chart_data, object_slug=object_slug)
                data["chartData"] = chart_changes_in_metadata_chart(final_chart_data)
                data["chartData"]["table_c3"] = []

        results['columnData'] = columnData
        # results['possibleAnalysis'] = settings.ANALYSIS_FOR_TARGET_VARIABLE
        da = []
        for d in results.get('sampleData'):
            da.append(list(map(str, d)))
        results['sampleData'] = da
        # results["modified"] = False

        dataset_object.meta_data = json.dumps(results)
        dataset_object.analysis_done = True
        dataset_object.status = 'SUCCESS'
        dataset_object.save()
        return results
    elif job_type == "master":
        insight_object = get_db_object(model_name=Insight.__name__,
                                       model_slug=object_slug
                                       )

        if "error_message" in results:
            insight_object.status = "FAILED"
            insight_object.save()
            return results

        results = add_slugs(results, object_slug=object_slug)
        insight_object.data = json.dumps(results)
        insight_object.analysis_done = True
        insight_object.status = 'SUCCESS'
        insight_object.save()
        return results
    elif job_type == "model":
        trainer_object = get_db_object(model_name=Trainer.__name__,
                                       model_slug=object_slug
                                       )

        if "error_message" in results or "model_summary" not in results:
            trainer_object.status = "FAILED"
            trainer_object.save()
            return results

        results['model_summary'] = add_slugs(results['model_summary'], object_slug=object_slug)
        trainer_object.data = json.dumps(results)
        trainer_object.analysis_done = True
        trainer_object.status = 'SUCCESS'
        trainer_object.save()

        if 'model_management_summary' in results:
            train_algo_details = results['model_management_summary']
            for algo_detail in train_algo_details:
                if len(algo_detail['listOfNodes']) > 1:
                    from api.utils import TrainAlgorithmMappingSerializer
                    temp_data = dict()
                    temp_data['name'] = algo_detail['name']
                    temp_data['data'] = json.dumps(add_slugs(algo_detail, object_slug=object_slug))
                    temp_data['trainer'] = trainer_object
                    temp_data['created_by'] = trainer_object.created_by.id
                    temp_config = {}
                    for i in results['model_dropdown']:
                        if algo_detail['name'] == i['name']:
                            temp_config['selectedModel'] = i
                    temp_config['variablesSelection'] = {}
                    temp_config['app_id'] = trainer_object.app_id
                    temp_data['config'] = json.dumps(temp_config)

                    serializer = TrainAlgorithmMappingSerializer(data=temp_data)
                    if serializer.is_valid():
                        train_algo_object = serializer.save()
                    else:
                        print(serializer.errors)
        return results
    elif job_type == 'score':
        score_object = get_db_object(model_name=Score.__name__,
                                     model_slug=object_slug
                                     )

        if "error_message" in results:
            score_object.status = "FAILED"
            score_object.save()
            return results

        results = add_slugs(results, object_slug=object_slug)
        score_object.data = json.dumps(results)
        score_object.analysis_done = True
        score_object.status = 'SUCCESS'
        score_object.save()
        return results
    elif job_type == 'robo':
        robo_object = get_db_object(model_name=Robo.__name__,
                                    model_slug=object_slug
                                    )

        if "error_message" in results:
            robo_object.status = "FAILED"
            robo_object.save()
            return results

        results = add_slugs(results, object_slug=object_slug)
        robo_object.data = json.dumps(results)
        robo_object.robo_analysis_done = True
        robo_object.status = 'SUCCESS'
        robo_object.save()
        return results
    elif job_type == 'stockAdvisor':
        stock_objects = get_db_object(model_name=StockDataset.__name__,
                                      model_slug=object_slug
                                      )
        results['name'] = stock_objects.name
        results = add_slugs(results, object_slug=object_slug)
        stock_objects.data = json.dumps(results)
        stock_objects.analysis_done = True
        stock_objects.status = 'SUCCESS'
        stock_objects.save()
        return results
    else:
        print("No where to write")


@task(name='save_results_to_job', queue=CONFIG_FILE_NAME)
def save_results_to_job(slug, results):
    from api.helper import get_db_object
    # import json

    job = get_db_object(model_name=Job.__name__,
                        model_slug=slug
                        )

    if isinstance(results, str):
        job.results = results
    elif isinstance(results, dict):
        results = json.dumps(results)
        job.results = results
    job.save()


@task(name='save_job_messages', queue=CONFIG_FILE_NAME)
def save_job_messages(slug, messages):
    from api.helper import get_db_object
    # import json
    try:
        job = get_db_object(model_name=Job.__name__,
                            model_slug=slug
                            )

        if isinstance(messages, str):
            job.messages = messages
        elif isinstance(messages, dict):
            results = json.dumps(messages)
            job.messages = messages
        job.save()
    except Exception as err:
        print(err)


@task(name='cleanup_logentry', queue=CONFIG_FILE_NAME)
def save_results_to_job1(slug, results):
    from api.helper import get_db_object
    # import json

    job = get_db_object(model_name=Job.__name__,
                        model_slug=slug
                        )

    if isinstance(results, str):
        job.results = results
    elif isinstance(results, dict):
        results = json.dumps(results)
        job.results = results
    job.save()
    print("save hogaya " * 100)


@task(name='cleanup_logentry')
def clean_up_logentry():
    from auditlog.models import LogEntry
    from django.contrib.auth.models import User

    all_users = User.objects.all()

    for user in all_users:
        log_entries = LogEntry.objects.filter(actor=user.id).count()
        LogEntry.objects.all().delete()
        print("delete object(s) :- %{0}".format(log_entries))


@task(name='cleanup_on_delete', queue=CONFIG_FILE_NAME)
def clean_up_on_delete(slug, model_name):
    from api.models import SaveAnyData, Job, SaveData

    job_instance = Job.objects.filter(object_id__contains=slug).first()
    if job_instance:
        job_instance.data = '{}'
        job_instance.save()

    sad_instance = SaveAnyData.objects.filter(slug__contains=slug)
    print(len(sad_instance))
    sad_instance.delete()

    sd_instance = SaveData.objects.filter(object_slug__contains=slug)
    print(len(sd_instance))
    sd_instance.delete()


@task(name='kill_job_using_application_id', queue=CONFIG_FILE_NAME)
def kill_application_using_fabric(app_id=None):
    if None == app_id:
        return -1
    from fabric.api import env, run
    from django.conf import settings
    import subprocess
    MODE = settings.MODE
    print(("MODE", MODE))
    if MODE == 'docker':
        # HDFS = settings.KILL_JOB
        # BASEDIR = settings.BASE_DIR
        # env.key_filename = settings.PEM_KEY
        # env.host_string = "{0}@{1}".format(HDFS["user.name"], HDFS["host"])

        try:
            capture = subprocess.Popen(
                "docker exec -t hadoop_spark_compose_hadoop_1 sh -c '/opt/hadoop/bin/yarn application --kill {0}'".format(
                    app_id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = capture.communicate()
            if 'finished' in stdout:
                return False
            else:
                return True
        except:
            return True
    else:
        HDFS = settings.HDFS
        BASEDIR = settings.BASE_DIR
        emr_file = BASEDIR + settings.PEM_KEY
        env.key_filename = [emr_file]

        if CONFIG_FILE_NAME == 'cwpoc':
            env.host_string = "{0}@{1}".format("ankush", HDFS["host"])
        else:
            env.host_string = "{0}@{1}".format(HDFS["user.name"], HDFS["host"])
        try:
            capture = run("yarn application --kill {0}".format(app_id))
            if 'finished' in capture:
                return False
            else:
                return True
        except:
            return True


@task(name='stock_sense_crawling', queue=CONFIG_FILE_NAME)
def stock_sense_crawl(object_slug):
    from api.helper import get_db_object
    print("stock_sense_crawl" * 2)
    stock_dataset_object = get_db_object(model_name=StockDataset.__name__,
                                         model_slug=object_slug
                                         )
    stock_dataset_object.generate_meta_data()
    stock_dataset_object.save()


@task(name='print_this_every_minute', queue=CONFIG_FILE_NAME)
def print_this_every_minute(data):
    print(data)


@task(name='call_dataset_then_score', queue=CONFIG_FILE_NAME)
def call_dataset_then_score(*args, **kwrgs):
    print(args)
    print(kwrgs)
    # collect all configs
    config = kwrgs
    dataset_details = config['dataset_details']
    # score_details = config['score_details']
    # trainer_details = config['trainer_details']
    modeldeployment_details = config['modeldeployment_details']
    user_details = config['user_details']

    # fetch modeldeployment instance
    from api.models import ModelDeployment
    model_deployment_object = ModelDeployment.objects.get(slug=modeldeployment_details['modeldeployment_slug'])

    # fetch user instance
    from django.contrib.auth.models import User
    user_object = User.objects.get_by_natural_key(username=user_details['username'])

    # fetch trainer model
    # trainer_object = model_deployment_object.deploytrainer.trainer
    dataset_score_deployment_details = {
        'name': model_deployment_object.name + ' - ' + str(datetime.datetime.now().time()),
        'deployment': model_deployment_object.id,
        'created_by': user_object.id,
        'config': '{}',
        'data': '{}'
    }
    from api.utils import DatasetScoreDeploymentSerializer
    dataset_score_deployment_serializer = DatasetScoreDeploymentSerializer(data=dataset_score_deployment_details)
    if dataset_score_deployment_serializer.is_valid():
        dataset_score_deployment_object = dataset_score_deployment_serializer.save()
        print(dataset_score_deployment_object)
    else:
        return
    # create dataset
    dataset_details['input_file'] = None
    if 'datasetname' in dataset_details['datasource_details']:
        dataset_details['name'] = dataset_details['datasource_details']['datasetname']
        dataset_details['created_by'] = user_object.id
    from api.datasets.helper import convert_to_string
    from api.datasets.serializers import DatasetSerializer

    dataset_details = convert_to_string(dataset_details)
    serializer = DatasetSerializer(data=dataset_details)
    if serializer.is_valid():
        dataset_object = serializer.save()
        dataset_score_deployment_object.dataset = dataset_object
        dataset_score_deployment_object.save()
        print(dataset_object)
        dataset_object.create()
    else:
        print(serializer.errors)


'''
Things to do
- call dataset object create function (uncomment in above code)
- Once dataset is completed from ML side they will
    -> call set_result API
    -> which will call write_into_database
    -> where we need to check if database is part of DatasetScore Table
    -> if yes, trigger score object create function
'''


def check_if_dataset_is_part_of_datascore_table_and_do_we_need_to_trigger_score(dataset_object_id):
    print(('received this dataset_object_id : ', dataset_object_id))

    if dataset_object_id is None:
        print("No dataset id given found")

        return

    from api.models import DatasetScoreDeployment

    try:
        dataset_object = Dataset.objects.get(id=dataset_object_id)
        datasetscore_deployment_object = DatasetScoreDeployment.objects.filter(dataset=dataset_object_id).first()

        if datasetscore_deployment_object is not None:
            # fetch modeldeployment instance
            print("Found the dataset in datasetscoredeployment table.")
            from api.models import ModelDeployment
            model_deployment_object = datasetscore_deployment_object.deployment
            print("Found deployment.")

            # fetch trainer insctance
            trainer_object = model_deployment_object.deploytrainer.trainer
            print("Found trainer_object.")

            # fetch user instance
            from django.contrib.auth.models import User
            user_object = dataset_object.created_by
            print("Found User")

            # create score
            # import json
            original_meta_data_from_scripts = json.loads(dataset_object.meta_data)
            print("Got metedata from dataset")

            if original_meta_data_from_scripts is None:
                uiMetaData = dict()
            if original_meta_data_from_scripts == {}:
                uiMetaData = dict()
            else:
                permissions_dict = {
                    'create_signal': user_object.has_perm('api.create_signal'),
                    'subsetting_dataset': user_object.has_perm('api.subsetting_dataset')
                }
                from api.datasets.helper import add_ui_metadata_to_metadata
                uiMetaData = add_ui_metadata_to_metadata(original_meta_data_from_scripts,
                                                         permissions_dict=permissions_dict)
                print("Got uiMetaData from dataset")

            from api.utils import convert_to_string
            # import json
            # config = json.loads(model_deployment_object.config)
            print("Got model_deployment_object config")

            # dataset_metadata = json.loads(dataset_object.meta_data)
            score_details = model_deployment_object.get_trainer_details_for_score(
                datasetscore_deployment_object.name + "_score")
            score_details['config']['variablesSelection'] = uiMetaData['varibaleSelectionArray']
            score_details['trainer'] = trainer_object.id
            score_details['dataset'] = dataset_object.id
            score_details['created_by'] = user_object.id
            score_details['app_id'] = int(score_details['config']['app_id'])
            score_details = convert_to_string(score_details)
            print("Constructed score_details")
            from api.utils import ScoreSerlializer
            score_serializer = ScoreSerlializer(data=score_details, context={})
            if score_serializer.is_valid():
                score_object = score_serializer.save()
                # we will not call score_object.create() here it will be called in write_into_databases
                datasetscore_deployment_object.score = score_object
                datasetscore_deployment_object.save()
                print(score_object)
                score_object.create()
            else:
                print(score_serializer.errors)
        else:
            print('datasetscore_deployment_object si None.')
            return
    except Exception as err:
        print(err)


def check_if_autoML_model_job_needs_to_be_triggered(dataset_object_id):
    print(('received this dataset_object_id : ', dataset_object_id))

    if dataset_object_id is None:
        print("No dataset id given found")

        return

    from api.models import Trainer
    try:
        dataset_object = Dataset.objects.get(id=dataset_object_id)
        trainer_object = Trainer.objects.filter(dataset=dataset_object_id).first()

        if trainer_object is not None:
            # fetch modeldeployment instance
            print("Found the dataset in trainer table.")
            ###########  Trigger autoML model job ##############
            create_model_autoML.delay(dataset_object.id)
        else:
            print('Its not a email autoML job.')
            return

    except Exception as err:
        outlook_autoML_failure_mail(trainer_object_id=None, error=err)
        print(err)


from celery.task.schedules import crontab
from celery.decorators import periodic_task


@periodic_task(run_every=(crontab(minute='*/10')), name="trigger_outlook_periodic_job", ignore_result=False,
               queue=CONFIG_FILE_NAME)
def trigger_outlook_periodic_job():

    mails = get_mails_from_outlook()
    if mails is not None:
        mail_id = ''
        if 'status' and 'err' not in list(mails.keys()):
            print("All set to proceed to upload dataset.")

            for configkey, configvalue in mails.items():
                data = {}
                for key, value in configvalue.items():
                    try:
                        print("inside try ... ")
                        # print key,value
                        # value is a dict
                        #############  Create config and trigger metadata job for train and test Dataset  #################
                        if key == 'sub_target':
                            data['sub_target'] = value
                        if key == 'target':
                            data['target'] = value
                        if 'train_dataset' in key:
                            input_file = value
                            data['Traindataset'] = input_file
                            data['name'] = input_file
                        if 'test_dataset' in key:
                            input_file = value
                            data['Testdataset'] = input_file
                            data['score_name'] = configkey
                        if 'emailAddress' in key:
                            data['email'] = value['emailAddress']['address']
                            mail_id = data['email']
                    except Exception as error:
                        outlook_autoML_failure_mail(trainer_object_id=None, error=error, mail_id=mail_id)
                        print('failure mail sent')
                        break
                if len(data) > 0:
                    print("Here is the collected data")
                    print(data)
                    trigger_metaData_autoML.delay(data)
                else:
                    print("No mails found")
                    break
                ##########################################################################################
        else:
            outlook_autoML_failure_mail(trainer_object_id=None, error=mails['err'], mail_id=mail_id)
            print('failure mail sent')
    else:
        print("No mails.")

    '''
    Task1: Look for auth Code, Access Token and Refresh Token : DONE
    Task2: Get mails from outlook
    Task3: Extract Text Data and attachments from mail
    Task4: Put Attachments in HDFS
    Task5: Prepare config for Data Upload.
    Task6: Trigger model Once Task5 is done.
    '''


@task(name='trigger_metaData_autoML', queue=CONFIG_FILE_NAME)
def trigger_metaData_autoML(data):
    print("metaData job triggered for autoML")
    ######################  User id for Email AutoML   ################
    print(data)
    '''
    Create one user with Username "email" in order to use email for AutoML model creation.

    '''
    from django.contrib.auth.models import User
    user_id = User.objects.get(username="email")
    ###################################################################
    ####################   Upload file from local  ####################
    from django.core.files import File
    from api.datasets.helper import convert_to_string
    from api.datasets.serializers import DatasetSerializer

    fail_log = dict()
    test_dataset_serializer = None
    train_dataset_serializer = None

    try:
        #########  Trainer dataset config   #########
        train_file = open(settings.BASE_DIR + '/media/datasets/' + data['Traindataset'])
        train_f = File(train_file)
        train_dataset_config = dict()
        train_dataset_config['name'] = data['name']
        train_dataset_config['input_file'] = train_f
        train_dataset_config['datasource_type'] = 'fileUpload'
        train_dataset_config['created_by'] = user_id.id
        train_dataset_details = convert_to_string(train_dataset_config)
        train_dataset_serializer = DatasetSerializer(data=train_dataset_details)
        ###################################################################
    except Exception as err:
        fail_log['train_config_error'] = str(err)
        pass
    try:
        #########  Test dataset config   #########
        if 'Testdataset' in data:
            test_file = open(settings.BASE_DIR + '/media/datasets/' + data['Testdataset'])
            test_f = File(test_file)
            test_dataset_config = dict()
            test_dataset_config['name'] = data['score_name'] + '_Test'
            test_dataset_config['input_file'] = test_f
            test_dataset_config['datasource_type'] = 'fileUpload'
            test_dataset_config['created_by'] = user_id.id
            test_dataset_details = convert_to_string(test_dataset_config)
            test_dataset_serializer = DatasetSerializer(data=test_dataset_details)
            ###################################################################
    except Exception as err:
        # fail_log['test_config_error'] = str(err)
        pass

    if train_dataset_serializer.is_valid():
        print("Saving train dataset Serializer")
        train_dataset_object = train_dataset_serializer.save()
        print(train_dataset_object)
        ################################   Create config for model object that to be triggered after metadata job  ##################
        try:
            model_config = dict()
            model_config['name'] = data['name'].split(".")[0] + '_Trainer'
            model_config['app_id'] = 2
            model_config['mode'] = "autoML"
            model_config['email'] = data['email']
            model_config['dataset'] = train_dataset_object.id
            model_config['config'] = dict()
            model_config['config']['targetColumn'] = data['target']
            model_config['config']['targetLevel'] = data['sub_target']
            model_config['created_by'] = user_id.id

            from api.utils import convert_to_string
            model_config = convert_to_string(model_config)
            print("Constructed model_config")
            print(model_config)

            from api.utils import TrainerSerlializer
            trainer_serializer = TrainerSerlializer(data=model_config, context={})
            if trainer_serializer.is_valid():
                print("Saving trainer Serializer")
                trainer_object = trainer_serializer.save()
                try:
                    if 'Testdataset' in data:
                        if test_dataset_serializer.is_valid():
                            print("Saving test dataset Serializer")
                            test_dataset_object = test_dataset_serializer.save()
                            print(test_dataset_object)
                            ################ Create config for Score object that to be triggered after model job   ##############
                            score_config = dict()
                            score_config['name'] = data['name'] + '_Score'
                            score_config['app_id'] = 2
                            score_config['trainer'] = trainer_object.id
                            score_config['dataset'] = test_dataset_object.id
                            score_config['created_by'] = user_id.id

                            from api.utils import ScoreSerlializer
                            score_serializer = ScoreSerlializer(data=score_config, context={})
                            if score_serializer.is_valid():
                                print("Saving score Serializer")
                                score_object = score_serializer.save()
                                print(score_object)
                                test_dataset_object.create()
                            else:
                                fail_log['score_serializer_error'] = str(score_serializer.errors)
                                # print(score_serializer.errors)
                    else:
                        print("There's no test data!")
                except Exception as err:
                    fail_log['score_generation_error'] = str(err)
                    pass
                    # outlook_autoML_failure_mail(trainer_object_id=None, error=err)
                    # print e
            else:
                fail_log['trainer_serializer_error'] = str(trainer_serializer.errors)
                # print(trainer_serializer.errors)
            ######### MODEL OBJECT SAVED  ---->  GO FOR METADATA CREATE ###########
            print("Going for metadata creation!!!")
            train_dataset_object.create()
        except Exception as err:
            fail_log['model_config_error'] = str(err)
            # outlook_autoML_failure_mail(trainer_object_id=None, error=err)
            pass
    else:
        fail_log['train_dataset_serializer_error'] = str(train_dataset_serializer.errors)
        print(train_dataset_serializer.errors)

    if fail_log:
        error = ''
        for i in fail_log:
            error = error + '\n' + i
        print('fail log >> ', fail_log)
        outlook_autoML_failure_mail(trainer_object_id=None, error=error, mail_id=data['email'])
        print('failure mail sent')


@task(name='create_model_autoML', queue=CONFIG_FILE_NAME)
def create_model_autoML(dataset_object_id=None, config=None):
    print('#####################  Configs for Trainer ##################')
    validationTechnique = {
        "displayName": "K Fold Validation",
        "name": "kFold",
        "value": 2,
    }
    if config is not None:
        try:
            print(config)
            data = json.loads(config)
            dataset_object = Dataset.objects.get(slug=data['slug'])
            print(dataset_object)

            model_config = {
                "name": data['model_name'],
                "app_id": 2,
                "mode": "autoML",
                "email": data['email'],
                "config": {}
            }

            original_meta_data_from_scripts = json.loads(dataset_object.meta_data)
            print("Got metedata from dataset")

            from django.contrib.auth.models import User
            user_object = dataset_object.created_by

            if original_meta_data_from_scripts is None:
                uiMetaData = dict()
            if original_meta_data_from_scripts == {}:
                uiMetaData = dict()
            else:
                permissions_dict = {
                    'create_signal': user_object.has_perm('api.create_signal'),
                    'subsetting_dataset': user_object.has_perm('api.subsetting_dataset')
                }
                from api.datasets.helper import add_ui_metadata_to_metadata
                uiMetaData = add_ui_metadata_to_metadata(original_meta_data_from_scripts,
                                                         permissions_dict=permissions_dict)
                print("Got uiMetaData from dataset")

            model_config['dataset'] = dataset_object.id
            model_config['config']['ALGORITHM_SETTING'] = copy.deepcopy(
                settings.AUTOML_ALGORITHM_LIST_CLASSIFICATION['ALGORITHM_SETTING'])
            model_config['config']['targetColumn'] = data['target']
            model_config['config']['targetLevel'] = data['subtarget']
            model_config['config']['variablesSelection'] = uiMetaData['varibaleSelectionArray']
            model_config['config']['validationTechnique'] = validationTechnique
            model_config['created_by'] = user_object.id

            from api.utils import convert_to_string
            model_config = convert_to_string(model_config)
            print("Constructed model_config")

            from api.utils import TrainerSerlializer
            trainer_serializer = TrainerSerlializer(data=model_config, context={})
            if trainer_serializer.is_valid():
                trainer_object = trainer_serializer.save()
                trainer_object.create()
            else:
                print(trainer_serializer.errors)

        except Exception as err:
            print(err)
    else:
        try:
            dataset_object = Dataset.objects.get(id=dataset_object_id)
            original_meta_data_from_scripts = json.loads(dataset_object.meta_data)
            print("Got metedata from dataset")

            from django.contrib.auth.models import User
            user_object = dataset_object.created_by

            if original_meta_data_from_scripts is None:
                uiMetaData = dict()
            if original_meta_data_from_scripts == {}:
                uiMetaData = dict()
            else:
                permissions_dict = {
                    'create_signal': user_object.has_perm('api.create_signal'),
                    'subsetting_dataset': user_object.has_perm('api.subsetting_dataset')
                }
                from api.datasets.helper import add_ui_metadata_to_metadata
                uiMetaData = add_ui_metadata_to_metadata(original_meta_data_from_scripts,
                                                         permissions_dict=permissions_dict)
                print("Got uiMetaData from dataset")
            try:
                trainer_obj = Trainer.objects.filter(dataset=dataset_object_id).first()
                model_config = {
                    "name": trainer_obj.name,
                    "app_id": 2,
                    "mode": "autoML",
                    "email": trainer_obj.email,
                    "config": {}
                }
                config = json.loads(trainer_obj.config)
                model_config['dataset'] = dataset_object.id
                model_config['config']['ALGORITHM_SETTING'] = copy.deepcopy(
                    settings.AUTOML_ALGORITHM_LIST_CLASSIFICATION['ALGORITHM_SETTING'])
                model_config['config']['validationTechnique'] = validationTechnique
                model_config['config']['targetLevel'] = config['targetLevel']
                model_config['config']['targetColumn'] = config['targetColumn']
                model_config['created_by'] = user_object.id
                model_config['config']['variablesSelection'] = uiMetaData['varibaleSelectionArray']
            except Exception as e:
                print(e)

            from api.utils import convert_to_string
            model_config = convert_to_string(model_config)
            print(("Constructed model_config", model_config))

            from api.utils import TrainerSerlializer
            trainer_serializer = TrainerSerlializer(data=model_config, context={})
            if trainer_serializer.is_valid():
                trainer_object = trainer_serializer.save()
                trainer_object.create()
            else:
                print(trainer_serializer.errors)

        except Exception as err:
            print(err)


@task(name='outlook_autoML_success_mail', queue=CONFIG_FILE_NAME)
def outlook_autoML_success_mail(trainer_object_id=None):
    if trainer_object_id is None:
        return
    else:
        trainer_object = Trainer.objects.get(id=trainer_object_id)
        if trainer_object.mode == 'autoML':

            from api.helper import get_outlook_auth
            r = get_outlook_auth(settings.OUTLOOK_AUTH_CODE, settings.OUTLOOK_REFRESH_TOKEN,
                                 settings.OUTLOOK_DETAILS)
            result = r.json()
            access_token = result['access_token']
            protocol = 'http'
            if settings.USE_HTTPS:
                protocol = 'https'

            Result_URL = '{}://{}/api/view_model_summary_autoML/?slug={}'.format(protocol,
                                                                                 settings.THIS_SERVER_DETAILS['host'],
                                                                                 trainer_object.slug)
            # content = "AutoML Dataupload successful. Model is created."
            content = Result_URL
            # app_slug = CustomApps.objects.get(app_id=trainer_object.app_id)
            # attachment_path = get_model_summary_pdf(app_slug.slug, trainer_object.slug)
            mail_data = dict()
            mail_data['modelName'] = trainer_object.name
            mail_data['datasetName'] = trainer_object.dataset.name
            mail_data['createdAt'] = trainer_object.created_at
            conf = json.loads(trainer_object.config)
            for i in conf['config']['COLUMN_SETTINGS']['variableSelection']:
                if i['targetColumn']:
                    mail_data['variable'] = i['name']
            try:
                if trainer_object.email is not None:
                    return_mail_id = trainer_object.email
                    # mail('send', access_token=access_token, return_mail_id=return_mail_id,
                    #     subject='Marlabs-AutoML Success', content=content, attachments=attachment_path)
                    mail('send', access_token=access_token, return_mail_id=return_mail_id,
                         subject='Marlabs-AutoML Success', content=content, mail_options=mail_data)
                else:
                    user_id = trainer_object.created_by_id
                    user_object = User.objects.get(id=user_id)
                    return_mail_id = user_object.email
                    if return_mail_id is not None:
                        # mail('send', access_token=access_token, return_mail_id=return_mail_id,
                        #     subject='Marlabs-AutoML Success', content=content, attachments=attachment_path)
                        mail('send', access_token=access_token, return_mail_id=return_mail_id,
                             subject='Marlabs-AutoML Success', content=content, mail_options=mail_data)

            except Exception as err:
                print(err)
                pass
        else:
            pass


@task(name='outlook_autoML_failure_mail', queue=CONFIG_FILE_NAME)
def outlook_autoML_failure_mail(trainer_object_id=None, error=None, mail_id=None):
    print("Trying to send failure mail")
    mail_data = dict()
    from api.helper import get_outlook_auth
    r = get_outlook_auth(settings.OUTLOOK_AUTH_CODE, settings.OUTLOOK_REFRESH_TOKEN,
                         settings.OUTLOOK_DETAILS)
    result = r.json()
    print(result)
    access_token = result['access_token']
    print("got access token")
    if trainer_object_id is None:
        mail_data['modelName'] = 'UNDEFINED'
        mail_data['datasetName'] = 'UNDEFINED'
        mail_data['createdAt'] = 'UNDEFINED'
        mail_data['variable'] = 'UNDEFINED'
        print("mail id : ", mail_id)
        err_mail('send', access_token=access_token, return_mail_id=mail_id,
                 subject='Marlabs-AutoML Failure', error=error, mail_options=mail_data)
    else:
        trainer_object = Trainer.objects.get(id=trainer_object_id)
        if trainer_object.mode == 'autoML':

            mail_data['modelName'] = trainer_object.name
            mail_data['datasetName'] = trainer_object.dataset.name
            mail_data['createdAt'] = trainer_object.created_at
            conf = json.loads(trainer_object.config)
            for i in conf['config']['COLUMN_SETTINGS']['variableSelection']:
                if i['targetColumn']:
                    mail_data['variable'] = i['name']
            try:
                if trainer_object.email is not None:
                    return_mail_id = trainer_object.email
                    err_mail('send', access_token=access_token, return_mail_id=return_mail_id,
                             subject='Marlabs-AutoML Failure', error=error, mail_options=mail_data)
                else:
                    user_id = trainer_object.created_by_id
                    user_object = User.objects.get(id=user_id)
                    return_mail_id = user_object.email
                    if return_mail_id is not None:
                        err_mail('send', access_token=access_token, return_mail_id=return_mail_id,
                                 subject='Marlabs-AutoML Failure', error=error, mail_options=mail_data)

            except Exception as err:
                print(err)
                pass
        else:
            pass


def mail(action_type=None, access_token=None, return_mail_id=None, subject=None, content=None, mail_options=None):
    # access_token = access_token
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        try:
            messages = send_my_messages(access_token, return_mail_id, subject, content, mail_options)
            if messages[:3] == '202':
                print("Mail Sent")
        except Exception as e:
            print(e)
            print("Some issue with mail sending module...")


def err_mail(action_type=None, access_token=None, return_mail_id=None, subject=None, error=None, mail_options=None):
    # access_token = access_token
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        try:
            messages = send_failure_messages(access_token, return_mail_id, subject, error, mail_options)
            if messages[:3] == '202':
                print("Mail Sent")
        except Exception as e:
            print(e)
            print("Some issue with mail sending module...")


def send_failure_messages(access_token, return_mail_id, subject, error, mail_options):
    get_messages_url = 'https://graph.microsoft.com/v1.0/me/' + '/sendmail'

    htmlData = """<!DOCTYPE html><html><body>Dear {},</br></br>Model creation has failed for some reason! \
    </br></br>Please contact the Admin team for further assistance.</br></br> \
    Sorry for the inconvenience.</br></br>Regards,</br>mAdvisor</body></html>""" \
        .format(return_mail_id.split('@')[0])
    '''
    htmlData = """<!DOCTYPE html><html><body>Dear {},</br></br>Model creation has failed! \
    </br></br>Details:</br>Model Name : {}</br>Created on : {}</br>Dataset : {}</br>Target Variable : {}</br>Reason for failure : {} \
    </br></br></br></br>Sorry for the inconvenience.</br></br>Regards,</br>mAdvisor</body></html>""" \
        .format(return_mail_id.split('@')[0],
                mail_options['modelName'],
                mail_options['createdAt'],
                mail_options['datasetName'],
                mail_options['variable'],
                str(error))'''

    payload = {

        "Message": {

            "Subject": subject,
            "Body": {

                "ContentType": "HTML",
                "Content": htmlData,

            },
            "ToRecipients": [
                {
                    "EmailAddress": {
                        "Address": return_mail_id
                    }
                }
            ],
            # 'Attachments': [attached_files]
        },
        "SaveToSentItems": "true",

    }
    from api.helper import make_api_call
    import requests

    r = make_api_call('POST', get_messages_url, access_token, payload=payload)
    if r.status_code == requests.codes.ok:
        print("Mail Sent")
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def send_my_messages(access_token, return_mail_id, subject, content, mail_options):
    '''
  Replies to the mail with attachments
  '''
    # get_messages_url = graph_endpoint.format('/me/messages?$select=sender,subject')
    # get_messages_url = 'https://graph.microsoft.com/v1.0' + '/users/' + settings.OUTLOOK_ID + '/sendmail'
    get_messages_url = 'https://graph.microsoft.com/v1.0/me/' + '/sendmail'
    # Use OData query parameters to control the results
    #  - Only first 10 results returned
    #  - Only return the ReceivedDateTime, Subject, and From fields
    #  - Sort the results by the ReceivedDateTime field in descending order
    '''
    b64_content = base64.b64encode(open(file_to_attach, 'rb').read())
    mime_type = mimetypes.guess_type(file_to_attach)[0]
    mime_type = mime_type if mime_type else ''
    attached_files = {'@odata.type': '#microsoft.graph.fileAttachment',
                      'ContentBytes': b64_content.decode('utf-8'),
                      'ContentType': mime_type,
                      'Name': file_to_attach.split('/')[-1]}
    '''
    htmlData = """<!DOCTYPE html><html><body>Dear {},</br></br>Model has been successfully created through AutoML.
    </br></br>Details:</br>Model Name : {}</br>Created on : {}</br>Dataset : {}</br>Target Variable :
    {}</br></br>Please go through the attached link in order to view your Model Summary.
    </br></br></br><a href="{}">Model Summary</a></br></br>Have a great day ahead.</br></br>Regards,</br>mAdvisor</body></html>""" \
        .format(return_mail_id.split('@')[0],
                mail_options['modelName'],
                mail_options['createdAt'],
                mail_options['datasetName'],
                mail_options['variable'],
                content)

    payload = {

        "Message": {

            "Subject": subject,
            "Body": {

                "ContentType": "HTML",
                "Content": htmlData,

            },
            "ToRecipients": [
                {
                    "EmailAddress": {
                        "Address": return_mail_id
                    }
                }
            ],
            # 'Attachments': [attached_files]
        },
        "SaveToSentItems": "true",

    }
    from api.helper import make_api_call
    import requests

    r = make_api_call('POST', get_messages_url, access_token, payload=payload)
    if r.status_code == requests.codes.ok:
        print("Mail Sent")
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)


'''
def send_devtools(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


def save_as_pdf(driver, path, options=None):
    if options is None:
        options = {}
    result = send_devtools(driver, "Page.printToPDF", options)
    with open(path, 'wb') as f:
        f.write(base64.b64decode(result['data']))


def get_model_summary_pdf(app_slug, model_slug):
    protocol = 'http'
    if settings.USE_HTTPS:
        protocol = 'https'

    login_url = '{}://{}'.format(protocol, settings.THIS_SERVER_DETAILS['host'])
    url = '{}/apps/{}/autoML/models/{}'.format(login_url, app_slug, model_slug)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(login_url)
    driver.find_element_by_id('username').send_keys('email')
    driver.find_element_by_id('password').send_keys('emailuser')
    driver.find_element_by_xpath('//button').click()
    driver.get(url)
    path = '{}/{}.pdf'.format(settings.MODEL_SUMMARY_DOWNLOAD_PATH, model_slug)
    save_as_pdf(driver, path, {'landscape': False})
    return path
'''


@periodic_task(run_every=(crontab(0, 0, day_of_month='1')), name="trigger_outlook_token", ignore_result=False,
               queue=CONFIG_FILE_NAME)
def trigger_outlook_token():

    outlook_data = settings.OUTLOOK_DETAILS
    token = OutlookToken.objects.first()

    post_data_auth_code = {
        'grant_type': 'authorization_code',
        'code': token.access_token,
        'redirect_uri': outlook_data['redirect_uri'],
        'scope': settings.OUTLOOK_SCOPES,
        'client_id': outlook_data['client_id'],
        'client_secret': outlook_data['client_secret']
    }
    post_data_refresh_token = {'grant_type': 'refresh_token',
                               'redirect_uri': outlook_data['redirect_uri'],
                               'scope': 'https://graph.microsoft.com/.default',
                               'refresh_token': token.refresh_token,
                               'client_id': outlook_data['client_id'],
                               'client_secret': outlook_data['client_secret']
                               }

    if token.refresh_token is not None:
        r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_refresh_token)
        result = r.json()
        outlook_token = OutlookToken(refresh_token=result['refresh_token'], access_token=result['access_token'])
        outlook_token.save()
    else:
        r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_auth_code)
        result = r.json()
        outlook_token = OutlookToken(refresh_token=result['refresh_token'], access_token=result['access_token'])
        outlook_token.save()
    return result



