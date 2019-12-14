import os, re

class h5:

    def __init__(self):

        self.directory = None
        self.data = []
    
    def scan(self, dir):

        if(dir == ""):
            return -1
        
        # extract in file name
        path = dir
        file_list = os.listdir(path)

        name = re.compile(r'\d{8}_\d{6}.(cc|note).h5')

        for a in file_list:
            searched_data = name.search(a)

            if(searched_data != None):
                cutted = a.split(".")

                if( cutted[-2] == "cc" ):
                    self.data.append(cutted[0])

        return self.data

class vsqx:

    def __init__(self):

        self.directory = None
        self.data = []
    
    def scan(self, dir):

        if(dir == ""):
            return -1
        
        # extract in file name
        path = dir
        file_list = os.listdir(path)

        name = re.compile(r'\d{8}_\d{6}.vsqx')

        for a in file_list:
            searched_data = name.search(a)

            if(searched_data != None):
                cutted = a.split(".")

                if( cutted[-1] == "vsqx" ):
                    self.data.append(cutted[0])

        return self.data

class wav:

    def __init__(self):

        self.directory = None
        self.data = []
    
    def scan(self, dir):

        if(dir == ""):
            return -1
        
        # extract in file name
        path = dir
        file_list = os.listdir(path)

        name = re.compile(r'\d{8}_\d{6}_01_A.wav')

        for a in file_list:
            searched_data = name.search(a)

            if(searched_data != None):
                cutted = a.split(".")

                if( cutted[-1] == "wav" ):
                    self.data.append(cutted[0])

        return self.data

class fileNameSpliter:

    def __init__(self):

        self.h5 = h5()
        self.vsqx = vsqx()
        self.wav = wav()
