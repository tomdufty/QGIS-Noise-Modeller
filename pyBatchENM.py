class ENMrun:

    ENMpath=''

    def __init__(self,source,section):
        self.source=source
        self.section=section

    def start_run(self):
        print('running')

    def read_results(self):
        print('reading results')


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


class Reciever:
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