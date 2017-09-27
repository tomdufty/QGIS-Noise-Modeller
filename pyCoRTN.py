# Calculation of Road Traffic Noise implemented in python for use in QGIS noise modeller


import math


def createsegments(road):
    segmentArray = []
    for node in road:
        segmentArray.append(segment(0, 0, 0, 1, 1, 1))


def calcangleofview(segment, receiver):
    print("caculating angle of view\n")


def calccrosssection(segment, receiver):
    averageHeight = 0
    pathDiff = 0
    print("caculating cross section\n")
    return averageHeight, pathDiff


def distCor(segment, receiver):
    # note  d may be calcualted as shortest perpendicular distance to extended road
    d = math.sqrt(((segment.x0 - segment.x1) / 2 - receiver.x) ^ 2 + ((segment.y0 - segment.y1) / 2 - receiver.y) ^ 2)
    h = receiver.z - (segment.z0 - segment.z1) / 2
    dddash = math.sqrt((d + 3.5) ^ 2 + h ^ 2)
    return -10 * math.log10(dddash / 13.5)


def groundabsCort(h, dist):
    I = 0.5  # % soft ground - tom be implemented later 1= soft ground
    print('calculating ground absorbtion')
    if h < 0.75:
        return 5.2 * I * math.log10(3 / (dist + 3.5))
    elif h < (dist + 5) / 6:
        return 5.2 * I * math.log10((6 * h - 1.5) / (dist + 3.5))
    else:
        return 0


def barrierCorr():
    print("barrier correction yo")
    # to be implement later - look up table required


def lowVolCorr():
    print("low volume correction???")
    # return -16.6 *math.log10(D)*math.log10(C)^2  ?? what is D and C?


class road:
    def __init__(self):
        print("new road")


class segment:
    percHeavy = 0.2
    volumeHourly = 1000
    speed = 100
    gradient = 0
    roadSurface = 0

    def __init__(self, x0, x1, y0, y1, z0, z1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1

    def basicnoiselevel(self):
        return 42.2 + 10 * math.log10(self.volumeHourly)

    def speedcorrection(self):
        return 33 * math.log10(self.speed + 40 + 500 / self.speed) + 10 * math.log10(
            1 + 5 * self.percHeavy * 100 / self.speed) - 68.8

    def deltaV(self):
        return (0.73 + (2.3 - 1.15 * self.percHeavy) * self.percHeavy) * self.gradient

    def gradCorr(self):
        return 0.3 * self.gradient
