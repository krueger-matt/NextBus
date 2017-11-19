# Prints upcoming vehicle IDs and how many minutes away they are from a given station
from urllib2 import urlopen
import xml.etree.ElementTree as ET

#line = raw_input("What line would you like to see predictions for? ")
#stop = raw_input("What stop would you like to see a prediction for? ")

line = 'N'
stop = '6994' #Montgomery Station Outbound
agency = 'sf-muni'

#Get real time predictions for a stop on a route

xml = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=" + agency + "&r=" + line + "&s=" + stop)
response = xml.read()

root = ET.fromstring(response)

for predictions in root.iter('predictions'):
    station = predictions.get('stopTitle')

vehicles = []
minutes = []

for prediction in root.iter('prediction'):
    if line == 'N':
        iden = "train: " + prediction.get('vehicle')
    else:
        iden = "bus: " + prediction.get('vehicle')
    vehicles.append(iden)
    iden = prediction.get('minutes') + " minutes"
    minutes.append(iden)
    
vehMin = []
vehMin.append(vehicles)
vehMin.append(minutes)

print "Here are upcoming departures for the " + line + " at " + station + ":"
for x in range(len(vehicles)):
    print zip(*vehMin)[x]