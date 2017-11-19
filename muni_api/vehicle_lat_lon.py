#This prints each vehicle ID and its Lat/Long on a separate line
from urllib2 import urlopen
import xml.etree.ElementTree as ET

line = 'N'
agency = 'sf-muni'

xml = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=" + agency + "&r=" + line + "&t=0")
response = xml.read()

root = ET.fromstring(response)
allVehicles = []
allLatitudes = []
allLongitudes = []

for vehicle in root.iter('vehicle'):
    iden = vehicle.get('id')
    if vehicle.get('predictable') == 'true':
        allVehicles.append(iden)
    iden = vehicle.get('lat')
    if vehicle.get('predictable') == 'true':
        allLatitudes.append(iden)
    iden = vehicle.get('lon')
    if vehicle.get('predictable') == 'true':
        allLongitudes.append(iden)
    
vehLatLon = []
vehLatLon.append(allVehicles)
vehLatLon.append(allLatitudes)
vehLatLon.append(allLongitudes)

print "Here is a list of all vehicle ID's on route " + line + ":"
for x in range(len(allVehicles)):
    print zip(*vehLatLon)[x]