echo "Running the dist"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

echo "HOST: $1"
echo "INPUT CUSTOMER FILE FILE: $2"
echo "INPUT HISTORICAL FILE FILE: $3"
echo "INPUT MARKET FILE FILE: $4"
echo "OUTPUT DIRECTORY: $5"
INPUT_FILE_1=$2
INPUT_FILE_2=$3
INPUT_FILE_3=$4
COMMAND_PREFIX="ssh -i api/lib/TIAA.pem hadoop@$1 spark-submit --master yarn --deploy-mode client"
#COMMAND_PREFIX="spark-submit --master yarn --deploy-mode client"
SCRIPTS_ROOT="/home/hadoop/codebase/mAdvisor-MLScripts/bi/scripts"

echo "Fixing permission on pem file"
chmod 0400 api/lib/TIAA.pem

echo "Running portfolio_analysis.py"
$COMMAND_PREFIX $SCRIPTS_ROOT/portfolio_analysis.py --input1 "hdfs://$1/$INPUT_FILE_1" --input2 "hdfs://$1/$INPUT_FILE_2" --input3 "hdfs://$1/$INPUT_FILE_3" --result "hdfs://$1:8020$5/portfolio-result.json" --narratives "hdfs://$1:8020$5/portfolio-narratives.json"