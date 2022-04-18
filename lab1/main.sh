# To run everything in one shot
# !/bin/bash

./multiplePing.sh
wait $! # wait until the last process created has finished
echo "---"
sleep 10
python3 analyze.py
echo "python script joined all files"
cd ./results
echo "Files created are listed here below: "
ls
cd ..