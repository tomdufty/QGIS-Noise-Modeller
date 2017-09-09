# import statements python2.7
import subprocess
import sqlite3
import re

COORDINATE_LIMIT = 32000


class ENMrun:
    ENMpath = r"C:/ENM/ENM11.EXE"
    error_code = 0

    def __init__(self,source,section):
        self.source_file = source
        self.section_file = section
        self.results_array = []
        self.wind_speed = 0
        self.wind_dir = 0
        self.tempGrad = 0
        self.metCondNo = 0
        self.recNo = section.rec.no
        self.source_no = 0

    def start_run(self):
        # start and run instance of ENM11
        print('running')
        error_code = subprocess.call(self.ENMpath)
        print('finished')

    def read_results(self):
        result_index = []
        wind_index = -1
        source_index = []

        print('reading results')
        with open('enm1.1ou') as f:
            out_content = f.readlines()
        for index in range(len(out_content)):
            if out_content[index][1:6] == 'TOTAL':
                result_index.append(index)
            if out_content[index][1:5] == 'WIND':
                wind_index = index + 1
            if out_content[index][1:7] == 'SOURCE':
                source_index.append(index)
        print(result_index)
        print(source_index)
        source_count = 0
        for i in range(len(source_index)):
            print(source_count)
            singe_source_result = []
            results_array1 = re.findall("[+-]?[0-9]*?[.][0-9]*", out_content[result_index[i]])
            results_array2 = re.findall("[+-]?[0-9]*?[.][0-9]*", out_content[result_index[i] + 1])
            results_array3 = re.findall("[+-]?[0-9]*?[.][0-9]*", out_content[result_index[i] + 2])
            singe_source_result.append(results_array1[0])
            for j in range(len(results_array2)):
                singe_source_result.append(results_array1[j + 1])
                singe_source_result.append(results_array2[j])
                singe_source_result.append(results_array3[j])
            self.results_array.append(singe_source_result)
            self.source_no = re.findall("[+-]?[0-9]*?[.][0-9]*", out_content[source_index[source_count]])
            source_count += 1
        self.wind_dir, self.wind_speed = re.findall("[+-]?[0-9]*?[.][0-9]*", out_content[wind_index])

        f.close()

    def write_results(self, connection, metcondno, tempgrad):
        print("writing results to table")
        query = "INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        for i in self.results_array:
            i.insert(0, tempgrad)
            i.insert(0, self.wind_dir)
            i.insert(0, self.wind_speed)
            i.insert(0, metcondno)
            i.insert(0, self.recNo)
            # get max id in order to create unique primary key
            cursor = connection.execute('SELECT max(id) FROM results ')
            max_id = cursor.fetchone()[0]
            if max_id is None:
                max_id = -1
            i.insert(0, max_id + 1)
            [float(j) for j in i]
            connection.execute(query, i)
            connection.commit()


