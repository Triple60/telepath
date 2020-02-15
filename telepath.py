"""
@author Ayush Sharma, January 2020
@source Hivemind, https://github.com/compserv/hivemind
@dataSource Open Computing Facility, https://www.ocf.berkeley.edu/
@dataMaintainers HKN's Computing Services Committee, https://hkn.eecs.berkeley.edu/about/officers
"""

import urllib.request, json, sys

# To get extended output, put 1 (or any other nonzero number) as an argument, as:
#   python3 telepath.py 1
# To get basic output, put nothing or 0 as an argument.

if (len(sys.argv) - 1 == 1):
    PRINTALL = int(sys.argv[1])
else :
    PRINTALL = False

def onlyHive(fullData):
    """
    Parses the fullData set and returns only those servers with "hive" in their name.
    This could probably be generalized to return other machines like those in Soda.
    """
    toReturn = {}
    for server in fullData:
        if str(server)[0:4] == "hive":
            toReturn[server] = fullData[server]
    
    return toReturn

def cleanTime(seconds):
    """
    A function used for more detailed input that converts a time in seconds to hh:mm:ss.
    """
    hours = seconds // (60 * 60)
    minutes = (seconds % 60 * 60) // 60
    seconds = (seconds % 60)
    return str(hours)[:-2] + ":" + str(minutes)[:-2] + ":" + str(seconds)[0:5]

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

serverData = json.loads(urllib.request.urlopen("https://www.ocf.berkeley.edu/~hkn/hivemind/data/latest.json").read().decode())
serverData = serverData['data']

serverData = onlyHive(serverData)
bestServers = findBestServer(serverData)
allServers = format(bestServers, 'uptime')

if PRINTALL:
    for server in allServers:
        print(server)
else :
    print(allServers[0].name[4:-3])