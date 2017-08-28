# import statements python2.7
import os
import subprocess
import sqlite3
import re
import math

COORDINATE_LIMIT=32000

class ENMrun:

    ENMpath=r"C:/ENM/ENM11.EXE"
    error_code=0

    def __init__(self,source,section):
        self.source_file = source
        self.section_file = section
        self.results_array = []
        self.wind_speed=0
        self.wind_dir=0
        self.metCondNo=0
        self.recNo=section.rec.no


    def start_run(self):
        # start and run instance of ENM11
        print('running')
        error_code = subprocess.call(self.ENMpath)
        print('finsihed')

    def read_results(self):
        print('reading results')
        with open('enm1.1ou') as f:
            self.content = f.readlines()
        for index in range(len(self.content)):
            if self.content[index][1:6]=='TOTAL':
                resultindex=index
        results_array1 = re.findall("[+-]?[0-9]*?[.][0-9]*", self.content[resultindex])
        results_array2 = re.findall("[+-]?[0-9]*?[.][0-9]*", self.content[resultindex+1])
        results_array3 = re.findall("[+-]?[0-9]*?[.][0-9]*", self.content[resultindex+2])
        self.results_array.append(results_array1[0])
        for j in range(len(results_array2)):
             self.results_array.append(results_array1[j+1])
             self.results_array.append(results_array2[j])
             self.results_array.append(results_array3[j])




    def write_results(self,connection):
        print("writing results to table")
        query="INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        self.results_array.insert(0,self.wind_dir)
        self.results_array.insert(0, self.wind_speed)
        self.results_array.insert(0,self.metCondNo)
        self.results_array.insert(0, self.recNo)
        # get max id in orer to create unique primary key
        cursor=connection.execute('SELECT max(id) FROM results ')
        max_id = cursor.fetchone()[0]
        if max_id is None:
            max_id=-1
        self.results_array.insert(0,max_id+1)
        [float(i) for i in self.results_array]
        connection.execute(query,self.results_array)
        connection.commit()


    def count_result_source(self):
        count = 0
        for i in range(len(self.content)):
            if len(self.content[i])>2:
                if self.content[i][1:7] == "SOURCE":
                    count += 1
        return count

    def read_wind(self):
        with open('enm1.1ou') as f:
            self.content = f.readlines()
        for index in range(len(self.content)):
            if self.content[index][1:5]=='WIND':
                windindex=index+1
        self.wind_dir,self.wind_speed = re.findall("[+-]?[0-9]*?[.][0-9]*",self.content[windindex])
        f.close()


class SourceFile:

    path = 'C:/ENM/Sources/QGISENM.SRC'
    demo_path='INPDEMO'


    def __init__(self):
        print('new source file')
        self.numberSource = 0
        self.xOriginMoved = False
        self.yOriginMoved = False
        self.xOffset = 0
        self.yOffset = 0


        with open(self.demo_path) as demosrcfile:
            initial_content=demosrcfile.readlines()
        demosrcfile.close()
        with open(self.path,'w') as srcfile:
            srcfile.writelines(initial_content)
        srcfile.close()

    def add_source(self,source):
        print('writing source file')
        x,y,z = source.x-self.xOffset,source.y-self.yOffset,source.z
        # check and see if source is within limits
        if x>COORDINATE_LIMIT:
            if self.xOriginMoved==False:
                self.xOffset=x-COORDINATE_LIMIT/2
                x=x-self.xOffset
                self.xOriginMoved=True
                source.xOffset=self.xOffset
            else:
                print('out of bounds')
                return
        if y>COORDINATE_LIMIT:
            if self.yOriginMoved==False:
                self.yOffset=y
                y=y-self.yOffset
                self.yOriginMoved=True
                source.yOffset=self.yOffset
            else:
                print('out of bounds')
                return

        spectrum=source.spectrum
        with open(self.path,'r') as srcfile:
            src_content=srcfile.readlines()
        with open(self.path,'w') as srcfile:
            for index in range(len(src_content)):
                if src_content[index][0:8] == '*X, Y, Z':
                    xyzindex=index+1
                if src_content[index][0:6] == '*Level':
                    Levelindex=index+1
            src_content[xyzindex]='%.0f    %.0f    %.1f    0    0    0\n'%(x,y,z)
            src_content[Levelindex] = '             %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f\n'%tuple(
                spectrum[0::3]
            )
            src_content[Levelindex+1] = '             %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f\n' % tuple(
               spectrum[1::3]
            )
            src_content[Levelindex+2] = '             %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f\n' % tuple(
                spectrum[2::3]
            )
            srcfile.writelines(src_content)
            self.numberSource += 1


