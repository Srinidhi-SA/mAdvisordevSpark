echo "Running the meta"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

echo "HDFS HOST: $1"
echo "INPUT FILE: $2"
echo "OUTPUT FILE: $3"

echo "Fixing permission on pem file"
chmod 0400 api/lib/TIAA.pem

# DO NOT FORGET TO UNCOMMENT THIS!!!!
echo "Running the save config"
scp -i api/lib/TIAA.pem "$2" hadoop@$1:~/configs/$3
