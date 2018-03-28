import requests
import json
from threading import Thread, Lock
from pprint import pprint
from lab2_parser import *

url = "https://desolate-ravine-43301.herokuapp.com"

mutex = Lock()
sensorData = {}

def getKeyAndPaths():
    paths = []
    r = requests.post(url)
    key = r.headers.get('Session')
    body = r.json()
    #pprint(body)

    for item in body:
        paths.append(item['path'])

    return key, paths

def requestSensorData(header, path):
    response = requests.get(url + path, headers = getHeader)
    print(response.content)
    contentType = response.headers.get('content-type')
    if contentType != 'text/plain; charset=utf-8':
        parsed = parseData(contentType, response.content)
        colectParsedData(parsed)


def startDataRequesting(header, paths):
    threads = []
    for path in paths:
        print(path)
        t = Thread(target = requestSensorData, args = (header, path))
        t.start()
        threads.append(t)

    return threads

def joinThreads(threads):
    for thread in threads:
        thread.join()

def colectParsedData(parsedData):
    mutex.acquire()
    for sensorType, sensorInfo in parsedData:
        if sensorType not in sensorData.keys():
            sensorData[sensorType] = []
        sensorData[sensorType].append(sensorInfo)
    mutex.release()

def showAggregatedData(sensorData):
    for sensorType in sensorData.keys():
        if sensorType == 0:
            nameOf = 'Temperature'
        elif sensorType == 1:
            nameOf = 'Humidity'
        elif sensorType == 2:
            nameOf = 'Motion'
        elif sensorType == 3:
            nameOf = 'Alien Presence'
        elif sensorType == 4:
            nameOf = 'Dark Matter'
        else:
            nameOf = 'No name Sensor'
        print(nameOf)
        for sensorValue in sensorData[sensorType]:
            print sensorValue['id'], sensorValue['value']
        print('\n')

key, paths = getKeyAndPaths()
getHeader = {'Session' : key}
threads = startDataRequesting(getHeader, paths)
joinThreads(threads)
showAggregatedData(sensorData)
