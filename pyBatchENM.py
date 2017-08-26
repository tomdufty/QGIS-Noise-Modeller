class ENMrun:
    def __init__(self,source,section):
        self.source=source
        self.section=section
    def start_run(self):
        print('running')

class source_file:
    path = ''

    def __init__(self):
        print('new source file')
