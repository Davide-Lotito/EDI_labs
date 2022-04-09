import json ##to work with json
import os ##to use bash command
import re ##to work with regex

# get only three useful lines 
def getLines(Lines):
    count = 0
    for line in Lines:
        count += 1
        if "PING" in line.strip():
            head = line.strip()
        if "packets" in line.strip():
            packets = line.strip()
        if "rtt min/avg/max/mdev" in line.strip():
            rtt = line.strip()
    return head, packets, rtt

# open each file and work on it
def getData(head, packets, rtt):
    # useful regex
    regIP = "[0-9]+\.+[0-9]+\.+[0-9]+\.+[0-9]"
    regPacketLost = "[0-9]+\%"
    regTime = "\s+[0-9]+ms"
    regRTT = "[0-9]+\.+[0-9]+"

    # search useful data
    destination = re.search(regIP, head)[0] #IP address
    packetLost = re.search(regPacketLost, packets)[0]
    time = re.search(regTime, packets)[0] #time value from ping command
    minRTT = re.findall(regRTT, rtt)[0]
    avgRTT = re.findall(regRTT, rtt)[1]
    maxRTT = re.findall(regRTT, rtt)[2]
    devRTT = re.findall(regRTT, rtt)[3]
    return destination, packetLost, time, minRTT, avgRTT, maxRTT, devRTT

def writeJson(destination, packetLost, time, minRTT, avgRTT, maxRTT, devRTT):
    return {
        "destination" : destination,
        "timestamp" : "timestamp",
        "packetLost" : packetLost,
        "time" : time,
        "RTT" : 
            {
                "minRTT" : minRTT,
                "avgRTT" : avgRTT,
                "maxRTT" : maxRTT,
                "devRTT" : devRTT
            }
    }

os.system("rm sample.txt")

# folder path
dir_path = './resultsPing/'

dirCount = 0
# iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        dirCount += 1

results_list = []

for i in range(0, dirCount):
    filePath = f"{dir_path}test{str(i)}.txt"
    file = open(filePath, 'r')
    Lines = file.readlines()
    head, packets, rtt = getLines(Lines)

    destination, packetLost, time, minRTT, avgRTT, maxRTT, devRTT = getData(head, packets, rtt)
    #print("--- new file: " + f"test{str(i)}.txt" +" ---")
    # print("The target IP is:", destination)
    # print("The time value is:", time)
    # print("Min RTT:", minRTT)
    # print("Avg RTT:", avgRTT)
    # print("Max RTT:", maxRTT)
    # print("Dev RTT:", devRTT)

    results_list.append(writeJson(destination, packetLost, time, minRTT, avgRTT, maxRTT, devRTT))
    
with open("sample.txt", "w+") as f:
    f.write(json.dumps(results_list))

f = open("sample.txt")
d = json.load(f)
print(json.dumps(d, indent=4))#prettyprint a json file