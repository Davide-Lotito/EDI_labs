from datetime import datetime
import json ##to work with json
import os ##to use bash command
import re ##to work with regex

# get only three useful lines 
def getLines(Lines):
    regTimeStamp = "\[+[0-9]+\.+[0-9]+\]"
    for line in Lines:
        z = re.search(regTimeStamp,line)
        if "PING" in line.strip():
            head = line.strip()
            continue
        if z:
            timeStamp = z[0]
            continue
        if "packets" in line.strip():
            packets = line.strip()
        if "rtt min/avg/max/mdev" in line.strip():
            rtt = line.strip()
    return head, packets, rtt, timeStamp

# open each file and work on it
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

# os.system("rm sample.txt")

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
    head, packets, rtt, timeStamp = getLines(Lines)

    timeStamp = timeStamp.replace("[","").replace("]","")
    index = timeStamp.find(".")
    ts = ""
    for z in range(0, index):
        ts += timeStamp[z]
    timeStamp = int(ts)
    timeInfo = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
    date = timeInfo.split(" ")[0]
    time = timeInfo.split(" ")[1]
        
    destination, packetLost, excTime, minRTT, avgRTT, maxRTT, devRTT = getData(head, packets, rtt)
    print("--- new file: " + f"test{str(i)}.txt" +" ---")
    # print("The target IP is:", destination)
    # print("The time value is:", time)
    # print("Min RTT:", minRTT)
    # print("Avg RTT:", avgRTT)
    # print("Max RTT:", maxRTT)
    # print("Dev RTT:", devRTT)
    # print("Timestamp:", timeStamp)
    # print(datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S'))
    # print("Date:", date)
    # print("Time:", time)

    results_list.append(writeJson(destination, packetLost, excTime, date, time, minRTT, avgRTT, maxRTT, devRTT))
    
with open(f"./results/results{timeStamp}.txt", "w+") as f:
    f.write(json.dumps(results_list))

print("---")

f = open(f"./results/results{timeStamp}.txt")
d = json.load(f)
print(json.dumps(d, indent=4))#prettyprint a json file