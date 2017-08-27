# import statements python2.7
import os
import subprocess
import sqlite3
import re


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
        self.recNo=0


    def start_run(self):
        # start and run instance of ENM11
        print('running')
        error_code = subprocess.call(self.ENMpath)
        print('finsihed')

    def read_results(self):
        print('reading results')
        with open('enm1.1ou') as f:
            self.content = f.readlines()
        results_array1 = re.findall("[+-]?[0-9]*?[.][0-9]*", self.content[54])
        results_array2 = re.findall("[+-]?[0-9]*?[.][0-9]*", self.content[55])
        results_array3 = re.findall("[+-]?[0-9]*?[.][0-9]*", self.content[56])
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
        self.wind_dir,self.wind_speed = re.findall("\d+\.\d+",self.content[13])
        print(self.wind_speed)


class SourceFile:

    path = ''

    def __init__(self):
        print('new source file')

    def write(self):
        print('writing source file')


class SectionFile:
    path = ''

    def __init__(self):
        print('new section file')

    def write(self):
        print('writing section file')


class RunFile:
    path = ''

    def __init__(self):
        print('new scenario file')

    def write(self,metCond):
        with open('enm.1cs') as f:
            content = f.readlines()
        print(content[9])
        content[9]='20,85,%d,%d, 4 ,%d,' %(metCond.wind_speed,metCond.wind_dir,metCond.temp_grad)
        print(content[9])

        print('writing scenario file')
        with open('enm.1cs', 'w') as file:
            file.writelines( content )


class Receiver:
    def __init__(self,x,y,z,h):
        print('new receiver')
        self.x=x
        self.y=y
        self.z=z
        self.h=h


class Spectrum:
    def __init__(self):
        print('new spectrum')


class Source:
    def __init__(self,x,y,z,h):
        print('new source')
        self.x=x
        self.y=y
        self.z=z
        self.h=h


class Section:
    def __init__(self,source):
        print('new section')
        self.source=source
        self.xzPointList=[]

    def add_point(self,x,z):
        self.xzPointList.append(self,x,z)


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
sourcefiletemp=SourceFile()
sectionFileTemp=SectionFile()
newRunFile=RunFile()

#create results table
results_path = "results_test.db"
results_table = ResultTable(results_path)

# loop through conjugations of met conditions and run enm adding result to database
for wind_direction in range(0,360,10):
    for wind_speed in range(0,6,1):
        newMetCond=MetCond(20,85,wind_speed,wind_direction,2)
        newRunFile.write(newMetCond)
        testRun=ENMrun(sectionFileTemp,sectionFileTemp)
        # testRun.start_run()
        testRun.read_results()
        testRun.read_wind()

        # write results to table
        testRun.write_results(results_table.conn)