class SectionFile:
    path = 'C:/ENM/Sections/QGISENM.SEC'

    def __init__(self,rec):
        self.rec=rec
        print('new section file')
        with open (self.path,'w') as srcfile:
            srcfile.seek(0)
            srcfile.truncate()

    def add_section(self,section):
        print('writing section file')
        recx=section.receiver.x-section.source.xOffset
        recy = section.receiver.y - section.source.yOffset
        srcx = section.source.x - section.source.xOffset
        srcy = section.source.y - section.source.yOffset
        sec_content=[]
        sec_content.append('*T\n')
        sec_content.append('{%.1f, %.1f}to{%.1f, %.1f}\n'%(srcx,srcy,recx,recy))
        sec_content.append('*X\n')
        sec_content.append(' '+'{:<14.0f}{:<14.0f}{:<5.1f}\n'.format(srcx,srcy,section.source.z))
        sec_content.append('*R\n')
        sec_content.append(' '+'{:<14.0f}{:<14.0f}{:<5.1f}\n'.format(recx,recy,section.receiver.z))
        sec_content.append('*G-V3\n%d,%d,0,1000,0,25,-15,15,0,\'GM\'\n'%(section.source.no,len(section.xzPointList)))
        for point in section.xzPointList:
            sec_content.append(' ' + '{:<14.1f}{:<14.1f}{:<2d}\n'.format(point[0],point[1], 4))
        sec_content.append(' '+'{:<14d}{:<14d}{:<2d}\n'.format(0,0,0))
        with open(self.path,'a') as srcfile:
            srcfile.writelines(sec_content)


class RunFile:
    path = ''

    def __init__(self):
        print('new scenario file')

    def write(self,metCond):
        with open('enm.1cs') as f:
            content = f.readlines()
        f.close()

        content[4]='QGISENM.SRC\n'
        content[6] = 'QGISENM.SEC\n'
        content[9]='20,85,%d,%d, 4 ,%d,\n' %(metCond.wind_speed,metCond.wind_dir,metCond.temp_grad)


        print('writing scenario file')
        with open('enm.1cs', 'w') as file:
            file.writelines(content)
        file.close()


class Receiver:
    def __init__(self,no,x,y,z,h):
        print('new receiver')
        self.no=no
        self.x=x
        self.y=y
        self.z=z
        self.h=h


class Spectrum:
    def __init__(self):
        print('new spectrum')


class Source:
    def __init__(self,no,x,y,z,spect):
        print('new source')
        self.no=no
        self.x=x
        self.y=y
        self.z=z
        self.xOffset=0
        self.yOffset=0
        self.spectrum = []
        for item in spect:
            self.spectrum.append(item)



class Section:
    def __init__(self,receiver,source):
        print('new section')
        self.source=source
        self.receiver=receiver
        self.xzPointList=[]
        # add first point - z heigh as 0 for now
        self.add_point(0,0)
        # add last point - should be moved to proper section development
        dist=math.sqrt(math.pow((receiver.x-source.x),2)+math.pow((receiver.y-source.y),2))
        self.add_point(dist,0)
        self.add_point(dist+10,0)

    def add_point(self,x,z):
        self.xzPointList.append([x,z])


class MetCond:
    def __init__(self,temp,humidity,wind_speed,wind_dir,temp_grad):
        self.temp=temp
        self.humidity=humidity
        self.wind_speed=wind_speed
        self.wind_dir=wind_dir
        self.temp_grad=temp_grad


