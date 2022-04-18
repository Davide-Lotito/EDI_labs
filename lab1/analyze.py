from datetime import datetime
import json # json
import os # bash command
import re # regex

"""
get only three useful lines 
"""
def getLines(Lines):
    regTimeStamp = "\[+[0-9]+\.+[0-9]+\]"
    for line in Lines:
        z = re.search(regTimeStamp,line)
        if "PING" in line.strip():
            head = line.strip()
        if z:
            timeStamp = z[0]
        if "packets" in line.strip():
            packets = line.strip()
        if "rtt min/avg/max/mdev" in line.strip():
            rtt = line.strip()
    return head, packets, rtt, timeStamp

"""
open each file and work on it
"""
def getData(head, packets, rtt):
    # useful regex
    regIP = "[0-9]+\.+[0-9]+\.+[0-9]+\.+[0-9]+"
    regPacketLost = "[0-9]+\%"
    regExcTime = "\s+[0-9]+ms"
    regRTT = "[0-9]+\.+[0-9]+"

    # search useful data
    destination = re.search(regIP, head)[0] #IP address
    packetLost = re.search(regPacketLost, packets)[0]
    excTime = re.search(regExcTime, packets)[0] #time value from ping command
    minRTT = re.findall(regRTT, rtt)[0]
    avgRTT = re.findall(regRTT, rtt)[1]
    maxRTT = re.findall(regRTT, rtt)[2]
    devRTT = re.findall(regRTT, rtt)[3]
    return destination, packetLost, excTime, minRTT, avgRTT, maxRTT, devRTT

"""
write the json file
"""
def writeJson(destination, packetLost, excTime, date, time, minRTT, avgRTT, maxRTT, devRTT):
    return {
        "destination" : destination,
        "date" : date,
        "time" : time,
        "packetLost" : packetLost,
        "excutionTime" : excTime,
        "minRTT" : minRTT,
        "avgRTT" : avgRTT,
        "maxRTT" : maxRTT,
        "devRTT" : devRTT,
    }

"""
get the time and date
"""
def getTime(timeStamp):
    timeInfo = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
    date = timeInfo.split(" ")[0]
    time = timeInfo.split(" ")[1]
    timeWrapper = list(time)
    timeWrapper[1] = str(int(timeWrapper[1]) + 2)
    time = "".join(timeWrapper)
    return date,time

# folder path
dirPath = './resultsPing/'

dirCount = 0
# iterate directory
for path in os.listdir(dirPath):
    # check if current path is a file
    if os.path.isfile(os.path.join(dirPath, path)):
        dirCount += 1

results_list = []

for i in range(0, dirCount):
    filePath = f"{dirPath}test{str(i)}.txt"
    file = open(filePath, 'r')
    Lines = file.readlines()
    head, packetsN, rtt, timeStamp = getLines(Lines)

    timeStamp = timeStamp.replace("[","").replace("]","")
    index = timeStamp.find(".")
    ts = ""
    for z in range(0, index):
        ts += timeStamp[z]
    timeStamp = int(ts)
    date, time = getTime(timeStamp)

    destination, packetLost, excTime, minRTT, avgRTT, maxRTT, devRTT = getData(head, packetsN, rtt)
    results_list.append(writeJson(destination, packetLost, excTime, date, time, minRTT, avgRTT, maxRTT, devRTT))
    
with open(f"./results/results{timeStamp}.txt", "w+") as f:
    f.write(json.dumps(results_list))

##test
#f = open(f"./results/results{timeStamp}.txt")
#d = json.load(f)
#print(json.dumps(d, indent=4))#prettyprint a json file