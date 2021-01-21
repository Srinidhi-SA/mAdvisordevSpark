echo "Running the dist"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

echo "HOST: $1"
echo "INPUT CONFIGURATION FILE: $2"
INPUT_FILE_1=$2
COMMAND_PREFIX="ssh -i api/lib/TIAA.pem hadoop@$1 spark-submit --master yarn --deploy-mode client"
#COMMAND_PREFIX="spark-submit --master yarn --deploy-mode client"
SCRIPTS_ROOT="/home/hadoop/codebase/mAdvisor-MLScripts/bi"

echo "Fixing permission on pem file"
#chmod 0400 api/lib/emr.pem
chmod 0400 api/lib/TIAA.pem

echo "Running master.py"
COMMAND="$COMMAND_PREFIX $SCRIPTS_ROOT/master.py $INPUT_FILE_1"
echo $COMMAND
$COMMAND_PREFIX $SCRIPTS_ROOT/master.py $INPUT_FILE_1