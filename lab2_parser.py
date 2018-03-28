import json
import xml.etree.ElementTree as ET

def parseData(contentTye, data):
    if contentTye == 'Application/xml':
        parser = xmlParser
    elif contentTye == 'Application/json':
        parser = jsonParser
    elif contentTye == 'text/csv':
        parser = csvParser

    return parser(data)

def getTuple(type, id, value):
    return (int(type), {
        'id' : id,
        'value' : value
    })

def xmlParser(data):
    xml = ET.fromstring(data)

    return [getTuple(xml.find('type').text ,
                     xml.attrib.get('id'),
                     xml.find('value').text)]


def jsonParser(data):
    jsonData = json.loads(data)

    return [getTuple(jsonData['sensor_type'],
                     jsonData['device_id'],
                     jsonData['value'])]

def csvParser(data):
    data = data.split('\n')
    data.pop(len(data) - 1)
    data.pop(0)
    csvData = []
    for element in data:
        sensorData = element.split(',')
        csvData.append(getTuple(sensorData[1],
                                sensorData[0],
                                sensorData[2]))

    return csvData
