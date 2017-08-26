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

#start of main code
sourcefiletemp=SourceFile()
sectionFileTemp=SectionFile()
testRun=ENMrun(sectionFileTemp,sectionFileTemp)
testRun.start_run()
testRun.read_results()

#

results_connection=sqlite3.connect()