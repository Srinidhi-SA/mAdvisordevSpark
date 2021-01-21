echo "Running the dist"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

echo "HOST: $1"
echo "INPUT FILE: $2"
echo "OUTPUT DIRECTORY: $3"
MEASURE=$4
COMMAND_PREFIX="ssh -i api/lib/TIAA.pem hadoop@$1 spark-submit --master yarn --deploy-mode client"
SCRIPTS_ROOT="/home/hadoop/codebase/mAdvisor-MLScripts/bi/scripts"
echo "MEASURE: $MEASURE"

echo "Fixing permission on pem file"
chmod 0400 api/lib/TIAA.pem

# SAMPLE SCRIPT
# ssh -i api/lib/mAdviser_key_pair.pem hadoop@ec2-54-88-153-37.compute-1.amazonaws.com spark-submit --master yarn  --deploy-mode client /home/hadoop/codebase/marlabs-bi/bi/scripts/descr_stats.py "hdfs://ip-172-31-3-88.ec2.internal:9000/user/input/Iris.csv" "hdfs://ip-172-31-3-88.ec2.internal:9000/user/output/output_prakash.json" --driver-memory 1g --executor-memory 1g --executor-cores 2


# DO NOT FORGET TO UNCOMMENT THIS!!!!
echo "Running for descr_stats"
$COMMAND_PREFIX $SCRIPTS_ROOT/descr_stats.py --input "hdfs://$1:9000/$2" --result "hdfs://$1:9000$3/result.json" --narratives "hdfs://$1:9000$3/narratives.json" --measurecolumn $MEASURE

echo "Running for one_way_anova.py"
$COMMAND_PREFIX $SCRIPTS_ROOT/one_way_anova.py --input "hdfs://$1:9000/$2" --result "hdfs://$1:9000$3/dimensions-result.json" --narratives "hdfs://$1:9000$3/dimensions-narratives.json" --measurecolumn $MEASURE

echo "Running regression.py"
$COMMAND_PREFIX $SCRIPTS_ROOT/regression.py --input "hdfs://$1/$2" --result "hdfs://$1:9000$3/reg-result.json" --narratives "hdfs://$1:9000$3/reg-narratives.json" --measurecolumn $MEASURE



## DO NOT FORGET TO UNCOMMENT THIS!!!!
#echo "Running for descr_stats"
#spark-submit --master yarn  --deploy-mode client /home/ankush/codebase/marlabs-bi/bi/scripts/descr_stats.py --input "hdfs://$1:9000/$2" --result "hdfs://$1:9000$3/result.json" --narratives "hdfs://$1:9000$3/narratives.json" --measurecolumn $MEASURE
#
#echo "Running for one_way_anova.py"
#spark-submit --master yarn  --deploy-mode client /home/ankush/codebase/marlabs-bi/bi/scripts/one_way_anova.py --input "hdfs://$1:9000/$2" --result "hdfs://$1:9000$3/dimensions-result.json" --narratives "hdfs://$1:9000$3/dimensions-narratives.json" --measurecolumn $MEASURE
#
#echo "Running regression.py"
#$COMMAND_PREFIX $SCRIPTS_ROOT/regression.py --input "hdfs://$1/$2" --result "hdfs://$1:9000$3/reg-result.json" --narratives "hdfs://$1:9000$3/reg-narratives.json" --measurecolumn $MEASURE
