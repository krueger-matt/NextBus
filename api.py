from urllib2 import urlopen

import xml.etree.ElementTree as ET

import requests

import pprint

#print "The next route " + line + " bus is in " + response4[x:x+z] + " minutes"

vehicleLocations = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=38&t=0")

response5 = vehicleLocations.read()

#print response5

#Function that returns all vehicles in response
def getAllVehicles(line):
    
    xml = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=" + line + "&t=0")

    response = xml.read()
    
    #root holds response5 which is the raw XML and ET.fromstring makes it into string format
    root = ET.fromstring(response)
    
    #Empty list to hold vehicle IDs
    allVehicles = []
    
    for vehicle in root.iter('vehicle'):
        iden = vehicle.get('id')
        allVehicles.append(iden)
        
    return allVehicles

#line = raw_input("What line would you like to see? ")
#print "Here is a list of all vehicle ID's on route " + line + ":"
#print getAllVehicles(line)


def getAllRoutes():
    
    xml = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=sf-muni")
    response = xml.read()
    
    root = ET.fromstring(response)
    
    allRoutes = []
    
    for route in root.iter('route'):
        tag = route.get('tag')
        allRoutes.append(tag)
        
    return allRoutes

#print "Here are all of the SF Muni routes:"
#print getAllRoutes()


def getAllAgencies():
    
    #open the XML and read it
    xml = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList")
    response = xml.read()
    
    root = ET.fromstring(response)
    
    #create empty list to hold agencies
    allAgencies = []
    
    #populate list with all agencies
    for agency in root.iter('agency'):
        tag = agency.get('tag')
        allAgencies.append(tag)
        
    return allAgencies

#print "Here are all of the Agencies using NextBus:"
#print getAllAgencies()


#routeConfig gives a list of all stops on a route
#"&terse" suppresses "path" data (path data is helpful for drawing a map)
def getStops(line):
    xml = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r=" + line + "&terse")
    response = xml.read()
    
    root = ET.fromstring(response)
    
    #Create an empty dictionary. For loop will add tag as key and title as value
    allStops = {}

    for stop in root.iter('stop'):
        tag = stop.get('tag')
        title = stop.get('title')
        #Test if title is None (since some of the XML returns stop IDs with no title
        if title is not None:
            allStops.update({tag:title})
            
    
    return allStops

line = raw_input("What line would you like to see the stops for? ")
print "Here is a list of all the stops on route " + line + ":"
#pprint will print a dictionary with each key/value pair on its own line
pprint.pprint(getStops(line))



#stopPrediction gives real time predictions for a specific stop
#a=sf-muni for agency - can use response
#r=38 for line - can use response2
#s=4760 for stop - can use response3

#line = '38'

#stopPrediction = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=" + line + "&s=4760")

#response4 = stopPrediction.read()

#print response4

#minutes = '''minutes="'''
#x = response4.find(minutes) + 9

#Check if second character after x is a "
#y = response4[x+1:x+2]

#If it is a " then z = 1 otherwise z = 2 so we get proper formatting
#if y == '\"':
#    z = 1
#else:
#    z = 2

def getPrediction(line,stop):
    xml = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=" + line + "&s=" + stop)
    response = xml.read()
    
    root = ET.fromstring(response)
    
    allPredictions = {}

    for prediction in root.iter('prediction'):
        vehicle = prediction.get('vehicle')
        minutes = prediction.get('minutes')
        allPredictions.update({vehicle:minutes})
        
    return allPredictions


line = raw_input("What line would you like to see? ")
stop = raw_input("What stop would you like to see a prediction for? ")

pprint.pprint(getPrediction(line,stop))

#xml = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=" + line + "&s=" + stop)
#response = xml.read()
#
#root = ET.fromstring(response)
#    
#print response