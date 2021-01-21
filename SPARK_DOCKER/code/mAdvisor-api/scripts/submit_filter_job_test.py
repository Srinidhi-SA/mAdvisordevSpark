import json
from sjsclient import client


host = "localhost"

host_with_hdfs = "hdfs://"+ host
sjs = client.Client("http://" + host + ":" + "8090")
test_app = sjs.apps.get("test_api_1")
test_ctx = sjs.contexts.get("pysql-context")
class_path = "bi.sparkjobs.filter_job"

config = {'result_path': 'hdfs://localhost:9000/datasets/65/output/meta.json_Ecommerce_data0.csv_1',
          'input_path': 'hdfs://localhost:9000/datasets/65/input/Ecommerce_data0.csv',
          'measure_suggestions': [], 'dimension_filter': {u'Buyer_Age': [u'45 to 54', u'18 to 24']},
          'measure_filter': {}, 'consider_columns': ['Buyer_Age']}

job = sjs.jobs.create(test_app, class_path, ctx=test_ctx, conf=json.dumps(config))

job_url = "http://{0}:8090/jobs/{1}".format(host, job.jobId)
