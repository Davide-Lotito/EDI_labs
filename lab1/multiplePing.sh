##A bash script to run, in one time, all the ping commands
# !/bin/bash

# targets=("google.com" "facebook.com" "github.com" "linkedin.com")
targets=("34.71.44.40" "35.236.81.238" "34.74.209.9" "34.151.215.105" "34.129.235.109" "34.85.87.24" "34.131.76.108" "34.101.215.255" "34.88.168.220" "34.65.88.164")   

rm ./resultsPing/*

for i in ${!targets[@]}; do
    s="test$i.txt"
    #s="ping[${targets[$i]}].txt"
    echo "ping to ${targets[$i]} -> results in the file $s"
    ping -c 10 -D ${targets[$i]} > ./resultsPing/$s &
done

wait $! # wait until the last process created has finished
echo "----"
cd ./resultsPing
echo "Files created are listed here below: "
ls