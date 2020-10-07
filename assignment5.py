#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Week 5 Assignment
Dave Soto"""

#Import important libraries.

import urllib.request
from io import StringIO
import csv
import argparse



# class server and request are very similar to the Printing example in the notes
class Server:
    def __init__(self):

        self.currentTask = None
        self.timeRemaining = 0

    def tick(self):
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        if self.currentTask != None:
            return True
        else:
            return False

    def startNext(self, newtask):
        self.currentTask = newtask
        self.timeRemaining = newtask.getTime()


class Request:
    def __init__(self, data):
        self.timestamp = int(data[0])
        self.timetaken = int(data[2])

    def getStamp(self):
        return self.timestamp

    def getPages(self):
        return self.pages

    def getTime(self):
        return self.timetaken

    def waitTime(self, currenttime):
        return currenttime - self.timestamp


def main():
    """download the contents"""

    # Initialize parser
    commandParser = argparse.ArgumentParser(description="Send a ­­url parameter to the script")
    # add parameter for file
    commandParser.add_argument("--file", type=str, help="Link to the csv file")
    # add parameter for servers
    commandParser.add_argument("--servers", type=int, help="Link to the csv file")
    # parse the argument
    args = commandParser.parse_args()
    # if url is not given
    if not args.file:
        exit()
    if not args.servers:  # id servers not in parameters use simulateOneServer function
        simulateOneServer(args.file)
    else:  # else simulate multiple servers function
        simulateManyServers(args.file, args.servers)


def simulateOneServer(file):
    """function to handle requests using one server"""

    content = urllib.request.urlopen(file).read().decode("ascii", "ignore")  # fetch contents
    data = StringIO(content)
    # read csv file
    csv_reader = csv.reader(data, delimiter=',')

    dataList = []  # store data from csv

    for line in csv_reader:
        # Use list to store data
        dataList.append(line)

    requestQueue = Queue()  # queue tor requests
    waitingtimes = []  # list to store waiting time before a request is processed
    server = Server()  # instantiate server class
    # listlength=len(dataList)-1
    for i in dataList:
        # iterate the requests
        request = Request(i)  # pass data to request class
        requestQueue.enqueue(request)  # enqueue the request object
        if (not requestQueue.isEmpty()) and (not server.busy()):  # if server is not busy and queue is not empty
            nexttask = requestQueue.dequeue()  # dequeue first item in queue
            waitingtimes.append(nexttask.waitTime(int(i[0])))  # append to waiting time to list
            server.startNext(nexttask)  # if server is free move to the next task
        server.tick()  # server timer
        averageWait = sum(waitingtimes) / len(waitingtimes)  # calculate average wait time
        print("Average Wait %6.2f secs %3d tasks remaining." % (
        averageWait, requestQueue.size()))  # similar to pritning example in notes

    print("Average latency is {} seconds".format(averageWait))
    return averageWait  # return latency


def simulateManyServers(file, noOfServers):
    content = urllib.request.urlopen(file).read().decode("ascii", "ignore")  # retireve the contents contents
    data = StringIO(content)
    # read csv file
    csv_reader = csv.reader(data, delimiter=',')

    dataList = []  # store data from csv file
    for line in csv_reader:
        dataList.append(line)

    requestQueue = Queue() 
    waitingtimes = []  # to store waiting times in the queue
    servers = [Server() for a in range(noOfServers)]
    
    for i in dataList:
        request = Request(i)  
        requestQueue.enqueue(request)
        
        for server in servers:  # iterate through the servers
            if (not server.busy()) and (
            not requestQueue.isEmpty()):  # icheck the queue if not empty move to the next
                nexttask = requestQueue.dequeue()  # dequeue last item
                waitingtimes.append(nexttask.waitTime(int(i[0]))) 
                server.startNext(nexttask) 
            server.tick()  
        averageWait = sum(waitingtimes) / len(waitingtimes)
        print("Average Wait %6.2f secs %3d tasks remaining." % (averageWait, requestQueue.size()))

    print("Average latency is {} seconds".format(averageWait))
    return (averageWait)  # return the avaerge latency for the task


# Call main function when script runs
if __name__ == "__main__":
    main()
