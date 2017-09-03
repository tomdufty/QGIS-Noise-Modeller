# start of main code

import pyBatchENM as pyENM
import math


class Receiver:
    def __init__(self, no, x, y, z, h):
        print('new receiver')
        self.no = no
        self.x = x
        self.y = y
        self.xOffset = 0
        self.yOffset = 0
        self.z = z
        self.h = h


class Spectrum:
    def __init__(self):
        print('new spectrum')


class Source:
    def __init__(self, no, x, y, z, spect):
        print('new source')
        self.no = no
        self.x = x
        self.y = y
        self.z = z
        self.xOffset = 0
        self.yOffset = 0
        self.spectrum = []
        for item in spect:
            self.spectrum.append(item)


class Section:
    def __init__(self, receiver, source):
        print('new section')
        self.source = source
        self.receiver = receiver
        self.xzPointList = []
        # add first point - z height as 0 for now
        self.add_point(0, 0)
        # add last point - should be moved to proper section development
        dist = math.sqrt(math.pow((receiver.x - source.x), 2) + math.pow((receiver.y - source.y), 2))
        self.add_point(dist, 0)
        self.add_point(dist + 10, 0)

    def add_point(self, x, z):
        self.xzPointList.append([x, z])


class MetCond:
    def __init__(self, temp, humidity, wind_speed, wind_dir, temp_grad, no):
        self.metCondNo = no
        self.temp = temp
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_dir = wind_dir
        self.temp_grad = temp_grad


# create results table
results_path = "results_test.db"
results_table = pyENM.ResultTable(results_path)

# create list of receivers from dummy csv file to be replaced with shapefile input

receiverlist = []
with open('receiverlist.csv') as f:
    content = f.readlines()
f.close()
for i in range(len(content)):
    arglistrec = [float(j) for j in content[i].split(',')]
    newReceiver = Receiver(*arglistrec)
    receiverlist.append(newReceiver)

# create list of sources
sourcelist = []
with open('sourcelist.csv') as f:
    content = f.readlines()
f.close()
for i in range(len(content)):
    # loop currntly redundant as each source overwrites the last
    arglistsource = [float(j) for j in content[i].split(',')]
    no, x, y, z = arglistsource[:4]
    spectrum = arglistsource[4:len(arglistsource)]
    newSource = Source(no, x, y, z, spectrum)
    sourcelist.append(newSource)

# loop through recievers, create appropriate files, run enm and write results to database
for rec in receiverlist:
    # create source file - initially only for 1 source
    sourcefiletemp = pyENM.SourceFile()
    # ivf there were more then one source we would also loop through sources
    sourcefiletemp.add_source(sourcelist[0])
    rec.xOffset = sourcefiletemp.xOffset
    rec.yOffset = sourcefiletemp.yOffset
    # create section file
    sectionFileTemp = pyENM.SectionFile(rec)
    # populate section file for each source receiver combo
    newSection = Section(rec, sourcelist[0])
    sectionFileTemp.add_section(newSection)

    # create new runfile
    newRunFile = pyENM.RunFile()

    # loop through conjugations of met conditions and run enm adding result to database
    metcondno = 0
    for wind_direction in range(0, 30, 10):
        for wind_speed in (0, 0.5, 1):
            for tempgrad in (3, 4):
                newMetCond = MetCond(20, 85, wind_speed, wind_direction, tempgrad, metcondno)
                newRunFile.write(newMetCond, rec)
                testRun = pyENM.ENMrun(sectionFileTemp, sectionFileTemp)
                testRun.start_run()
                testRun.read_results()
                # write results to table
                testRun.write_results(results_table.conn, metcondno, tempgrad)
                metcondno += 1
