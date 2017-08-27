# import statements python2.7
import os
import subprocess
import sqlite3

class ENMrun:

    ENMpath=r"C:/ENM/ENM11.EXE"
    error_code=0

    def __init__(self,source,section):
        self.source_file=source
        self.section_file=section

    def start_run(self):
        # start and run instance of ENM11
        print('running')
        error_code = subprocess.call(self.ENMpath)
        print('finsihed')

    def read_results(self):
        print('reading results')
        with open('enm1.1ou') as f:
            self.content=f.readlines()
        for i in range(len(self.content)):
            print(self.content[i])


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


class ScenarioFile:
    path = ''

    def __init__(self):
        print('new scenario file')

    def write(self):
        print('writing scenario file')


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
                                            SourceNo integer NOT NULL,
                                            MetCondNo integer NOT NULL,
                                            speed FLOAT(5),
                                            direction FLOAT(5),
                                            r12_5Hz FLOAT(5),
                                            r16Hz float(5),
                                            r20Hz float(5),
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
            conn = sqlite3.connect(result_path)
        except Exception as e:
            print(e)
        if conn is not None:
            try:
               c = conn.cursor()
               print("create table")
               c.execute(self.sql_create_results_table,())
               print("executed")
            except Exception as e:
                print("exception")
                print(e)

# start of main code
# sourcefiletemp=SourceFile()
# sectionFileTemp=SectionFile()
# testRun=ENMrun(sectionFileTemp,sectionFileTemp)
# testRun.start_run()
# testRun.read_results()

results_path = "results_test.db"
results_table = ResultTable(results_path)
