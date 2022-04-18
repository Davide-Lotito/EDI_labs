##A bash script to automate and run multiple time
# !/bin/bash

# fatto 30 volte, ogni 6 minuti --> 3 ora di lavoro

for i in {1..30}; do 
    echo -n "This is an execution in loop $i "
    date
    ./main.sh 
    sleep 360
done