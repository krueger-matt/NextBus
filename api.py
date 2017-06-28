from urllib2 import urlopen

import xml.etree.ElementTree as ET

import requests

#response is a list of all agencies
agency = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList")
response = agency.read()

muni = '''<agency tag="sf-muni'''

#print response
#print response.find(muni)

#x is start of string that finds where Muni is in list. Y is end of string (+2 added to account for /> which is used to find end of string)
x = response.find(muni)
y = response[x:].find("/>") + 2

#print response[x:x+y]

#route is a list of all routes
#a=sf-muni gives all routes for Muni
route = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=sf-muni")
response2 = route.read()

#print response2

#routeConfig gives a list of all stops on a route
#"&terse" suppresses "path" data (path data is helpful for drawing a map)
routeConfig = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r=38&terse")

response3 = routeConfig.read()

#print response3

#stopPrediction gives real time predictions for a specific stop
#a=sf-muni for agency - can use response
#r=38 for line - can use response2
#s=4760 for stop - can use response3

line = '38'

stopPrediction = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=" + line + "&s=4760")

response4 = stopPrediction.read()

#print response4

minutes = '''minutes="'''
x = response4.find(minutes) + 9

#Check if second character after x is a "
y = response4[x+1:x+2]

#If it is a " then z = 1 otherwise z = 2 so we get proper formatting
if y == '\"':
    z = 1
else:
    z = 2

print "The next route " + line + " bus is in " + response4[x:x+z] + " minutes"

vehicleLocations = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=38&t=0")

response5 = vehicleLocations.read()

#print response5

#Function that returns all vehicles in response5
def getAllVehicles():
    
    #root holds response5 which is the raw XML and ET.fromstring makes it into string format
    root = ET.fromstring(response5)
    
    #Empty list to hold vehicle IDs
    allVehicles = []
    
    for vehicle in root.iter('vehicle'):
        iden = vehicle.get('id')
        allVehicles.append(iden)
        
    return allVehicles
        
print "Here is a list of all vehicle ID's on route " + line + ":"
print getAllVehicles()


def getAllRoutes():
    
    root = ET.fromstring(response2)
    
    allRoutes = []
    
    for route in root.iter('route'):
        tag = route.get('tag')
        allRoutes.append(tag)
        
    return allRoutes

print "Here are all of the SF Muni routes:"
print getAllRoutes()


def getAllAgencies():
    
    root = ET.fromstring(response)
    
    allAgencies = []
    
    for agency in root.iter('agency'):
        tag = agency.get('tag')
        allAgencies.append(tag)
        
    return allAgencies

print "Here are all of the Agencies using NextBus:"
print getAllAgencies()
