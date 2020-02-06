"""
@author Ayush Sharma, January 2020
@source Hivemind, https://github.com/compserv/hivemind
@dataSource Open Computing Facility, https://www.ocf.berkeley.edu/
@dataMaintainers HKN's Computing Services Committee, https://hkn.eecs.berkeley.edu/about/officers
"""

import urllib.request, json, sys
# import datetime, time

# To get extended output, put 1 (or any other nonzero number) as an argument, as:
#   python3 telepath.py 1
# To get basic output, put nothing or 0 as an argument.

if (len(sys.argv) - 1 == 1):
    PRINTALL = int(sys.argv[1])
else :
    PRINTALL = False

serverData = json.loads(urllib.request.urlopen("https://www.ocf.berkeley.edu/~hkn/hivemind/data/latest.json").read().decode())
serverData = serverData['data']

def onlyHive(fullData):
    toReturn = {}
    for server in fullData:
        if str(server)[0:4] == "hive":
            toReturn[server] = fullData[server]
    
    return toReturn

serverData = onlyHive(serverData)

def findBestServer(hiveData):
    """
    Sweeps the dictionary and finds the best server by first finding the minimum average CPU usage and then finding the one with the fewest users.
    """
    def findMin(valueFunction, fullData):
        """
        Finds the minimum value in the data set fullData according to a value obtained by applying valueFunction to those values
        """
        minValue = None
        minValues = {}
        for data in fullData:
            if fullData[data]:
                averageValue = valueFunction(data, fullData)
                if minValue == None or averageValue < minValue:
                    minValue = averageValue
                    minValues = {}
                    minValues[data] = fullData[data]
                elif averageValue == minValue:
                    minValues[data] = fullData[data]
        return minValues
    
    bestCPU = findMin((lambda x, dataSet: dataSet[x]['load_avgs'][1]), hiveData)    # First, get the best servers by lowest average CPU usage, as Hivemind's code does
    return findMin((lambda x, dataSet: len(dataSet[x]['users'])), bestCPU)          # Then, get the best servers by fewest number of online users

bestServers = findBestServer(serverData)

def format(serverDict, sortKeyword='id'):
    """
    Returns an array of nicely formatted servers, sorted by whatever the user prefers, or id by default.
    """
    sortDict = {'id': lambda server: int(server.name[4:-3]),
                'uptime': lambda server: server.uptime}

    sortFunction = sortDict[sortKeyword]

    class Server:
        def __init__(self, serverName, dataSet):
            self.name = str(serverName)
            self.loadAvgs = dataSet[serverName]['load_avgs']
            self.users = dataSet[serverName]['users']
            self.uptime = dataSet[serverName]['uptime']
        def __str__(self):
            return str(self.name[:-3]) + " (" + str(self.loadAvgs[1] * 100) + "% mean CPU load, " + str(len(self.users)) + " users online, up for " + cleanTime(self.uptime) + ")"
    
    serverList = []

    for server in serverDict:
        serverList.append(Server(server, serverDict))
    
    # Now, sort the list based on the sorting function
    serverList.sort(key=sortFunction)

    return serverList

def cleanTime(seconds):
    hours = seconds // (60 * 60)
    minutes = (seconds % 60 * 60) // 60
    seconds = (seconds % 60)
    return str(hours)[:-2] + ":" + str(minutes)[:-2] + ":" + str(seconds)[0:5]

# print(datetime.datetime.now().time())
# print(time.time())
allServers = format(bestServers, 'uptime')

if PRINTALL:
    for server in allServers:
        print(server)
else :
    print(allServers[0].name[4:-3])

"""
Note on 1/31/2020, 4:22 PM: 'uptime' is definitely measured in seconds.

16:08:49.708358
1580515729.7094128
hive10 (0.0% mean CPU load, [] users online, up for 1990847.37 seconds)
hive19 (0.0% mean CPU load, [] users online, up for 86882.45 seconds)
hive9 (0.0% mean CPU load, [] users online, up for 15730.67 seconds)

16:19:57.909603
1580516397.9111762
hive17 (0.0% mean CPU load, [] users online, up for 87544.09 seconds)
hive18 (0.0% mean CPU load, [] users online, up for 20362.93 seconds)
hive19 (0.0% mean CPU load, [] users online, up for 87542.54 seconds)
hive20 (0.0% mean CPU load, [] users online, up for 183525.98 seconds)
hive22 (0.0% mean CPU load, [] users online, up for 4270.56 seconds)
hive23 (0.0% mean CPU load, [] users online, up for 6549.33 seconds)
hive8 (0.0% mean CPU load, [] users online, up for 349888.53 seconds)
hive9 (0.0% mean CPU load, [] users online, up for 16390.19 seconds)
"""

"""
Todo:
Implement in command-line-runnable file
"""