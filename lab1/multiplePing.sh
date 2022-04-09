##A bash script to run, in one time, all the ping commands
# !/bin/bash

targets=("google.com" "facebook.com" "github.com" "linkedin.com")

rm ./resultsPing/*

for i in ${!targets[@]}; do
    s="test$i.txt"
    #s="ping[${targets[$i]}].txt"
    echo "ping to ${targets[$i]} -> results in the file $s"
    ping -c 10 ${targets[$i]} > ./resultsPing/$s &
done

wait $! # wait until the last process created has finished
echo "----"
cd ./resultsPing
echo "Files created are listed here below: "
ls