class ResultTable:
    sql_create_results_table = """ CREATE TABLE IF NOT EXISTS results (
                                            id integer PRIMARY KEY,
                                            RecNo integer NOT NULL,
                                            MetCondNo integer NOT NULL,
                                            direction FLOAT(5),
                                            speed FLOAT(5),
                                            total FLOAT(5),
                                            r25Hz float(5),
                                            r31_5Hz float(5),
                                            r40Hz float(5),
                                            r50Hz float(5),
                                            r63Hz float(5),
                                            r80Hz float(5),
                                            r100Hz float(5),
                                            r125Hz float(5),
                                            r160Hz float(5),
                                            r200Hz float(5),
                                            r250Hz float(5),
                                            r315Hz float(5),
                                            r400Hz float(5),
                                            r500Hz float(5),
                                            r630Hz float(5),
                                            r800Hz float(5),
                                            r1kHz float(5),
                                            r1_25kHz float(5),
                                            r1_6kHz float(5),
                                            r2kHz float(5),
                                            r2_5kHz float(5),
                                            r3_15kHz float(5),
                                            r4kHz float(5),
                                            r5kHz float(5),
                                            r6_3kHz float(5),
                                            r8kHz float(5),
                                            r10kHz float(5),
                                            r12_5kHz float(5),
                                            r16kHz float(5),
                                            r20kHz float(5)
                                        ); """

    def __init__(self,result_path):
        try:
            self.conn = sqlite3.connect(result_path)
        except Exception as e:
            print(e)
        if self.conn is not None:
            try:
               c = self.conn.cursor()
               print("create table")
               c.execute(self.sql_create_results_table,())
            except Exception as e:
                print("exception")
                print(e)

# start of main code

#create results table
results_path = "results_test.db"
results_table = ResultTable(results_path)

#create list of receivers from dummy csv file to be replaced wiht shapefile input

receiverlist=[]
with open('receiverlist.csv') as f:
    content = f.readlines()
f.close()
for i in range(len(content)):
    arglistrec=[float(j) for j in content[i].split(',')]
    newReceiver=Receiver(*arglistrec)
    receiverlist.append(newReceiver)

#create list of sources
sourcelist=[]
with open('sourcelist.csv') as f:
    content = f.readlines()
f.close()
for i in range(len(content)):
    # loop currntly redundant as each source overwrites the last
    arglistsource=[float(j) for j in content[i].split(',')]
    no,x,y,z=arglistsource[:4]
    spectrum=arglistsource[4:len(arglistsource)]
    newSource=Source(no,x,y,z,spectrum)
    sourcelist.append(newSource)

# loop through recievers, create appropriate files, run enm and write results to database
for rec in receiverlist:
    # create source file - initally only for 1 source
    sourcefiletemp=SourceFile()
    # ivf there were more then one source we would also loop through sources
    sourcefiletemp.add_source(sourcelist[0])
    #create section file
    sectionFileTemp=SectionFile(rec)
    # populaate section file for each soruce reciever combo
    newSection=Section(rec,sourcelist[0])
    sectionFileTemp.add_section(newSection)

    #create new rufile
    newRunFile=RunFile()



# loop through conjugations of met conditions and run enm adding result to database
# for wind_direction in range(0,360,10):
#    for wind_speed in range(0,6,1):
#        newMetCond=MetCond(20,85,wind_speed,wind_direction,2)
#        newRunFile.write(newMetCond)
#        testRun=ENMrun(sectionFileTemp,sectionFileTemp)
#        testRun.start_run()
#        testRun.read_results()
#        testRun.read_wind()

        # write results to table
#        testRun.write_results(results_table.conn)

    newMetCond=MetCond(20,85,3,180,2)
    newRunFile.write(newMetCond)
    testRun=ENMrun(sectionFileTemp,sectionFileTemp)
    testRun.start_run()
    testRun.read_results()
    testRun.read_wind()

     # write results to table
    testRun.write_results(results_table.conn)

