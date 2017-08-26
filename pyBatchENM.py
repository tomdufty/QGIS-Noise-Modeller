class ENMrun:
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