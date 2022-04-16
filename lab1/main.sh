# To run everything in one shot
# !/bin/bash

./multiplePing.sh
wait $! # wait until the last process created has finished
python3 analyze.py