class SourceFile:

    path = 'C:/ENM/Sources/QGISENM.SRC'
    demo_path = 'INPDEMO'

    def __init__(self):
        print('new source file')
        self.numberSource = 0
        self.xOriginMoved = False
        self.yOriginMoved = False
        self.xOffset = 0
        self.yOffset = 0
        # individual source in third octaves

        with open(self.path,'w') as srcfile:
            srcfile.seek(0)
            srcfile.truncate()
        srcfile.close()

    def add_source(self, source):
        print('writing source file')
        x, y, z = source.x - self.xOffset, source.y - self.yOffset, source.z
        spectrum = source.spectrum
        # check and see if source is within limits
        if x > COORDINATE_LIMIT:
            if self.xOriginMoved is False:
                self.xOffset = x - COORDINATE_LIMIT / 2
                x = x - self.xOffset
                self.xOriginMoved = True
                source.xOffset = self.xOffset
            else:
                print('out of bounds')
                return
        if y > COORDINATE_LIMIT:
            if self.yOriginMoved is False:
                self.yOffset = y
                y = y - self.yOffset
                self.yOriginMoved = True
                source.yOffset = self.yOffset
            else:
                print('out of bounds')
                return
        # pooorly  ofrmatted string to replaced with properly formatted array string
        string = '*H-Third Octave\n'\
            '*Y\n'\
            '1,1\n'\
            '2,1\n'\
            '3,1\n'\
            '4,1\n'\
            '5,1\n'\
            '6,1\n'\
            '7,1\n'\
            '*Title\n'\
            '\n'\
            '*Page\n'\
            '1 , 0 , 0 , 0, 0\n'\
            '\n'\
            '\n'\
            '*= Formula\n'\
            '\n'\
            '*Source\n'\
            ' %d  ,\'POINT\' , 0 ,  , %d ,\n'\
            '*Title\n'\
            '\n'\
            '*I\n'\
            '\n'\
            '\n'\
            '*X, Y, Z: Source Coordinates\n'\
            '%f    %f    %f    0    0    0\n'\
            '*Frequency Range\n'\
            ' 1 , 30 ,\'SPECT\'\n'\
            '            ----------------------FREQUENCY HZ----------------------\n'\
            '             31.5   63   125   250   500    1k    2k    4k    8k   16k\n'\
            '*Level\n'\
            '            %f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,\n'\
            '            %f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,\n'\
            '            %f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,%f   ,\n'\
            '*Directivity-V3.05\n'\
            '0,0,22.5,0,0,0,0\n' % (source.no, source.no, x, y, z, spectrum[0], spectrum[3], spectrum[6],
                                    spectrum[9], spectrum[12], spectrum[15],spectrum[18], spectrum[21], spectrum[24],
                                    spectrum[27], spectrum[1], spectrum[4], spectrum[7], spectrum[10], spectrum[13],
                                    spectrum[16], spectrum[19], spectrum[22],spectrum[25], spectrum[28], spectrum[2],
                                    spectrum[5], spectrum[8], spectrum[11], spectrum[14], spectrum[17], spectrum[20],
                                    spectrum[23], spectrum[26], spectrum[29])

        # with open(self.path, 'r') as srcfile:
        #     src_content = srcfile.readlines()
        with open(self.path, 'a') as srcfile:
            #previous method of writing source file based on demo file - delete when succesfully made redundant

            # for index in range(len(src_content)):
            #     if src_content[index][0:8] == '*X, Y, Z':
            #         xyzindex = index + 1
            #     if src_content[index][0:6] == '*Level':
            #         Levelindex = index + 1
            #     print(xyzindex)
            #     print(Levelindex)
            #     src_content[xyzindex] = '%.0f    %.0f    %.1f    0    0    0\n' % (x, y, z)
            #     src_content[Levelindex] = '             %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f' \
            #                               '  %0.1f\n' % tuple(
            #         spectrum[0::3]
            #     )
            #     src_content[Levelindex + 1] = '             %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f' \
            #                                   '  %0.1f\n' % tuple(
            #        spectrum[1::3]
            #     )
            #     src_content[Levelindex + 2] = '             %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f  %0.1f' \
            #                                   '  %0.1f\n' % tuple(
            #         spectrum[2::3]
            #     )

            srcfile.writelines(string)
            self.numberSource += 1


class SectionFile:
    path = 'C:/ENM/Sections/QGISENM.SEC'

    def __init__(self, rec):
        self.rec = rec
        print('new section file')
        with open(self.path, 'w') as srcfile:
            srcfile.seek(0)
            srcfile.truncate()

    def add_section(self,section):
        print('writing section file')
        recx = section.receiver.x - section.source.xOffset
        recy = section.receiver.y - section.source.yOffset
        srcx = section.source.x - section.source.xOffset
        srcy = section.source.y - section.source.yOffset
        sec_content = []
        sec_content.append('*T\n')
        sec_content.append('{%.1f, %.1f}to{%.1f, %.1f}\n' % (srcx,srcy,recx,recy))
        sec_content.append('*G-V3\n%d,%d,0,1000,0,25,-15,15,0,\'GM\'\n' % (section.source.no, len(section.xzPointList)))
        for point in section.xzPointList:
            sec_content.append(' ' + '{:<14.1f}{:<14.1f}{:<2d}\n'.format(point[0], point[1], 4))
        sec_content.append(' '+'{:<14d}{:<14d}{:<2d}\n'.format(0, 0, 0))
        with open(self.path, 'a') as srcfile:
            srcfile.writelines(sec_content)


class RunFile:
    path = ''

    def __init__(self):
        print('new scenario file')

    def write(self, metcond, rec):
        with open('enm.1cs') as f:
            content = f.readlines()
        f.close()

        content[4] = 'QGISENM.SRC\n'
        content[6] = 'QGISENM.SEC\n'
        content[9] = '20,85,%.1f,%.1f, 4 ,%d,\n' % (metcond.wind_speed, metcond.wind_dir, metcond.temp_grad)
        content[10] = '%d\n' % 1
        content[11] = '%.1f,%.1f,%.1f\n' % (rec.x-rec.xOffset, rec.y-rec.yOffset, rec.h)
        content[12] = '1\n'

        print('writing scenario file')
        with open('enm.1cs', 'w') as file:
            file.writelines(content)
        file.close()


class ResultTable:
    sql_create_results_table = """ CREATE TABLE IF NOT EXISTS results (
                                            id integer PRIMARY KEY,
                                            RecNo integer NOT NULL,
                                            MetCondNo integer NOT NULL,
                                            direction FLOAT(5),
                                            speed FLOAT(5),
                                            tempGrad integer NOT NULL,
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
                c.execute(self.sql_create_results_table, ())
            except Exception as e:
                print("exception")
                print(e)