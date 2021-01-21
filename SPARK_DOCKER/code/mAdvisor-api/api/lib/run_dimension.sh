echo "Running the dist"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

echo "HOST: $1"
echo "INPUT FILE: $2"
echo "OUTPUT DIRECTORY: $3"
DIMENSION=$4
COMMAND_PREFIX="ssh -i api/lib/TIAA.pem hadoop@$1 spark-submit --master yarn --deploy-mode client"
SCRIPTS_ROOT="/home/hadoop/codebase/marlabs-bi/bi/scripts"
echo "DIMENSION: $DIMENSION"

echo "Fixing permission on pem file"
chmod 0400 api/lib/TIAA.pem

echo "Running frequency_dimensions.py"
$COMMAND_PREFIX $SCRIPTS_ROOT/frequency_dimensions.py --input "hdfs://$1/$2" --result "hdfs://$1:8020$3/frequency-result.json" --narratives "hdfs://$1:8020$3/frequency-narratives.json" --dimensioncolumn $DIMENSION

echo "Running chisquare.py"
$COMMAND_PREFIX $SCRIPTS_ROOT/chisquare.py --input "hdfs://$1/$2" --result "hdfs://$1:8020$3/chi-result.json" --narratives "hdfs://$1:8020$3/chi-narratives.json" --dimensioncolumn $DIMENSION --ignorecolumn 'fund_name'

echo "Running decision_tree.py"
$COMMAND_PREFIX $SCRIPTS_ROOT/decision_tree.py --input "hdfs://$1/$2" --result "hdfs://$1:8020$3/tree-result.json" --narratives "hdfs://$1:8020$3/tree-narratives.json" --dimensioncolumn $DIMENSION --ignorecolumn 'fund_name'


#echo "Running the dist"
#
#export LC_ALL=en_US.UTF-8
#export LANG=en_US.UTF-8
#
#echo "HOST: $1"
#echo "INPUT FILE: $2"
#echo "OUTPUT DIRECTORY: $3"
#DIMENSION=$4
#COMMAND_PREFIX="spark-submit --master yarn --deploy-mode client"
#SCRIPTS_ROOT="/home/ankush/codebase/marlabs-bi/bi/scripts"
#echo "DIMENSION: $DIMENSION"
#
#echo "Running frequency_dimensions.py"
#$COMMAND_PREFIX $SCRIPTS_ROOT/frequency_dimensions.py --input "hdfs://$1/$2" --result "hdfs://$1:9000$3/frequency-result.json" --narratives "hdfs://$1:9000$3/frequency-narratives.json" --dimensioncolumn $DIMENSION
#
#echo "Running chisquare.py"
#$COMMAND_PREFIX $SCRIPTS_ROOT/chisquare.py --input "hdfs://$1/$2" --result "hdfs://$1:9000$3/chi-result.json" --narratives "hdfs://$1:9000$3/chi-narratives.json" --dimensioncolumn $DIMENSION --ignorecolumn 'fund_name'
#
#echo "Running decision_tree.py"
#$COMMAND_PREFIX $SCRIPTS_ROOT/decision_tree.py --input "hdfs://$1/$2" --result "hdfs://$1:9000$3/tree-result.json" --narratives "hdfs://$1:9000$3/tree-narratives.json" --dimensioncolumn $DIMENSION --ignorecolumn 'fund_name'
