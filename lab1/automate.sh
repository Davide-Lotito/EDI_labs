##A bash script to automate and run multiple time
# !/bin/bash

for i in {1..6}; do 
    echo -n "This is a test in loop $i "
    date
    ./main.sh 
    sleep 600
done