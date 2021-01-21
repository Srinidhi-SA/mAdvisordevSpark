echo "Running the meta"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

echo "HDFS HOST: $1"
echo "INPUT FILE: $2"
echo "OUTPUT FILE: $3"
echo "COLUMN_SETTINGS: $4"
echo "DIMENSION_FILTER: $5"
echo "MEASURE_FILTER: $6"
echo "MEASURE_SUGGESTIONS: $7"

COMMAND_PREFIX="ssh -i api/lib/TIAA.pem hadoop@$1 spark-submit --master yarn --deploy-mode client"
#SCRIPTS_ROOT="/home/hadoop/codebase/marlabs-bi/bi/scripts"
SCRIPTS_ROOT="/home/hadoop/codebase/mAdvisor-MLScripts/bi/scripts"


echo "Fixing permission on pem file"
chmod 0400 api/lib/emr.pem

# DO NOT FORGET TO UNCOMMENT THIS!!!!
echo "Running the filter"
#spark-submit --master yarn  --deploy-mode client /home/ankush/codebase/marlabs-bi/bi/scripts/metadata.py
#        --input "hdfs://$1:8020$2" --result "hdfs://$1:8020$3"

echo $COMMAND_PREFIX /home/hadoop/codebase/mAdvisor-MLScripts/bi/filter_cl.py \
        --input "hdfs://$1:8020$2" \
        --result "hdfs://$1:8020$3" \
        --consider_columns $4 \
        --dimension_filter $5 \
        --measure_filter $6 \
        --measure_suggestions $7


$COMMAND_PREFIX  /home/hadoop/codebase/mAdvisor-MLScripts/bi/filter_cl.py \
        --input "hdfs://$1:8020$2" \
        --result "hdfs://$1:8020$3" \
        --consider_columns "'""$4""'" \
        --dimension_filter "'""$5""'" \
        --measure_filter "'""$6""'" \
        --measure_suggestions "'""$7""'"
