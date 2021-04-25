import re
import sys

def GetCoordinate(line):
    results = re.search("<coordinates>(.*)</coordinates>", line)
    if results is None:
        return
    coord = results.groups()[0].split(',')
    print("{}, {}".format(coord[1], coord[0]))

def GetName(line):
    results = re.search("<name>(.*)</name>", line)
    if results is None:
        return
    print(results.groups()[0])


fileName = sys.argv[1]
print(fileName)


lines = []
with open(fileName, "r") as f:
    lines = f.readlines()
    

for line in lines:
    if "coordinates" in line:
        GetCoordinate(line)
    if "name" in line:
        GetName(line)
